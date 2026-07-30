---
name: agents-md-writer
description: Use when creating, reviewing, or modifying AGENTS.md, deciding what guidance belongs there, or resolving instruction scope and hierarchy. Load for scope rules, draft approval requirements, and deterministic validation.
---

# AGENTS.md Writer

## Purpose

Use this skill for deliberate AGENTS.md content decisions. It owns what belongs in AGENTS.md, instruction scope and hierarchy, the write approval gate, and deterministic validation.

In default AGENTS.md shall be written by human, because it's a persistent context that you automatically load in every conversation. User needs your assistant mainly because you can help them do some lengthy tedious work that human hates; it does not mean an automatic approval.

## Responsibility Boundaries

Keep the task limited to drafting, reviewing, or modifying AGENTS.md content. Do not turn it into reusable process-document authoring, current-session management, runtime configuration, permission setup, or initialization-generator work. Private status, Git, notification, and task-lifecycle machinery stays out of public AGENTS content. Do not call, wrap, reimplement, or claim to intercept mutating initialization generators unless the user explicitly requests one.

Review only requests may report findings without write authorization. Creation or modification requires a standalone explicit AGENTS task, a complete draft shown to the user, then explicit approval after the display before writing.

## Runtime And Hierarchy Checks

Before drafting hierarchy language, identify two things:

1. Host runtime: the agent environment currently doing the work.
2. Target AGENTS consumer: the runtime expected to read the file, such as OpenCode, Codex, Cursor, Cline, or several clients.

Verify the target consumer's AGENTS.md hierarchy semantics from authoritative evidence before claiming precedence. If the target is unknown or mixed, avoid universal nearest file claims. Say which semantics are known, which are unverified, and write portable content without false precedence rules.

OpenCode reads the first AGENTS.md found by walking upward from the current working directory. In practice almost all AI agents (including Codex, Cursor, Cline, etc.) except Claude Code follow this convention. You can safely follow this assumption without loss of generality, unless you're inside Claude Code or user gives another instruction.

## Content Model

AGENTS.md captures tacit project knowledge, not a project overview. Never restate what the agent can read directly from the code and config. Every sentence must earn its place by being a fact or rule the agent could NOT quickly and reliably discover by reading the repository itself. Use three layers:

1. Project owned trigger to action guidance: the tacit HOW behind a task, not the observable WHAT. State the tool, command, flag, ordering, or gate that isn't obvious from the tree. For testing, state how to run the suite (for example `uv run pytest -q`, never bare `pytest`), not which behaviors the test files already assert. For dependencies, state the policy and tool (for example manage deps with `uv`, never hand-edit requirements), not the package list that `pyproject.toml` already holds.
2. Middle abstraction cognitive alignment: a coherent paragraph giving the project reference frame, goals, invariants, and tradeoffs that code won't reveal by failing tests (for example "money is integer cents everywhere; never introduce floats").
3. Maintenance protection for AGENTS.md itself: a short rule saying AGENTS.md changes need explicit authorization, a shown draft, approval of that draft, and a standalone task.

Turn negative constraints into positive alternatives when possible. If no alternative exists, explain the rationale so the agent can apply the principle in nearby cases.

## Discoverability Filter

Apply this sentence by sentence, alongside the Ownership Filter. For each candidate sentence ask: could an agent learn this reliably in a few minutes by reading the repo's code and config?

1. YES, it is discoverable (dependency lists, directory trees, what each module or test does, which framework is imported, generic "write tests" or "keep code clean" advice) -> cut it. It is noise that competes with the tacit rules.
2. NO, it is tacit (a required tool or command, a non-obvious ordering, an invariant, a gotcha, a rule enforced only by convention) -> keep it. This is what AGENTS.md exists for.
3. Point, don't restate. When discoverable info matters for orientation, point to where it lives (for example "deps are in `pyproject.toml`") instead of copying it, so it cannot drift out of sync.
4. Drift test. If a fact would silently go stale when someone edits code without touching AGENTS.md, don't state it verbatim. State the durable rule and point to the living source of truth.

When unsure, prefer cutting. A short file of pure tacit rules beats a long file that buries them under a project summary.

## Ownership Filter

Apply this sentence by sentence:

1. If it describes the project, its public commands, its architecture, its durable safety boundary, or its contributor facing workflow, it can belong.
2. If it describes one maintainer's preference, private tool, hidden hook, notification habit, local status file, or personal workflow, keep it out.
3. If a personal preference can be translated into a project fact that remains true under a different maintainer, write the project fact instead.
4. Remove dead links and private skill names from generated project AGENTS content. Replace them with public, runnable alternatives when available.

Keep detailed approval mechanics, private skill names, validator mechanics, and size limits outside generated project AGENTS content. They belong in this skill, not in each repository's AGENTS.md.

## Workflow Checklist

1. Confirm the user made a standalone AGENTS request. If it's a drive by change during unrelated work, stop and ask for a separate AGENTS task.
2. Identify host runtime and target consumer. Verify hierarchy semantics from authoritative evidence before writing precedence claims.
3. Filter requested content with the ownership test and the discoverability test. Keep tacit rules, non-obvious commands, orderings, and invariants. Cut anything the agent could read straight from the code or config, and exclude private hooks, private skills, personal notifications, and developer specific habits.
4. Draft compact AGENTS content using the three layers. Avoid templates unless the user asked for one.
5. Display the complete draft to the user. For review only, report findings and don't write.
6. For creation or modification, write only after explicit approval of the displayed draft.
7. Validate the AGENTS.md draft or file from this skill directory with `node scripts/validate-agents-md.mjs <path>`. The file must be `<=300` logical lines and `<=10,000` normalized Unicode code points.

If either validation limit is exceeded, compress, restructure, or externalize non-core guidance. Don't bypass the validator or copy the limits into generated project AGENTS content.

## Common Failure Modes

| Failure | Correct behavior |
| --- | --- |
| "It's only one file, so write it now." | Treat AGENTS.md mutation as privileged context work that needs its own task, draft, and approval. |
| "The user listed private release hooks, so include them." | Keep the public command or project fact, and omit private hooks or replace them with public contributor guidance. |
| "Run `/init-deep` to save time." | Don't call initialization generators unless the user explicitly chose that workflow. This skill drafts and reviews content. |
| "Nearest AGENTS.md always wins." | Verify the target consumer. Use OpenCode's cwd based first match only for OpenCode. |
| "Describe each directory and module so the agent understands the layout." | The tree is readable from the repo. Cut it. Keep only a non-obvious structural rule (for example "business logic lives in `services/`, keep routers thin") if it isn't clear from the code. |
| "List what the tests cover." | The test files already show that. State how to run them (the tool, command, and flags) and any non-obvious gate, not what they assert. |
| "List the dependencies so the agent knows the stack." | `pyproject.toml` (or equivalent) already lists them. State the dependency tool and policy, and point to the manifest instead of copying it. |
| "Add a general 'write tests and keep code clean' section." | Generic best practice is not tacit project knowledge. Cut it unless the project enforces a specific, non-obvious rule. |

