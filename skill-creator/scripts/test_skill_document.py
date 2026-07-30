#!/usr/bin/env python3
"""Contract tests for the lightweight OpenCode skill guide."""

from pathlib import Path
from unittest import TestCase, main


SKILL_MD = Path(__file__).resolve().parent.parent / "SKILL.md"


class TestSkillDocument(TestCase):
    def test_description_states_triggers_and_loaded_capabilities(self):
        content = SKILL_MD.read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1].lower()

        self.assertIn("description:", frontmatter)
        self.assertIn("use when", frontmatter)
        for trigger in ("creating", "editing", "auditing", "validating", "packaging"):
            self.assertIn(trigger, frontmatter)
        self.assertIn("provides", frontmatter)
        for capability in (
            "lean architecture",
            "scaffolding",
            "validation",
            "conservative packaging checks",
        ):
            self.assertIn(capability, frontmatter)

    def test_packaging_guidance_requires_inspection_without_safety_guarantee(self):
        content = SKILL_MD.read_text(encoding="utf-8").lower()

        self.assertIn("conservative checks", content)
        self.assertIn("still inspect", content)
        self.assertIn("not a guarantee", content)

    def test_skill_guide_stays_lean(self):
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertLessEqual(len(content.splitlines()), 60)
        self.assertNotIn("## Edit workflow", content)


if __name__ == "__main__":
    main()
