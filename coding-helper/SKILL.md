---
name: coding-helper
description: "Use when a software engineering task involves understanding a codebase, shaping requirements, planning, implementation, bug fixing, refactoring, testing, code review, or delivery. It provides a complete end-to-end engineering operating procedure, explicit decision gates, debugging and test discipline, delegation rules, verification criteria, completion checks, and on-demand local references for common development domains. Mandatory for every code-related task. Only after reading this skill shall you start reading or writing codes."
---

# Coding Helper

Read this file _completely_ before acting. This file is the single source of process rules about coding. Every requirement, threshold, ordering constraint, severity definition, and authorization boundary you must follow is here.

Certainly you know how to code as your training data teaches you. However **user wishes you to align with the coding style they prefer, which they think of is the best way to efficiency and success, and that is detailedly recorded in this skill.** Just follow these instructions.

## What This Gives You

- One route from initial investigation through evidence-backed completion.
- A task classifier that avoids unnecessary design, planning, or test ceremony.
- Root-cause debugging and test-first behavior-change discipline.
- Safe rules for delegation, review, Git operations, and user-owned changes.
- Concrete completion evidence instead of unsupported success claims.
- Optional local references for specific engineering domains.

The skill itself is offline-capable.

## Operating Contract

1. Follow system, developer, user, and project-local instructions before this generic procedure. Treat task-specific governance as authoritative.
2. Inspect before changing. Use an available code index first; otherwise use focused search and file reads. Do not guess architecture from filenames.
3. Protect concurrent work. Never discard, overwrite, or reformat unrelated user or agent changes. Treat everything you did not just write as user-owned. Stop and ask only when they directly conflict.
4. Prefer the smallest correct change. Do not add compatibility layers, abstractions, dependencies, or refactors without a concrete need.
5. Treat every Git write as user-owned. Read-only inspection is safe. Do not do any of the following without explicit user authorization for that specific operation:
   - stage, commit, amend, merge, rebase, cherry-pick, tag;
   - create, switch, rename, or delete a branch;
   - create, move, lock, prune, or remove a worktree;
   - push, force-push, change tracking, open or modify a PR;
   - discard files, clean untracked files, or rewrite history.

   A task plan, repository convention, or reviewer suggestion is not authorization. Push authorization does not imply PR authorization, or the reverse.
6. Match process depth to risk. A one-line exact edit is not a design project; a cross-system behavior change is not a one-line task. Calibration:
   - "Fix this typo in the log message" → edit, verify it builds, done. No task list, no design, no new tests.
   - "Add a `--dry-run` flag to the existing CLI command" → small plan (§4), one focused test (§6.2 new-behavior), implement, verify.
   - "Add multi-tenant support across the API" → Design route first (§3): ambiguous scope, new architecture decisions, needs approval before code.

## Stop Conditions

These apply at every step, in every route. Stop and ask the user when ANY is true. Do not work around them, when:

- Requirements, permissions, or change ownership are materially ambiguous.
- The approved plan is unsafe or impossible in the current repository.
- Baseline checks already fail, so new failures cannot be attributed to your change (§9).
- Three materially different fix attempts have failed (§6.1).
- A required secret, service, device, or credential is unavailable.
- A Git write or destructive action is needed but not explicitly authorized (contract §5).
- Unrelated user or agent changes directly conflict with the requested change.

Reporting a blocker with concrete evidence is a valid, complete outcome. Guessing past one is not. Honesty is a merit that you need to follow.

## 1. Classify the Task

Pick exactly one primary route before acting. Read the table top to bottom and stop at the first row that matches. Then execute only the sections listed in its "Run these sections" column, in order. Always finish with sections 8, 9, 10.

| Route | Match when | Run these sections |
|---|---|---|
| Investigation | The user wants explanation, diagnosis, or options, and did not ask for a change | 2 → 8 (report findings; make no edits) |
| Design | Requirements, behavior, or architecture are still being chosen | 2 → 3 → 4 → (then re-enter table with the approved route) |
| Direct change | Scope and expected behavior are already precise | 2 → 4 → 7 → 8 → 9 → 10 |
| Bug | Behavior is wrong, failing, flaky, or unexpectedly slow | 2 → 6.1 → 7 → 8 → 9 → 10 |
| Refactor | Behavior must stay identical while structure changes | 2 → 6.2 → 7 → 8 → 9 → 10 |
| Review | The user asks for findings, not changes | 2 → 8 (report only; do not edit unless asked) |
| Documentation/configuration | The deliverable is prose or declarative config | 2 → 7 → 8 → 9 (validate syntax/effect; do not invent fake tests) → 10 |
| Delivery | Implementation is done; integration/Git is being considered | 9 → 10 (only after explicit Git authorization) |

If two rows seem to match, pick the one with the stronger required evidence (Bug over Direct change; Design over Direct change). Reclassify when evidence changes the task; do not continue under an obsolete plan because work has started. When you reclassify, restart at the new route's section list.

Worked routing example:
- "Why does checkout return 500 for empty carts?" → user wants a diagnosis, no fix requested → Investigation → run 2, then 8.
- "Checkout returns 500 for empty carts; fix it." → wrong behavior → Bug → run 2, 6.1, 7, 8, 9, 10.
- "Should we use a queue or cron for retries?" → approach undecided → Design → run 2, 3, 4, then re-classify the agreed approach.

## 2. Understand the Work

If, and only if, the user explicitly requests reverse engineering, security assessment, penetration testing, forensics, threat hunting, or vulnerability analysis, read `../security-analysis/index.md` before any domain-specific investigation or action and follow its single-topic routing. Do not infer this trigger merely because ordinary engineering work involves authentication, permissions, cryptography, input validation, or other security-relevant code.

Before substantive edits:

- Read applicable project instructions, specifications, and architecture docs.
- Locate the relevant implementation, tests, callers, and data boundaries.
- Inspect working-tree state when version control is present. Never infer a clean tree from silence in an earlier session.
- Restate the requested outcome, non-goals, constraints, and success evidence.
- Identify assumptions. Resolve architecture, security, permission, and public contract ambiguity instead of silently choosing a direction.
- Find a nearby working example of the same pattern and compare meaningful differences.
- For unfamiliar libraries, verify current official documentation rather than relying on memory.

Stop investigation when enough evidence exists to make the next decision. Do not turn context gathering into an unbounded repository survey.

## 3. Shape Only When Needed

Decide with this test: enter design mode if ANY of these is true — otherwise skip straight to implementation.

- The requested behavior is ambiguous or under-specified.
- Two or more materially different approaches exist and the choice matters.
- Architecture, data model, or public-interface boundaries are undecided.
- The change is irreversible or high-blast-radius (schema, auth, migrations).

Decision examples:
- "Rename `getUser` to `fetchUser` everywhere" → none true → skip design, implement directly.
- "Add caching to the profile endpoint" → approach matters (in-memory vs Redis vs HTTP cache) → enter design, present options.

In design mode:

1. Ask one focused question at a time. Prefer questions that distinguish real alternatives; never ask for facts the repository or supplied specification already answers.
2. Surface oversized scope early and split independent subsystems into separately testable slices.
3. Present two or three viable approaches with a recommendation. For each, cover architecture and ownership boundaries, data and control flow, failure handling and observability, migration or compatibility impact, testability and operational cost, and complexity introduced now and later. Do not invent alternatives merely to satisfy a count.
4. A sufficient design answers all of these:
   - which components change and what each owns;
   - what inputs, outputs, invariants, and interfaces connect them;
   - where state lives and who may mutate it;
   - what happens on invalid input, partial failure, retries, or cancellation;
   - which trust, permission, privacy, or secret boundaries apply;
   - how compatibility and rollout are handled if relevant;
   - which automated tests and runtime checks demonstrate success;
   - what is explicitly out of scope.
5. Obtain user approval before implementing the unresolved design. Approval of one section does not imply approval of a materially changed scope.

Skip design ceremony for an approved specification, exact edit, narrow bug, or mechanical change that creates no new product or architecture decision.

For a visual decision, first ask whether the difference between the alternatives can be understood and decided from text. If text is insufficient and the user is also likely to have difficulty understanding or choosing between the options, propose making small front-end/HTML mockup pages for visual comparison. 
Do not start this channel automatically: only after the user agrees to this method may you use the local companion documented in [`tools/visual-companion/visual-companion.md`](tools/visual-companion/visual-companion.md) for the proposed visual comparison. It is a strictly local-only interaction channel for presenting alternatives and collecting the user's visual feedback; it does not replace the user's explicit decision or produce production UI code by itself.

## 4. Plan and Track

Create a structured task list when work has three or more meaningful steps, spans several files or systems, coordinates agents, or benefits from checkpoints. Skip the list for a single-step change. Keep exactly one item in progress and update it from fresh evidence only.

- "Fix one failing assertion in one test" → no task list.
- "Add endpoint, wire the service, add tests, update the client" → task list with one item per step.

For complex, delegated, or handoff-oriented work, write an implementation plan. Each task must deliver one independently testable outcome and must state:

- a concise objective and the requirement it satisfies;
- exact files to create, modify, or inspect;
- interfaces consumed and produced;
- ordering dependencies and assumptions;
- a failing test first for feasible new behavior;
- validation commands and expected evidence;
- explicit exclusions and likely risks.

Concrete contrast:

```
BAD:  "Add rate limiting and handle errors."
      (no files, no interface, no evidence — an agent cannot execute this)

GOOD: Objective: limit /login to 5 attempts/min per IP (req R3).
      Files: middleware/rate_limit.py (new), app/routes.py (wire in).
      Interface: limiter(key: str, limit: int, window_s: int) -> bool.
      Depends on: none. Excludes: distributed/Redis backend (out of scope).
      Test first: test_login_blocks_6th_attempt_within_window -> expect 429.
      Verify: pytest tests/test_rate_limit.py, then pytest tests/test_auth.py.
```

Split tasks where a reviewer could approve one deliverable and reject another. Keep setup, schema, documentation, and configuration with the behavior that needs them unless independently useful.

A plan must not contain:

- tasks that only say "implement", "handle errors", or "add tests";
- placeholders such as `TBD`, `TODO`, or "similar to the previous task";
- signatures used by later tasks but never defined;
- unrelated refactoring hidden inside feature work;
- commit, push, merge, or PR steps presented as automatic work.

Before executing a plan, check it yourself:

- map every requirement and non-goal to at least one task or decision;
- verify paths, names, types, and signatures are consistent across tasks;
- confirm each behavior-changing task has meaningful failure evidence;
- confirm commands suit this repository and are not invented;
- record unresolved risks and ask rather than silently choosing.

Do not require a persistent plan for a trivial single-step task. Plan commit checkpoints are suggestions, never authorization to execute Git operations (contract §5). For independent plan review, use `prompts/plan-reviewer.md`.

## 5. Delegate Deliberately

Delegate (launch sub-agents) when independent context or parallel investigation reduces risk or latency. Do not delegate merely to avoid understanding the task.

Delegate when several investigations are independent, one bounded task benefits from fresh context, a separate reviewer can challenge implementation assumptions, or parallel work shares no files, mutable resources, or ordering dependency.

Keep work local when failures may share one root cause, tasks edit overlapping files or contracts, understanding depends on a single evolving system model, delegation overhead exceeds the task, or available agents cannot access required evidence safely.

Deciding examples:
- "Find every place we read `config.yaml` and summarize how each is used" → read-only, splittable → delegate in parallel to several searchers.
- "Rename `Order.total` and update all call sites and their tests" → one shared contract, overlapping edits → keep local and sequential; do not parallelize.

Parallelize independent research and diagnosis freely. Be conservative with parallel implementation in one checkout. Before parallel dispatch, verify all of:

- scopes are independent and do not edit the same files;
- one result cannot invalidate another agent's assumptions;
- commands do not contend for the same database, port, device, or fixture;
- each agent can finish without waiting for another;
- integration and full-suite verification have a clear owner.

Each assignment must contain one bounded objective, full task requirements and relevant non-goals, exact file or subsystem scope, essential architecture and neighboring interfaces, known errors and commands with expected evidence, constraints on edits and shared resources, and a required return status. Do not pass full conversation history as a substitute for curated context. Use `prompts/implementer.md` for implementation assignments.

Handle returned status as follows:

| Status | Coordinator action |
|---|---|
| `DONE` | Inspect diff and begin review |
| `DONE_WITH_CONCERNS` | Evaluate concerns before review |
| `NEEDS_CONTEXT` | Supply missing facts and redispatch |
| `BLOCKED` | Change context, task size, or approach, or escalate |

Never retry an unchanged prompt after a genuine blocker. Never treat a worker's success statement as evidence: inspect the diff and rerun verification yourself.

When formal review is warranted, keep this gate order and do not collapse or reverse it: implementer self-review → requirement review (`prompts/spec-compliance-reviewer.md`) → implementer fixes → requirement re-review → quality review (`prompts/code-quality-reviewer.md`) → implementer fixes → quality re-review. Requirement compliance comes before code quality; blocking findings are resolved and re-reviewed before proceeding.

When parallel results return, compare diffs for overlap, reconcile assumptions, run the integrated checks, and report any unresolved conflict.

## 6. Establish Failure Evidence

Tests are evidence, not ceremony. Never write a speculative fix to "confirm" a guess: a diagnostic experiment may change one variable temporarily, but it is not production implementation.

### 6.1 Bugs and Unexpected Behavior (Bug route)

Follow this order. Do not reorder it.

1. Read the complete error, warning, stack trace, failing assertion, logs, inputs, and recent relevant changes.
2. Reproduce with exact inputs and record whether it is deterministic. Trace malformed data and unexpected control flow backward to its origin, including across process, service, queue, file, and database boundaries.
3. State one falsifiable hypothesis: cause, mechanism, and expected observation. Test one variable at a time. If reproduction is intermittent, add instrumentation or condition-based observation instead of guessing; do not add arbitrary sleeps or raise timeouts unless the timeout itself is the verified requirement.
4. After the cause is understood, write a failing regression test and run it. Confirm it fails because the diagnosed defect is present, not from a typo, broken fixture, missing dependency, or unrelated baseline failure. A valid regression test names the behavior rather than the implementation detail, exercises real code where practical, has a clear expected failure message or value, passes only when the root cause is corrected, and stays useful against recurrence.
5. Implement the smallest fix at the root cause. Do not bundle cleanup, dependency upgrades, compatibility layers, or neighboring behavior unless the fix genuinely requires them.
6. Verify the regression, surrounding behavior, and relevant quality checks (§9).

If automation is not feasible, use a minimal reproducible script or documented runtime check and state the limitation explicitly. If three materially different fix attempts fail, stop stacking patches and return to Stop Conditions.

### 6.2 New or Changed Behavior (Direct change and Refactor routes)

For a Refactor, first write characterization tests that lock in current behavior, then restructure while they stay green.

For new behavior, when executable tests are meaningful and practical:

1. **RED:** Write the smallest behavior-focused test.
2. Run it and confirm it fails for the expected missing behavior. If it passes, you have not established RED: the behavior may already exist or the test may not exercise it. Fix the test or scope before writing code.
3. **GREEN:** Implement only enough to pass.
4. Run the focused test, then relevant surrounding tests.
5. Refactor only while all affected tests stay green.
6. Repeat for the next behavior.

Worked cycle — add `slugify` that lowercases and hyphenates:

```
# 1. RED: write one focused test
test_slugify_lowercases_and_hyphenates:
    assert slugify("Hello World") == "hello-world"

# 2. Run it. Expected failure (function does not exist yet):
#    NameError: name 'slugify' is not defined   <- this is valid RED
#    If it had errored on a typo in the test instead, that is NOT valid RED.

# 3. GREEN: implement the minimum
def slugify(s): return s.lower().replace(" ", "-")

# 4. Run the focused test -> passes. Run neighboring tests -> still green.
# 5. Only now refactor (e.g. handle repeated spaces) with tests staying green.
```

Do not manufacture tests for prose or declarative configuration with no executable behavior. Instead validate parsing, schema validity, generated output, command behavior, or the smallest relevant runtime effect.

### 6.3 Test Quality Rules

Write tests that are focused on one behavior and named in domain terms, deterministic and order-independent, explicit about boundary and error cases, built on public behavior rather than private implementation, economical with mocks, and clear enough to read as documentation.

Never do any of the following:

- assert that a mock was called without checking the real outcome;
- add production methods only to make tests convenient;
- use a broad snapshot for a small semantic requirement;
- insert arbitrary timing delays;
- weaken an assertion to make a failing suite green;
- change a regression expectation to match the defect.

## 7. Implement the Smallest Correct Change

Before the first edit: read the complete approved requirement or plan, inspect project instructions and relevant code and tests, identify gaps and destructive consequences, resolve blockers rather than guessing through a critical ambiguity, and establish a clean or explicitly understood test baseline (§9). Never begin on a protected branch when project rules forbid it.

- Follow existing architecture, naming, error handling, and test conventions.
- Keep each edit focused on the requested behavior and its necessary support.
- Preserve public contracts unless the approved task explicitly changes them.
- Validate inputs and errors at meaningful boundaries, not every layer by habit.
- Avoid hidden global state, speculative extensibility, and test-only production APIs.
- Add dependencies only after confirming the project does not already provide the capability and the dependency is justified.
- Keep secrets out of source, examples, logs, patches, archives, and prompts.
- After each coherent step, inspect the resulting diff before continuing.

If the plan conflicts with codebase reality, pause and revise the plan or ask the user. Do not force the repository to match a stale plan.

Use domain references only when their trigger matches:

| Need | Local reference |
|---|---|
| API, backend, auth, data, realtime, production hardening | `references/application-fullstack.md` |
| Kotlin, Compose, Gradle, Android platform behavior | `references/mobile-android.md` |
| Swift, UIKit, SwiftUI, Apple platform behavior | `references/mobile-ios.md` |
| Frontend visual direction, motion, accessibility | `references/frontend-ui.md` |
| GLSL, WebGL, SDF, ray marching, simulation | `references/graphics-shaders.md` |
| Agent-facing tool contracts and schemas | `references/tool-interface-design.md` |
| Agent context assembly, retrieval, memory, compression, session continuity, or diagnosing context-induced agent failure | `references/agent-context-design.md` |
| Formal BDI, RDF, OWL, or SPARQL modeling | `references/bdi-modeling.md` |

## 8. Review the Result

Review and verification answer different questions. Requirement review asks whether you built exactly what was requested (evidence: spec-to-diff mapping). Quality review asks whether the implementation is safe and maintainable (evidence: code, tests, architecture). Verification asks whether the current repository state actually passes (evidence: fresh command output, §9). Passing tests cannot excuse a missing requirement; spec compliance cannot excuse unsafe code.

Review the complete change, not only the latest edit.

Requirement review — read the requirements independently of any implementation summary, then inspect the actual diff and surrounding code for:

- every requested behavior, constraint, and acceptance criterion;
- explicit non-goals and unchanged contracts;
- missing error paths, migrations, documentation, or platform handling;
- extra features, dependencies, compatibility layers, or refactors;
- mismatches in names, types, defaults, copy, and interfaces;
- tests that prove each observable requirement rather than merely execute code.

Quality review — after requirement compliance is established, inspect for:

- incorrect logic, boundary errors, races, stale state, unsafe assumptions;
- security, permission, privacy, secret-handling, and injection risks;
- error handling that loses context or leaves partial state;
- public contract regressions and compatibility hazards;
- unnecessary complexity, duplication, coupling, or speculative abstraction;
- weak, flaky, over-mocked, or missing tests;
- performance issues on realistic paths and data sizes;
- misleading names, comments, docs, or dead code.

Also confirm generated and copied material contains no placeholders, stale names, credentials, or dead links.

Report findings ordered by severity, using these definitions:

- **Critical:** data loss, security exposure, crash, or fundamentally wrong result.
- **Important:** likely regression, missing requirement, unreliable test, or maintainability issue that should block completion.
- **Minor:** bounded clarity or cleanup improvement that does not block use.

Critical and Important findings are blocking and must be resolved before integration. Each finding states the defect and severity, the file and narrow line range, the input or scenario that triggers it, the impact on users or data or maintenance, and the smallest direction for correction without rewriting the task.

```
[Critical] SQL injection in user lookup
  File: app/db/users.py:42
  Trigger: username containing a single quote, e.g. "a' OR '1'='1".
  Impact: attacker reads or deletes arbitrary rows; auth bypass.
  Fix direction: use a parameterized query instead of f-string interpolation.
```

If there are no findings, say so and identify residual testing or environment gaps.

When receiving review feedback:

1. Read all items before changing code.
2. Clarify ambiguous or mutually dependent items.
3. Verify each claim against current code, requirements, and platform support.
4. Implement correct findings one at a time.
5. Push back factually when advice is incorrect, unnecessary, or incompatible.
6. Rerun affected tests after each behavior-changing correction.
7. Request re-review of the complete affected scope.

Feedback is technical input, not automatic authority. Do not performatively agree, blindly implement, or silently ignore a finding. Escalate conflicts with user-approved architecture to the user.

## 9. Verify With Fresh Evidence

Establish a baseline before changing behavior when practical: run the project-appropriate focused or baseline test command so new failures are distinguishable from pre-existing ones. Run only setup commands justified by project files, and do not silently upgrade lockfiles or dependencies. If baseline checks fail, report exact evidence and ask whether to investigate or proceed with the failure documented (Stop Conditions).

For every completion claim:

1. Identify the exact command or inspection that proves it.
2. Run it fresh after the final change, not from memory or an earlier run.
3. Read the relevant complete output and exit status.
4. Count failures, warnings, skipped checks, and untested requirements.
5. Make only the claim the evidence supports.

Run checks from narrow to broad:

1. the exact regression or new-behavior test;
2. the containing file or component suite;
3. tests for callers, integrations, and affected contracts;
4. type checking, linting, static analysis, or build as applicable;
5. the full suite when practical and proportionate;
6. a runtime smoke check when automated tests do not cover integration reality.

Each claim requires its own proof:

| Claim | Required proof |
|---|---|
| Regression fixed | Original failing case now passes after verified RED |
| Tests pass | Named test command exits successfully with zero failures |
| Build succeeds | Build command exits successfully |
| Types or lint are clean | Their own commands report no blocking issues |
| Requirements complete | Requirement-by-requirement inspection |
| Delegated work complete | Diff inspection plus independently rerun checks |

A linter does not prove a build; a focused test does not prove the suite; a passing suite does not prove every requirement. Never claim passing, fixed, complete, ready to commit, or ready for review from memory, earlier output, or another agent's report.

When a check fails, report the command, failure count, first actionable error, and whether it appears introduced or pre-existing; do not claim completion. When a check cannot run, state the missing dependency or environment and the specific risk left unverified.

## 10. Finish and Report

Before final response:

- Resolve or explicitly account for every task-list item.
- Inspect version-control status and the complete intended diff; confirm no unrelated user changes were modified.
- Summarize changed behavior and important file paths.
- List verification commands and their actual results.
- Verify documentation and internal links when those files changed.
- State residual risks, skipped checks, and user decisions still required.
- Do not expose secrets or dump large logs.

Verification is not integration. Do not commit, amend, push, merge, delete branches, or create a PR as part of finishing (contract §5). Present the options and let the user choose:

- keep the branch or worktree as-is;
- commit locally;
- push or open a PR;
- merge locally;
- remove or discard work. Never delete a branch, remove a worktree, or discard uncommitted work as routine cleanup.

When the user explicitly authorizes a commit:

1. Recheck status, intended diff, staged diff, and recent commit style.
2. Run fresh relevant verification before staging.
3. Stage only intended paths.
4. Scan the staged diff for secrets and generated noise.
5. Use a concise repository-style message.
6. Report the commit identifier and any remaining unstaged changes.

Do not amend unless explicitly asked. If hooks fail, fix the issue and seek authorization for the next commit action.

When the user explicitly authorizes a push or PR:

1. Inspect tracking, remotes, branch state, included commits, and the full base diff.
2. Rerun relevant checks on the final state.
3. Describe actual changes, tests, risks, and known limitations.
4. Return the remote or PR URL when available.

Never force-push unless explicitly requested and the risk is understood.

Completion means the requested outcome is implemented or answered, relevant evidence is fresh, and the report accurately states both success and limits.

When you are sure the current task is completed, clear your TODO list; otherwise continue doing your work until completion, or there exists other things that force you to stop. (Check the section "Stop Conditions")

## Bundled Assets

`prompts/` holds dispatch templates you paste into a sub-agent assignment. They are not procedures for you to follow yourself; when you do the work directly, you need none of them. `tools/` holds optional local utilities.

| Asset | What it is | Load or run it when |
|---|---|---|
| `prompts/implementer.md` | Sub-agent dispatch template | Delegating one bounded implementation task (§5) |
| `prompts/plan-reviewer.md` | Sub-agent dispatch template | An implementation plan needs independent review before execution (§4) |
| `prompts/spec-compliance-reviewer.md` | Sub-agent dispatch template | Running the requirement gate of the review order (§5) |
| `prompts/code-quality-reviewer.md` | Sub-agent dispatch template | Running the quality gate, only after the requirement gate passes (§5) |
| `tools/visual-companion/visual-companion.md` | Operating guide for the strictly local visual comparison channel | After the user agrees to visual mockups for a visual decision (§3) |
| `tools/description_generator.py` | Optional offline lint for agent tool descriptions | Auditing tool descriptions, alongside `references/tool-interface-design.md` |
| `tools/test_description_generator.py` | This skill's own regression test | Maintaining this skill; never as part of a user task |

## Supporting Reading

`references/process-rationale.md` — why these rules exist, how each gate fails when skipped, worktree isolation and Git inspection recipes, and longer worked examples. Read it when a rule's intent is unclear, when you are tempted to skip a gate, or when you need the detailed command sequences. It contains no rules of its own.

## Rules for Maintaining This Skill

This skill shall contain no external AI/API service, so that it can be faithfully executed by an AI agent in an offline environment.

This `SKILL.md` describes normative guidelines for the whole coding lifecycle. As to other files, some give detailed guidance for specific domain, some give detailed explanation on these guidelines, and some give optional pure advice/utility. Lengthy `SKILL.md` is a trade-off for better alignment; others follow the principle of progressive disclosure.
