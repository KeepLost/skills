---
name: skill-creator
description: "Use when creating, editing, auditing, validating, or packaging OpenCode skills. Provides lean architecture guidance, scaffolding, validation, and conservative packaging checks."
---

# Skill Creator

Build small OpenCode-native skills that add only guidance or resources the model cannot reliably infer.

## Architecture

- `SKILL.md` holds concise trigger-specific guidance.
- `scripts/` holds deterministic helpers; `references/` holds on-demand detail; `assets/` holds output resources. Create only what is needed.
- Metadata is always visible, while the body and resources load on demand. Keep frequent-load content short.
- Do not add README, changelog, setup, or duplicate documentation files.

## Frontmatter

- Allowed keys: `name`, `description`, `license`, `compatibility`, `metadata`.
- `name` must be lowercase hyphen-case and match the skill directory basename.
- `description` must state both the trigger and the capabilities gained after loading, preferably as `Use when ... Provides ...`.
- Describe capabilities, not the complete workflow. Put operational detail in the body.

## Commands

```bash
python scripts/init_skill.py <name> --path <parent>
python scripts/quick_validate.py <skill-directory>
python scripts/package_skill.py <skill-directory> [output-directory]
```

After scaffolding, delete placeholders and unused resources. During edits or audits, remove generic advice while preserving non-obvious constraints, exact commands, and safety rules.

Validation checks structure, frontmatter, and folder/name consistency. Packaging applies conservative checks for sensitive paths and likely hardcoded secrets, but this is not a guarantee: still inspect the resulting archive before distribution.

