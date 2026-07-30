# Process Rationale

This file explains *why* the rules in `../SKILL.md` exist and how they fail when skipped. It also holds the longer command recipes that would bloat the main procedure.

It adds no process requirements. If this file and `../SKILL.md` ever appear to disagree, `../SKILL.md` is correct and this file is stale. Command recipes below illustrate rules already stated there; they do not authorize the operations shown.

## Why Route Before Acting

The classifier exists because the two common failure modes are opposites, and both come from skipping classification.

An agent that treats every request as a Direct change will patch a symptom that a Bug route would have traced to its cause, and the defect returns in a different shape. An agent that treats every request as a Design project burns the user's time workshopping a rename.

The tie-break rule (stronger evidence wins) exists because the cost is asymmetric. Running the Bug route on something that turned out to be a simple change costs additional diagnostic and regression-evidence work. Running the Direct change route on a real bug ships a fix for the wrong cause with no regression test.

Reclassification matters more than initial accuracy. Evidence found in §2 routinely reveals that "add a flag" is really "the config loader ignores overrides." Continuing under the original route because work already started is sunk-cost reasoning; the plan was written against facts that no longer hold.

## Why Depth Must Match Risk

Process ceremony is not free: it consumes user attention and agent context. Both are scarce. Ceremony spent on a typo is ceremony unavailable for the schema migration later in the session.

The reverse error is worse but less obvious. Under-processing a high-blast-radius change fails silently — the code merges, and the cost shows up as a production incident or an irreversible migration. This is why the irreversibility criterion in §3 triggers design mode on its own, independent of how clear the request seems. Clarity of request and reversibility of consequence are unrelated properties.

## Why Stop Conditions Are a Feature

An agent that never stops is not more useful; it is less trustworthy, because its confident output and its guesses look identical to the reader.

Each stop condition marks a point where continuing produces output that *looks* like progress but carries no evidence:

- **Ambiguous requirements** — you will build something. It may not be the thing requested, and the mismatch surfaces only after review effort is spent.
- **Failing baseline** — attribution breaks. You cannot distinguish a failure you introduced from one that was already there, so no verification claim you make afterward is sound. This is why §9 puts baseline establishment first.
- **Three failed fix attempts** — the count is a heuristic, not physics, but it encodes a real pattern: after three materially different failed attempts, the problem is usually in the model of the system, not in the fix. Attempt four drawn from the same wrong model fails too, and each attempt leaves residue in the diff.
- **Missing credential or service** — the alternative is a mock that proves nothing, or a hardcoded secret.
- **Unauthorized Git write** — see below.

Reporting a blocker with evidence is a complete outcome because it hands the user a decision they can actually make. Guessing past it hands them a diff they must now audit.

## Why Observed Failure Evidence Matters

When an executable test is meaningful and practical, a test written after the implementation that passes on first run proves almost nothing. It is consistent with three different worlds: the code is correct; the test does not actually exercise the code; or the behavior already existed and the change was unnecessary. You cannot tell which from a green result.

Observing the failure first eliminates the second and third worlds. That is the entire mechanism. RED is not a ritual about ordering — it is the only cheap evidence that the test has causal contact with the code.

The evidence need not be a fabricated automated test. Prose and declarative configuration may have no executable behavior, and some bugs cannot be automated in the available environment. In those cases, the runtime reproduction, parser, schema check, generated output, or nearest observable effect fills the same causal role, with the limitation stated explicitly.

This is also why the *reason* for the failure matters. A test that fails from a typo in the test file, a missing import, or an unrelated broken fixture is red for the wrong reason and eliminates nothing. When it later turns green after your fix, the transition may have been caused by anything.

The same logic drives characterization tests before a refactor. A refactor's correctness claim is "behavior is unchanged." Without tests that were green before the restructuring, there is no baseline to compare against, and "unchanged" is an assertion rather than a finding.

## Why the Test Anti-Patterns Are Prohibited

Each prohibited pattern converts a test from evidence into decoration. The suite keeps reporting green while its diagnostic value goes to zero:

- **Asserting a mock was called** tests that you wrote the call, not that the call achieves anything. It keeps passing when the real collaborator's contract changes underneath you.
- **Production APIs added for tests** make the tested path differ from the shipped path, so the test verifies a configuration nobody runs.
- **Broad snapshots for small requirements** fail on every unrelated change, which trains everyone to regenerate them without reading. After the second blind regeneration the snapshot asserts nothing.
- **Arbitrary delays** trade a deterministic failure for a slow intermittent one. The race is still there; you have only made it harder to reproduce.
- **Weakening an assertion to go green** and **editing a regression expectation to match the defect** are the most damaging, because they invert the artifact's purpose. The test now certifies the bug and will block whoever later fixes it.

## Why Minimal Fixes

Bundling cleanup with a fix destroys attribution. When the combined change is reverted, the fix is lost with it. When a new defect appears, the diff offers several plausible causes, and a reviewer must reason about the union of both changes — more work than reasoning about each separately.

The narrow-fix rule is not about diff aesthetics. It keeps each change independently revertible and independently explicable.

## Why Review Splits Into Two Gates

Requirement review and quality review fail in different directions, and merging them lets each hide the other's misses.

A single combined pass tends to collapse into whichever question the reviewer finds more interesting — usually code quality, because it is more concrete. The result is well-factored, well-tested code that implements the wrong requirement, or implements three requirements plus two nobody asked for. Extras are as much a defect as omissions: they carry maintenance cost, expand the security surface, and were never approved.

Requirement review comes first because quality findings on code that should not exist are wasted work. There is no point hardening the error paths of a feature that is about to be deleted for being out of scope.

Reading requirements *before* the implementation summary matters for the same reason RED matters. An implementation summary is a claim by the author about what they built; reading it first anchors you to their framing and you end up checking internal consistency rather than compliance.

## Why Findings Need Five Fields

A finding that omits the trigger cannot be reproduced, so it cannot be confirmed or closed. One that omits impact cannot be prioritized against other findings. One that omits file and line forces the implementer to re-derive the reviewer's search. One that prescribes a full rewrite instead of a direction takes the design decision away from the person who owns the task.

The severity tiers are decision boundaries, not descriptions of feeling. Critical and Important block integration; Minor does not. That is the only distinction the tiers need to carry, which is why the definitions are anchored to consequences (data loss, security exposure, likely regression) rather than to how serious the issue seems.

## Why Feedback Is Input, Not Authority

Reviewers work from less context than implementers. They routinely flag things that are correct given constraints they did not see. An implementer who applies every finding mechanically will introduce defects on the reviewer's authority, and the reviewer will not catch them because they now match the reviewer's model.

Verifying each claim against current code is what makes review a technical process rather than a social one. Pushing back with evidence is part of the job; silent non-compliance is not, because it leaves the reviewer believing the issue was addressed.

## Why Verification Must Be Fresh

Every claim of correctness is a claim about a specific repository state. A test result from three edits ago describes a state that no longer exists. The gap between "it passed when I ran it" and "it passes now" is exactly where regressions live, and it is invisible in the transcript because both look like a green result.

The claim-to-proof table exists because the categories are genuinely not substitutable, and conflating them is the most common false completion claim:

- A linter reads syntax and style. It never executes code, so it cannot detect a wrong result.
- A type checker proves internal consistency of declarations. Perfectly typed code computes the wrong answer without complaint.
- A focused test proves one behavior. It says nothing about the callers you changed.
- A green suite proves no *tested* behavior broke. Untested requirements are invisible to it, which is why "requirements complete" needs requirement-by-requirement inspection rather than a test run.
- Another agent's report is a claim, not evidence. It may be honest and still wrong, because the agent verified a state that no longer exists after integration.

Reporting a failure honestly, with the command and the first actionable error, costs one message. Claiming completion on stale evidence costs the user's trust in every future claim you make.

## Why Git History Is User-Owned

Code changes in the working tree are cheap to inspect and cheap to undo. Git operations are neither, and several are irreversible in practice: a force-push over a colleague's commits, a deleted branch whose reflog has expired, a `clean -fd` over uncommitted work.

There is also a social layer the agent cannot see. Commit granularity, message conventions, branch naming, and what belongs in a PR are team agreements. A commit that is technically fine can still be wrong for the project, and the repository alone does not reveal that.

This is why a plan checkpoint is not authorization. The plan was written by the same reasoning process that wants to execute it, so treating it as permission means the agent authorizes itself. Authorization has to come from outside the agent's own output.

Push and PR are separate authorizations because they have different audiences. A push moves commits to a shared remote; a PR requests human review and often triggers CI, notifications, and review obligations for other people.

## Why Isolation Sometimes Helps

A separate worktree earns its setup cost when the current checkout holds unrelated work that a failed experiment could disturb, when several efforts need distinct branches at once, or when an approved plan runs long enough that the user may want to keep working meanwhile.

It is pure overhead for a read-only task, a tiny authorized edit, or an environment already managed as an isolated worktree by an outer process.

Creating one is still a Git write, so it needs authorization like any other.

### Inspection Recipes

Read-only state inspection before edits or an authorized operation:

```bash
git status --short
git diff -- <relevant-paths>
git diff --cached
git log --oneline -10
git branch --show-current
git worktree list
```

Detecting whether you are already inside a linked worktree or a submodule, before proposing another one:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git branch --show-current
git worktree list
```

A differing `--git-dir` and `--git-common-dir` suggests a linked worktree. A superproject check prevents misclassifying a submodule. Detached HEAD may be intentional in an externally managed workspace rather than something requiring a change.

### Ignored Local Parents

Project-local worktree directories are sometimes used by repository convention. These read-only checks show whether two common parent names are ignored:

```bash
git check-ignore -q .worktrees
git check-ignore -q worktrees
```

An unignored worktree directory pollutes `git status` for everyone and invites an accidental commit of an entire second checkout. The output therefore informs any later user-owned decision about ignore rules or an external location; it does not authorize creating a worktree or editing ignore rules.

## Why Delegation Is Narrow

Delegation buys independent context, and that is its only real product. A sub-agent with a fresh window is not smarter; it is uncontaminated by the coordinator's accumulated assumptions, which is valuable precisely when those assumptions are what is wrong.

That framing explains both halves of the rule. Parallel *investigation* is nearly free because read-only work cannot conflict, and independent searchers surface findings a single agent would have anchored past. Parallel *implementation* in one checkout is expensive because two agents editing overlapping files produce a diff neither of them can explain, and reconciling it costs more than sequential work would have.

Delegating to avoid understanding the task is the anti-pattern, because the coordinator still has to review the result. If you cannot specify the objective, scope, and expected evidence, you cannot evaluate what comes back, and the delegation has only moved the misunderstanding somewhere less visible.

Passing full conversation history instead of curated context defeats the purpose outright: it reproduces the coordinator's contamination in the worker, so you pay the coordination cost and get none of the independence.

### Why Blocked Means Change Something

Retrying an unchanged prompt after a genuine blocker is the clearest possible waste: the worker reported that the inputs are insufficient, and identical inputs produce an identical outcome. The four statuses map to four different repairs because they report four different deficits — `NEEDS_CONTEXT` is missing facts, `BLOCKED` is a wrong task shape or a real external obstacle, `DONE_WITH_CONCERNS` is complete work with known risk, `DONE` is a claim awaiting verification.

## Why Task Boundaries Follow Reviewability

The rule "split where a reviewer could approve one deliverable and reject another" is a proxy for independence. If two pieces of work can receive different verdicts, they have different risk profiles and different evidence, and bundling them forces an all-or-nothing decision on things that should be decided separately.

The prohibited plan contents share one failure: they defer a decision without recording that it was deferred. "Handle errors" reads like a task but contains no decision, so the executing agent invents one silently. A signature used by task 4 but never defined in task 2 guarantees that task 4's agent either invents an incompatible one or stalls. `TBD` is at least honest, which is why it should be resolved before execution rather than carried into it.

## Reference Boundary

Domain references (`application-fullstack.md`, `mobile-android.md`, `mobile-ios.md`, `frontend-ui.md`, `graphics-shaders.md`, `tool-interface-design.md`, `bdi-modeling.md`) hold stack-specific technical knowledge, loaded only when their trigger in `../SKILL.md` §7 matches.

They deliberately contain no process rules. A rule that lives in a conditionally-loaded file is a rule that applies only when the agent happens to load that file, which makes compliance depend on retrieval luck. Anything that must always hold belongs in `../SKILL.md`.

