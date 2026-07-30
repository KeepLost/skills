#!/usr/bin/env python3
"""
Regression tests for skill initialization.
"""

import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import init_skill


class TestInitSkill(TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_init_skill_"))

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_generated_description_placeholder_is_yaml_string(self):
        with redirect_stdout(StringIO()):
            skill_dir = init_skill.init_skill("yaml-description-skill", self.temp_dir, [], False)

        self.assertIsNotNone(skill_dir)
        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1]

        self.assertIn("description: '[TODO:", frontmatter)

        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed")

        parsed = yaml.safe_load(frontmatter)

        self.assertIsInstance(parsed["description"], str)
        self.assertTrue(parsed["description"].startswith("[TODO: Use when "))
        self.assertIn(" Provides ", parsed["description"])

    def test_generated_template_is_lean(self):
        with redirect_stdout(StringIO()):
            skill_dir = init_skill.init_skill("lean-skill", self.temp_dir, [], False)

        content = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

        self.assertLess(len(content), 1200)
        self.assertNotIn("Structuring This Skill", content)
        self.assertNotIn("Examples from other skills", content)

    def test_all_generated_text_is_written_as_utf8(self):
        original_write_text = Path.write_text
        encodings = []

        def write_text(path, data, *args, **kwargs):
            encodings.append(kwargs.get("encoding"))
            return original_write_text(path, data, *args, **kwargs)

        with patch.object(Path, "write_text", autospec=True, side_effect=write_text):
            with redirect_stdout(StringIO()):
                result = init_skill.init_skill(
                    "utf8-skill",
                    self.temp_dir,
                    ["scripts", "references", "assets"],
                    True,
                )

        self.assertIsNotNone(result)
        self.assertEqual(encodings, ["utf-8"] * 4)


if __name__ == "__main__":
    main()
