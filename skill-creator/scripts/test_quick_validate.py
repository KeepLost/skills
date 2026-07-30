#!/usr/bin/env python3
"""
Regression tests for quick skill validation.
"""

import os
import tempfile
from pathlib import Path
from unittest import TestCase, main

import quick_validate


class TestQuickValidate(TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="test_quick_validate_"))

    def tearDown(self):
        import shutil

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_accepts_crlf_frontmatter(self):
        skill_dir = self.temp_dir / "crlf-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\r\nname: crlf-skill\r\ndescription: Use when testing CRLF input. Provides validation.\r\n---\r\n# Skill\r\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertTrue(valid, message)

    def test_accepts_current_directory_path(self):
        skill_dir = self.temp_dir / "current-dir-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: current-dir-skill\ndescription: Use when validating the current directory. Provides validation.\n---\n# Skill\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        previous_cwd = Path.cwd()

        try:
            os.chdir(skill_dir)
            valid, message = quick_validate.validate_skill(".")
        finally:
            os.chdir(previous_cwd)

        self.assertTrue(valid, message)

    def test_rejects_missing_frontmatter_closing_fence(self):
        skill_dir = self.temp_dir / "bad-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: bad-skill\ndescription: missing end\n# no closing fence\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertEqual(message, "Invalid frontmatter format")

    def test_fallback_parser_handles_multiline_frontmatter_without_pyyaml(self):
        skill_dir = self.temp_dir / "multiline-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = """---
name: multiline-skill
description: Use when PyYAML is unavailable. Provides fallback validation.
compatibility: Requires Python 3.9 or newer
metadata: |
  {
    "owners": ["team-openclaw"]
  }
---
# Skill
"""
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        previous_yaml = quick_validate.yaml
        quick_validate.yaml = None
        try:
            valid, message = quick_validate.validate_skill(skill_dir)
        finally:
            quick_validate.yaml = previous_yaml

        self.assertTrue(valid, message)

    def test_accepts_compatibility_frontmatter(self):
        skill_dir = self.temp_dir / "compatible-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = """---
name: compatible-skill
description: Use when OpenCode compatibility matters. Provides compatibility guidance.
compatibility: Requires OpenCode
---
# Skill
"""
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertTrue(valid, message)

    def test_rejects_unsupported_frontmatter_keys(self):
        skill_dir = self.temp_dir / "unsupported-key-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = """---
name: unsupported-key-skill
description: Use when testing unsupported keys. Provides validation.
homepage: https://example.com
---
# Skill
"""
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertIn("homepage", message)

    def test_rejects_folder_and_frontmatter_name_mismatch(self):
        skill_dir = self.temp_dir / "folder-name"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = """---
name: frontmatter-name
description: Use when testing mismatched names. Provides validation.
---
# Skill
"""
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertIn("folder-name", message)
        self.assertIn("frontmatter-name", message)

    def test_rejects_empty_name(self):
        skill_dir = self.temp_dir / "empty-name-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = '---\nname: ""\ndescription: Use when testing empty names. Provides validation.\n---\n# Skill\n'
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertEqual(message, "Name must not be empty")

    def test_rejects_whitespace_only_name(self):
        skill_dir = self.temp_dir / "ws-name-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: '   '\ndescription: Use when testing blank names. Provides validation.\n---\n# Skill\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertEqual(message, "Name must not be empty")

    def test_rejects_empty_description(self):
        skill_dir = self.temp_dir / "empty-desc-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = '---\nname: valid-skill\ndescription: ""\n---\n# Skill\n'
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertEqual(message, "Description must not be empty")

    def test_rejects_whitespace_only_description(self):
        skill_dir = self.temp_dir / "ws-desc-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: valid-skill\ndescription: '   '\n---\n# Skill\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertEqual(message, "Description must not be empty")

    def test_rejects_description_without_trigger_or_capability(self):
        skill_dir = self.temp_dir / "weak-description-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: weak-description-skill\ndescription: ok\n---\n# Skill\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertIn("Use when", message)
        self.assertIn("capability", message)

    def test_rejects_trigger_description_without_capability_marker(self):
        skill_dir = self.temp_dir / "trigger-only-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: trigger-only-skill\ndescription: Use when validating a skill.\n---\n# Skill\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertIn("capability", message)

    def test_accepts_use_only_when_with_loading_capability(self):
        skill_dir = self.temp_dir / "restricted-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = "---\nname: restricted-skill\ndescription: Use only when packaging a local skill. Loading adds conservative checks.\n---\n# Skill\n"
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

        valid, message = quick_validate.validate_skill(skill_dir)

        self.assertTrue(valid, message)


if __name__ == "__main__":
    main()
