---
name: uv-python
description: "Use when installing Python versions, creating environments, managing project dependencies, initializing or migrating Python projects, or installing and running Python CLI tools; loading this reference provides project-local setup, sync/run, tool, and migration capability with uv. Mandatory for every Python commands. Must read first before executing any Python codes."
---

# uv Python Reference

Use uv's project interface for normal development. A project is defined by `pyproject.toml`, resolved in `uv.lock`, and synchronized into `.venv`. Use `uv run`; activation is not required.

## SOP for Python Projects

All Python projects use `uv` to manage Python dependencies by default, unless user has another insturctions.

Usually the virual environment created by `uv` would be installed in the `.venv/` folder under the project's root.

## Project Setup

Create a new project:

```bash
uv init my-project
cd my-project
uv python pin 3.12
uv add httpx
uv run python -c "import httpx"
```

For an existing project containing `pyproject.toml`:

```bash
uv sync
uv run python -m your_package
```

`uv sync` creates `.venv` when needed and makes it match the lockfile and project metadata. Commit `pyproject.toml` and `uv.lock`; normally ignore `.venv/`. Use `uv venv .venv` only outside a uv project or when explicit environment creation is useful.

## Python Versions And Environments

```bash
uv python list                 # Show available and installed interpreters
uv python install 3.12         # Install a uv-managed interpreter
uv python pin 3.12             # Write the project's .python-version
uv venv --python 3.12 .venv    # Explicitly create an environment
```

`requires-python` declares compatibility; `.python-version` selects a development interpreter.

## Project Dependencies

```bash
uv add requests                # Add a runtime dependency and sync
uv add 'django>=5,<6'
uv remove requests             # Remove a dependency and sync
uv sync                        # Lock if needed, then synchronize .venv
uv run pytest                  # Run inside the synchronized project env
uv run python script.py
```

Prefer these commands over installing directly into the environment. Edit `pyproject.toml` when metadata has no suitable command, then run `uv lock` or `uv sync`.

Useful checks and reproducible execution:

```bash
uv lock --check                # Fail if uv.lock is outdated
uv sync --locked               # Fail rather than update an outdated lockfile
uv run --locked pytest         # Run without permitting lockfile changes
uv tree                        # Inspect the resolved dependency tree
```

## Development Groups Versus Extras

Dependency groups are for development tasks, not published extras. Normal sync includes `dev`.

```bash
uv add --dev pytest            # Add to dependency-groups.dev
uv add --group lint ruff       # Add to a named development group
uv sync --no-dev               # Exclude the dev group
uv sync --group lint           # Include a named group
uv sync --all-groups           # Include every dependency group
```

Extras are consumer-facing features in `project.optional-dependencies`; they are opt-in.

```bash
uv add --optional postgres psycopg
uv sync --extra postgres
uv sync --all-extras
uv run --extra postgres python app.py
```

Do not use extras for test or lint tooling unless consumers genuinely need it.

## CLI Tools

Install a tool persistently when its console command should remain available:

```bash
uv tool install ruff
ruff check .                    # Run the installed console command directly
uv tool list
uv tool upgrade ruff
uv tool uninstall ruff
```

If needed, run `uv tool update-shell` and start a new shell to update `PATH`.

Use `uvx` (an alias for `uv tool run`) for temporary execution, not to invoke an installed tool:

```bash
uvx ruff check .
uvx --from httpie http --help   # Package name and command name differ
uvx --from 'ruff==0.12.0' ruff check .
```

Put reproducible project tools in a dependency group; reserve `uvx` for deliberate one-offs.

## Migrating Existing Projects

Treat migration as metadata translation, not merely environment recreation.

For a requirements-based project, start with:

```bash
uv init --bare
uv add -r requirements.txt
uv sync
```

Then review `pyproject.toml` and `uv.lock`: confirm markers, extras, constraints, direct URLs, indexes, editable/local sources, and runtime-versus-development classification. `uv add -r` is useful, but neither bulk import nor one-by-one addition guarantees lossless retention.

For `setup.py`, translate metadata into `[project]`, optional features into `[project.optional-dependencies]`, development dependencies into `[dependency-groups]`, and retain an appropriate `[build-system]`. Editable sources and overrides may require `[tool.uv.sources]`. Repeated `uv add` does not guarantee preservation of markers, extras, editable behavior, or build metadata; inspect and test builds.

Verify the migrated project with its tests and, for a distributable package, build it with `uv build` and inspect the resulting metadata.

