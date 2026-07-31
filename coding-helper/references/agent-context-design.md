# Agent Context Design

Domain knowledge for building or debugging the context layer of an agent system: what an agent is shown, how it is retrieved, what is retained, what is compressed, and what is externalized to files. It applies whether the agent under design is a product you are shipping or the session you are currently running in.

Everything here is technical guidance: design properties to aim for, never permissions. Process, routing, delegation, verification depth, completion, and authorization are governed by [`../SKILL.md`](../SKILL.md) — including when this material is applied to your own session. This file defines no workflow of its own.

Related: [`tool-interface-design.md`](tool-interface-design.md) for the tool contracts that appear in an agent's context.

## Working Model

Context is all state presented to an agent for one inference: instructions, tool definitions, retrieved material, conversation history, and tool observations. Treat it as a finite attention budget, not an archive.

The target is not minimum size. Optimize for signal density: the smallest working set that preserves correct decisions, exact constraints, and reliable continuation.

| Component | Design questions | Stable practice |
|---|---|---|
| Instructions | Are goals, constraints, and precedence explicit? | Clear sections, consistent instruction altitude |
| Tool definitions | Is each one distinguishable from its neighbors? | Remove overlap; keep stable definitions byte-stable |
| Retrieved material | Is every loaded section needed now and current? | Retrieve just in time at semantic boundaries |
| History | Which turns still affect an unresolved decision? | Retain active state; retire resolved exploration |
| Observations | Is exact output still needed, or only its result? | Keep exact active evidence; reference resolved bulk |

Instruction altitude matters: rules specific enough to be actionable, general enough to survive small changes in the task. Rules that restate the model's defaults add tokens without changing behavior.

## Scope Boundary

Not every use of a file is context engineering. Reading source, editing config, or writing a requested document is ordinary work. This material applies when a file or message is intentionally serving as agent state, context overflow, retrieval index, or continuity mechanism.

A long prompt or large history is not itself a defect. Intervene when it causes a measured problem in quality, continuity, cost, latency, or capacity.

## Diagnosis

Compare the failing case with a short, clean control using the same objective, tools, and expected result. Record context composition and the earliest point where behavior diverges. One weak response proves nothing; look for a repeatable relationship between context and failure.

Work this table top to bottom. Later remedies can hide earlier causes: compressing history will mask a poisoned claim without removing it. Stop at the first well-supported cause and record plausible secondary causes. Remedies live in Section "Intervention Selection" below; this table only separates causes.

| Cause | Distinguishing evidence |
|---|---|
| Non-context defect | Clean control also fails |
| Missing context | Required information is absent from all available state |
| Poisoning | A false or stale claim has downstream dependents |
| Clash | Applicable sources disagree without precedence |
| Confusion | Constraints from another task or workstream leak in |
| Distraction | Removing irrelevant content restores behavior |
| Under-retrieval | Relevant source exists but the returned section is insufficient |
| Buried context | Exact required content is loaded but consistently overlooked |
| Accumulation | Stale history or observations correlate with decline |

A non-context defect is not a context problem: repair task framing, data, permissions, or tools instead.

Symptom notes: guessing and repeated rediscovery point to missing context. Errors that survive correction point to poisoning. Wrong-goal answers and inappropriate tool choices are stronger confusion signals than mere irrelevance.

Frequent misdiagnoses:

- Prompt ambiguity read as long-context degradation
- Tool failure read as missing context
- Stale retrieval read as model hallucination
- Intentional task switching read as confusion
- Large but relevant evidence read as distraction
- Normal code navigation read as filesystem context management

### Claim Provenance And Conflicts

For each consequential claim, track:

- the exact claim and whether it is fact, decision, assumption, or inference;
- its source location and version or timestamp;
- the downstream decisions relying on it;
- its verification and conflict status.

Corrections must replace bad claims, not sit beside them. When dependents cannot be audited safely, return to the last verified state.

For a conflict: state the claims without blending them, identify each source's scope, version, and authority, apply the precedence rule supplied by the task or owner, and remove superseded material from the working set. When precedence is unknown, leave the decision unresolved and surface it rather than silently picking a side; for your own work, that is a Stop Condition in [`../SKILL.md`](../SKILL.md).

## Intervention Selection

Prefer reversible selection over lossy transformation, in the order given under Optimization below. Change one major context variable at a time and keep a reversible baseline.

Rows join to the diagnosis table by cause name. `Non-context defect` has no row here because it is not a context problem; `Cost or latency only` has no diagnosis row because it is a pressure rather than a defect.

| Diagnosed cause | First intervention | Escalation |
|---|---|---|
| Missing context | Retrieve or persist the missing item | Add a discoverable index and refresh rule |
| Poisoning | Remove the bad claim and dependent conclusions | Rebuild from the last verified state |
| Clash | Declare source precedence and applicable version | Split incompatible contexts |
| Confusion | Restate the active task and isolate workstreams | Start a clean task context |
| Distraction | Remove irrelevant blocks and mask resolved output | Tighten retrieval filters |
| Under-retrieval | Improve names, sections, query scope, or chunk boundaries | Add a compact local index |
| Buried context | Promote a concise task frame and explicit anchors | Split the material into focused loads |
| Accumulation | Mask resolved output, offload retrievable bulk, then compress | Partition independent work |
| Cost or latency only | Stabilize reusable prefixes and reduce repeated payloads | Apply selective offloading or compression |

## Context Assembly

Keep stable instructions clear and internally consistent. Place volatile facts separately so an update does not invalidate stable material or leave a stale mixed section.

Use progressive disclosure: keep identifiers and summaries in active context, then load full sections only when the current decision needs them. Split documents at semantic boundaries — headings, records, complete procedures — not arbitrary offsets.

Tool definitions are part of the assembled context, so overlapping tools create ambiguity even when their token cost is small. For what a tool description must distinguish, see [`tool-interface-design.md`](tool-interface-design.md).

## Optimization

Once a cause is diagnosed and an intervention chosen, these are the mechanisms that implement it, cheapest and most reversible first.

### Least-Lossy Order

Use the least lossy measure that addresses the measured bottleneck:

1. Remove duplicates, boilerplate, and no-longer-applicable instructions.
2. Narrow retrieval to complete, relevant sections.
3. Stabilize reusable prompt prefixes.
4. Mask resolved observations while keeping references.
5. Offload large retrievable material to external state.
6. Compress retired history with explicit preservation fields.
7. Partition independent work when isolation benefits exceed coordination cost.

Do not build optimization machinery without a demonstrated capacity, quality, latency, or cost problem.

### Prefix Stability

Place stable instructions and tool definitions before changing task data. Keep timestamps, request identifiers, and changing status outside reusable prefixes. Where caching depends on byte-stable input, a formatting change is an operational change.

Prefix stability is an efficiency measure, never a reason to retain obsolete instructions. Correctness and freshness win over cache reuse.

### Observation Masking

Mask an observation only after its relevant result is extracted and the full content stays retrievable if later work may need it.

Keep exact observations that contain active error messages or stack traces, evidence for an unresolved decision, user-provided constraints or approvals, structured values whose exact form matters, or the latest result in an active reasoning chain.

Mask duplicate output, repeated headers, completed search listings, and resolved logs first. A useful replacement names the source, key result, storage location, and freshness.

### Retrieval Control

Use exact names and structural search for known identifiers; use conceptual search when terminology is uncertain. Locate first, inspect size, then load — applying the semantic-unit rule from Context Assembly above.

If retrieval is broad, improve scope before summarizing the result. If retrieval is narrow but incomplete, fix chunk boundaries or add neighboring context. Track whether loaded material actually contributes to an answer or decision.

### Budgeting

Inventory context by category instead of watching a single total. Reserve room for the current request, tool results, error recovery, and final output. Act when growth threatens that reserve or representative quality declines, not at a universal percentage.

| Dominant pressure | Preferred action |
|---|---|
| Repeated stable prefix | Improve prefix stability |
| Verbose tool observations | Mask or offload resolved output |
| Retrieved documents | Narrow retrieval or partition sources |
| Old conversation state | Mask resolved output, offload bulk, then compress |
| Independent workstreams | Isolate contexts and exchange compact artifacts |

### Partitioning

Partition along clear ownership and output boundaries. The context-specific design property is what crosses the boundary: a coordinator should receive conclusions, provenance, conflicts, and open questions, not every exploratory observation. That asymmetry is the point of partitioning — each partition absorbs its own bulk.

Partitioning fits poorly when subtasks share rapidly changing state, need constant cross-checking, or cannot be validated independently.

Partitioning as a context technique is not the same decision as delegating your own work. When you delegate, §5 of [`../SKILL.md`](../SKILL.md) governs whether to delegate at all, what every assignment must contain including the required return status, and how to handle what comes back. Nothing here relaxes that.

## Compression

Compression replaces retired context with a smaller representation that still supports correct continuation. Optimize total effort to finish, including re-reading and re-derivation, not the size of the next request alone.

It sits at step 6 of the least-lossy order for a reason: compression is lossy, so pruning and offloading come first.

### Anchored Incremental Summary

Maintain one verified summary and merge only newly retired material into it. Do not regenerate the whole summary each cycle; repeated rewriting silently erases older constraints and identifiers.

Stable sections, each named as a second-level heading in the summary document, and what each must hold:

```text
Intent And Success Criteria   original task intent, definition of done
User Constraints              every still-active constraint and approval
Verified Facts And Sources    facts with provenance; not inferences
Decisions And Rationale       chosen option, alternatives considered, why
Artifacts                     read vs created vs modified, by full path
Exact Identifiers And Errors  commands, paths, signatures, error text, verbatim
Current Verification State    checks run and their latest actual outcomes
Unresolved Questions          open questions, blockers, ownership, conflicts
Failed Attempts               only those that prevent repeating dead ends
Next Actions                  the next executable step
```

Add domain-specific sections when useful, but keep section meanings stable across cycles. Exploratory narration, duplicate observations, superseded plans, and boilerplate can go once their useful result lands in one of these sections.

### Merge Rules

1. Treat the existing verified summary as an anchor, not text to paraphrase freely.
2. Add new facts with provenance; replace only explicitly superseded facts.
3. Deduplicate artifacts by full path and decisions by subject.
4. Preserve commands, paths, signatures, error text, and structured values verbatim when exactness matters.
5. Mark assumptions and unresolved conflicts; never promote them to facts.
6. Update current state and next actions after incorporating completed work.
7. Keep a retrievable source reference until the merged summary passes its probes.

## External State Lifetimes

Choose a lifetime before writing agent state.

| Class | Appropriate content | Lifetime | Required controls |
|---|---|---|---|
| Session scratch | Raw tool output, temporary notes, active plan, transient index | Current task or session | Clear owner, cleanup rule, retrievable path |
| Shared artifacts | Findings, handoffs, progress, test evidence, conflicts | Shared workflow | Ownership, schema, concurrency rule, status and provenance |
| Cross-session durable memory | Stable preferences, approved decisions, reusable validated facts | Multiple sessions | Validation, source, update policy, expiry or deletion path |

Project source, tests, configuration, and requested deliverables are ordinary project artifacts. They become context state only when deliberately used to preserve, retrieve, coordinate, or restore agent working knowledge.

Do not promote temporary guesses into durable memory, and do not use durable memory as an unreviewed transcript archive.

### Session Scratch

Use scratch storage for large observations and intermediate state that would crowd active context. Keep a compact reference with path, source, purpose, creation time, and summary.

A well-formed scratch class has:

- a task- or session-scoped directory the agent owns;
- discoverable names rather than anonymous files;
- a defined cleanup owner and trigger (completion, cancellation, or expiry);
- bounded reads and targeted search for large content;
- graceful behavior when a referenced file is missing.

Scratch storage must live in a path the agent created for that purpose. Deleting anything else, including untracked files in the user's working tree, is subject to the authorization rules in [`../SKILL.md`](../SKILL.md).

Do not store secrets merely to make them retrievable. Apply the same access controls as the source data.

### Shared Artifacts

Shared state should communicate through stable schemas rather than freeform append-only notes. Give each writer an owned path, or use an explicit serialization mechanism; concurrent writes to one file risk silent corruption.

A handoff should carry objective, completed work, findings with sources, artifact changes, verification evidence, unresolved conflicts, blockers, and requested next action. Separate status from findings when their update rates differ.

A shared-artifact schema should therefore carry freshness and completion status, so a reader can tell finished findings from in-progress ones. That is a property of the schema, not a substitute for verification: when you consume a sub-agent's report, §§5 and 9 of [`../SKILL.md`](../SKILL.md) still require inspecting the diff and rerunning checks yourself.

### Cross-Session Durable Memory

Promote information only when it should outlive the session and has been validated. Each entry carries a stable key and concise value, source or approving authority, the scope where it applies, creation and last-review information, confidence or verification state, and supersession, expiry, or deletion rules.

Do not persist transient errors, speculative conclusions, temporary task state, or whole transcripts. Resolve contradictions before loading durable entries together.

### Retrieval And Lifecycle

Use meaningful paths, clear headings, and compact indexes. References must survive routine workflow changes or provide a rediscovery strategy when paths move.

Keep source material immutable when it serves as recovery evidence. Write derived summaries separately and link them to the source.

A complete state design also answers what happens when each class ends:

- which scratch output is disposable and who disposes of it;
- how a shared artifact is marked finished versus abandoned;
- what qualifies information for promotion to durable memory;
- how stale references and duplicate keys get resolved;
- who holds ownership, access, and cleanup responsibility afterward.

A design that answers only the write path leaves stale state able to pose as current truth.

Externalization succeeds only if retrieval is more selective than reloading the original context. Nothing in that lifecycle authorizes deleting or reverting state you do not own — [`../SKILL.md`](../SKILL.md) governs that, and §10 owns what finishing a task requires.

## Validation Probes

Derive expected answers from the source material before retiring it, then probe after the change. Probes test continuation quality, not context size.

| Probe | Tests |
|---|---|
| "What exact failure started this work?" | Factual retention |
| "Which artifacts changed, and how?" | Artifact trail |
| "Which constraints still govern the task?" | Instruction continuity |
| "What decision was made and why?" | Rationale retention |
| "What is the next executable step?" | Continuation |
| "Which claims remain unverified?" | Epistemic status |
| "Can a requirement be followed from a different context position?" | Placement sensitivity |

Inspect answers for unsupported additions as well as omissions, and rotate probes to cover the task's real risks. A passing subset does not prove all critical information survived. Probe failures show what was lost; they do not identify which mechanism lost it.

Beyond probes, measure task success, unnecessary re-fetching, repeated work, and the operational metric you were trying to improve. Roll back any optimization that reduces size while increasing recovery work or unsupported conclusions. Keep raw evidence until the change has passed. Prefer deterministic local checks; these comparisons need no external judge or hosted evaluator.

Probe answers are model output, not command output. They tell you whether a context design carries enough signal; they never substitute for the fresh command evidence that §9 of [`../SKILL.md`](../SKILL.md) requires for a completion claim.

## Recovery From A Bad Context

Recovery runs least-lossy first, and each step should be available by design rather than improvised:

1. revert the most recent context transformation;
2. restore exact source material from retained history or external state;
3. remove unsupported summary claims and re-establish provenance;
4. rebuild a minimal context holding current task, constraints, verified facts, artifact state, and next action;
5. then retry with a less lossy intervention.

A clean context carrying forward only independently verified state is the last resort.

Revert and restore here mean agent-owned context and state, not the user's files or version-control history. Reversing anything else follows the authorization rules in [`../SKILL.md`](../SKILL.md).

If the source cannot be recovered, mark the information unknown; never fill a gap with plausible inference. Repeated failed recovery is a signal to stop and ask rather than to keep retrying — the Stop Conditions in [`../SKILL.md`](../SKILL.md) apply.

## Context Design Review Checklist

Properties of the artifact, not steps to perform:

- Each context component has an identified owner and a reason to be present.
- Stable instructions and volatile facts are separated.
- Retrieval returns complete semantic units, addressable by name.
- Tool definitions do not overlap in purpose or trigger.
- Every persisted state item has a declared class, lifetime, and cleanup owner.
- Summaries preserve exact identifiers, commands, and error text verbatim.
- A retrievable source exists for anything a summary replaced.
- Durable memory entries carry provenance, scope, and an expiry or deletion path.
- Conflicting sources have a precedence rule rather than a blended result.
- Continuation is possible after a context reset without repeating finished work.

