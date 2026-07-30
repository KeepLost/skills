#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import re
import sys
import zipfile
from pathlib import Path

from quick_validate import validate_skill


EXCLUDED_DIRS = {".git", ".svn", ".hg", "__pycache__", "node_modules"}
SENSITIVE_FILENAMES = {
    ".npmrc",
    ".pypirc",
    ".netrc",
    "credentials.json",
    "secrets.json",
}
SENSITIVE_ARCHIVE_SUFFIXES = (".skill", ".zip", ".tar", ".tgz", ".gz")
BEARER_PATTERN = re.compile(
    r"\bAuthorization\s*:\s*Bearer\s+([A-Za-z0-9._~+/-]{16,})",
    re.IGNORECASE,
)
NAMED_SECRET_PATTERN = re.compile(
    r"^\s*(?:export\s+)?(?:[A-Z][A-Z0-9_]*(?:_TOKEN|_KEY|_SECRET)|PASSWORD)"
    r"\s*=\s*['\"]?([^\s'\"#]{16,})",
    re.IGNORECASE | re.MULTILINE,
)
PLACEHOLDER_MARKERS = (
    "example",
    "placeholder",
    "replace-with-runtime-secret",
    "replace-me",
    "changeme",
)
PEM_BEGIN = "-----BEGIN "
PEM_PRIVATE_KEY_END = "PRIVATE KEY-----"


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _is_sensitive_path(path: Path) -> bool:
    for part in path.parts:
        name = part.lower()
        if name == ".env.example":
            continue
        if (
            name == ".env"
            or name.endswith(".env")
            or name.endswith(".pem")
            or name.endswith(".key")
            or name in {"id_rsa", "id_ed25519"}
            or name in SENSITIVE_FILENAMES
            or name.endswith(SENSITIVE_ARCHIVE_SUFFIXES)
        ):
            return True
    return False


def _is_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return normalized.startswith("$") or any(
        marker in normalized for marker in PLACEHOLDER_MARKERS
    )


def _find_secret_in_text(text: str):
    for pattern, label in (
        (BEARER_PATTERN, "Authorization bearer token"),
        (NAMED_SECRET_PATTERN, "named secret assignment"),
    ):
        for match in pattern.finditer(text):
            if not _is_placeholder(match.group(1)):
                return label

    for line in text.splitlines():
        marker = line.strip()
        if marker.startswith(PEM_BEGIN) and marker.endswith(PEM_PRIVATE_KEY_END):
            return "PEM private key marker"
    return None


def _read_utf8_text(path: Path):
    data = path.read_bytes()
    if b"\x00" in data or any(byte < 9 or 13 < byte < 32 for byte in data):
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .skill file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .skill file (defaults to current directory)

    Returns:
        Path to the created .skill file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"[ERROR] Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"[ERROR] Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"[ERROR] Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"[OK] {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    files = sorted(
        skill_path.rglob("*"),
        key=lambda path: path.relative_to(skill_path).as_posix(),
    )

    # Refuse the entire package before creating an archive that could be mistaken
    # for a successful, safe artifact.
    for file_path in files:
        if file_path.is_symlink():
            continue
        relative_path = file_path.relative_to(skill_path)
        if any(part in EXCLUDED_DIRS for part in relative_path.parts):
            continue
        if file_path.is_file() and file_path.resolve() == skill_filename.resolve():
            continue
        if _is_sensitive_path(relative_path):
            print(f"[ERROR] Refusing to package sensitive path: {file_path}")
            return None
        if file_path.is_file():
            try:
                text = _read_utf8_text(file_path)
            except OSError as e:
                print(f"[ERROR] Could not inspect file before packaging: {file_path}: {e}")
                return None
            if text is not None:
                secret_type = _find_secret_in_text(text)
                if secret_type:
                    print(
                        f"[ERROR] Refusing to package possible {secret_type} in: "
                        f"{file_path}"
                    )
                    return None

    # Create the .skill file (zip format)
    try:
        with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Walk in a deterministic order. Sort by the archive-relative POSIX
            # entry name (not Path object order, which is filesystem/OS-flavour
            # dependent) so written .skill entries are byte-stable everywhere.
            for file_path in files:
                # Security: never follow or package symlinks.
                if file_path.is_symlink():
                    print(f"[WARN] Skipping symlink: {file_path}")
                    continue

                rel_parts = file_path.relative_to(skill_path).parts
                if any(part in EXCLUDED_DIRS for part in rel_parts):
                    continue

                if file_path.is_file():
                    resolved_file = file_path.resolve()
                    if not _is_within(resolved_file, skill_path):
                        print(f"[ERROR] File escapes skill root: {file_path}")
                        return None
                    # If output lives under skill_path, avoid writing archive into itself.
                    if resolved_file == skill_filename.resolve():
                        print(f"[WARN] Skipping output archive: {file_path}")
                        continue

                    # Calculate the relative path within the zip.
                    arcname = Path(skill_name) / file_path.relative_to(skill_path)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n[OK] Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"[ERROR] Error creating .skill file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        print("\nExample:")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
