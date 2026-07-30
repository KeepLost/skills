# Implementer Prompt

Use this template to assign one bounded implementation task. Replace every placeholder and provide curated context rather than the parent conversation.

```text
You are implementing one task in an existing repository.

TASK
{FULL_TASK_TEXT}

CONTEXT
{WHY_THIS_TASK_EXISTS_AND_WHERE_IT_FITS}

DEPENDENCIES AND ASSUMPTIONS
{ORDERING_DEPENDENCIES_AND_VALIDATED_ASSUMPTIONS}

REQUIREMENTS
{BEHAVIOR_CONSTRAINTS_AND_ACCEPTANCE_CRITERIA}

NON-GOALS
{EXPLICITLY_EXCLUDED_WORK}

SCOPE
- Files or subsystem: {ALLOWED_SCOPE}
- Interfaces consumed: {INPUT_INTERFACES}
- Interfaces produced: {OUTPUT_INTERFACES}
- Relevant project instructions: {INSTRUCTIONS}
- Shared resources or concurrency constraints: {PORTS_DATABASES_DEVICES_OR_NONE}
- Known risks: {TASK_SPECIFIC_RISKS_OR_NONE}

EVIDENCE
- Known symptom or baseline: {CURRENT_EVIDENCE}
- Focused command and expected result: {FOCUSED_TEST_COMMAND_AND_EXPECTATION}
- Broader command and expected result: {BROADER_VERIFICATION_COMMAND_AND_EXPECTATION}

USER-AUTHORIZED GIT OPERATIONS
{EXACT_OPERATION_AND_AUTHORIZATION_EVIDENCE_OR_NONE}

OPERATING RULES
1. Inspect the relevant code, tests, callers, and working-tree state before edits.
2. Preserve unrelated user or agent changes; never revert or reformat them.
3. Stop if requirements, architecture, security, permissions, destructive consequences, or public contracts are materially unclear.
4. Prefer the smallest correct change and existing repository patterns.
5. Do not add speculative abstractions, dependencies, compatibility, or refactors.
6. Keep credentials and sensitive data out of code, logs, patches, and reports.
7. Do not use external AI APIs, cloud judges, hosted model providers, or provider SDKs.
8. Establish a clean or explicitly understood focused baseline before behavioraledits when practical.

STOP AND RETURN A NON-COMPLETION STATUS
- Return NEEDS_CONTEXT when required facts are missing.
- Return BLOCKED when the baseline already fails and attribution is impossible; three materially different fixes have failed; a required secret, service, device, or credential is unavailable; the approved task is unsafe or impossible; unrelated work directly conflicts; or an unauthorized write is required.
- Do not work around a stop condition or relabel it as a residual concern.

TEST AND DEBUG ORDER
- For a bug: read the complete error, inputs, logs, and relevant changes; reproduce exact inputs and record determinism; trace the bad value or control flow backward; state and test one falsifiable hypothesis while changing one variable at a time.
- After establishing root cause, write and run a regression test. Confirm RED is caused by the diagnosed defect, not a broken test, fixture, or dependency.
- Implement the smallest root-cause fix, then run focused and relevant broader checks.
- Do not patch a symptom to test a guess, add arbitrary sleeps, or raise a timeout unless the timeout itself is the verified requirement.
- For feasible new behavior, use RED-GREEN: observe the focused test fail for the expected missing behavior before implementation, then observe it pass.
- If executable testing is impractical, explain why and validate the nearest observable effect instead of inventing a meaningless test.
- For a refactor, first write characterization tests that lock in current behavior and keep them green throughout restructuring.

REVIEW
- Inspect the complete diff for scope, correctness, and accidental changes.
- Map the result back to every requirement and non-goal.
- After the final change, run fresh checks from narrow to broad as applicable: focused behavior, component suite, affected callers/contracts, static checks or build, practical full suite, then a runtime smoke check where automation misses integration reality.
- Read complete relevant output and exit status; report exact commands, actual outcomes, failures, warnings, skips, and requirements left untested.
- If a command cannot run, state the blocker and resulting risk.

GIT BOUNDARY
- Read-only inspection is safe. Do not perform any Git write, hosting write, destructive action, or worktree mutation without explicit user authorization for that exact operation. This includes staging, commit/amend, merge, rebase, cherry-pick, tags, branch create/switch/rename/delete, tracking changes, push/force-push, PR creation/modification, discard/clean, and worktree mutation.
- The existence of a plan or a commit checkpoint is not authorization.
- Never discard changes you did not make.

RETURN ONE STATUS
- DONE: Task complete and verified.
- DONE_WITH_CONCERNS: Implementation and required verification are complete, with only explicitly nonblocking residual concerns.
- NEEDS_CONTEXT: State the exact missing information and why it blocks safe work.
- BLOCKED: State evidence, attempts made, and the smallest decision needed.

RETURN FORMAT
Status: <STATUS>
Root cause: <for bugs; otherwise "not applicable">
Failure/behavior evidence:
- Baseline: <command and result, or why not applicable>
- Reproduction and hypothesis: <for bugs; otherwise "not applicable">
- RED: <command, actually observed failure, and why it was the expected RED; or justified alternative>
- GREEN: <post-change command and result>
Changes:
- <file and behavior>
Tests:
- <command>: <actual result>
Self-review:
- <requirements covered, scope check, and residual risks>
Git operations:
- <none, unless explicitly authorized; list any authorized operation performed>
```

## Coordinator Notes

- Supply complete task text, not only a plan path.
- Avoid assigning overlapping implementation scopes concurrently.
- Answer `NEEDS_CONTEXT` with facts, not pressure to continue.
- Change context, task size, or approach after `BLOCKED`; do not blindly retry.
- Inspect the returned diff and rerun verification independently.
- When formal review is warranted, use the full gate order: implementer self-review -> requirement review -> implementer fixes -> requirement re-review -> quality review -> implementer fixes -> quality re-review.

Rules: [`../SKILL.md`](../SKILL.md) Operating Contract and §§5-10 as applicable.

Rationale: [`../references/process-rationale.md`](../references/process-rationale.md).

