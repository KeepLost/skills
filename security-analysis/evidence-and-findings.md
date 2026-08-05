# Evidence, Findings, and Paths

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## Core Model

Security analysis produces three layers of output, each building on the
previous:

```
Evidence  →  Finding  →  Path
(observed)   (concluded)  (connected)
```

- **Evidence** is an immutable, reproducible observation.
- **Finding** is a conclusion drawn from one or more pieces of evidence.
- **Path** is a connected sequence of findings that tells the complete
  story (attack path, call flow, or solution steps).

## Evidence

Each piece of evidence is a single observation, recorded independently.

| Field | Description |
|---|---|
| `id` | `E-001`, `E-002`, etc. |
| `title` | Short label |
| `observed_at` | Timestamp |
| `source_type` | `command` / `screenshot` / `file` / `log` / `memory` / `network` / `manual` |
| `source_ref` | File path or command identifier |
| `content_hash` | SHA-256 of the source artifact, or `n/a` |
| `repro_command` | Exact command a third party can run to reproduce, or note explaining why reproduction is limited |
| `raw_excerpt` | Sanitized excerpt of the raw output |
| `linked_workitem` | Related task ID, or `n/a` |

**Rules:**

- Every finding must reference at least one piece of evidence.
- `repro_command` must be runnable by a third party or must explicitly
  state the limitation (e.g., "requires lab environment with specific
  firmware version").
- Evidence is immutable: if an observation is corrected, create a new
  evidence item and note the supersession, do not edit the original.

## Finding

A finding is a security or reverse-engineering conclusion.

| Field | Values |
|---|---|
| `id` | `F-001`, `F-002`, etc. |
| `title` | Short label |
| `severity` | `critical` / `high` / `medium` / `low` / `info` |
| `category` | `vuln` / `misconfig` / `design` / `reverse_algo` / `bypass` / `other` |
| `status` | `candidate` / `validated` / `false_positive` / `accepted_risk` |
| `evidence_ids` | `[E-001, E-002]` (must be non-empty) |
| `location` | `file:line` / `address` / `url` / `class.method` |
| `impact` | What the issue means for users, data, or operations |
| `confidence` | `high` / `medium` / `low` |
| `repro_steps` | Numbered steps to trigger the issue |
| `remediation` | Suggested fix direction (not a full patch) |

**Rules:**

- `evidence_ids` must be non-empty.
- A finding with `status=validated` must have `confidence` of `high` or
  `medium`. A `low` confidence validated finding must note the residual
  risk explicitly.
- Distinguish `candidate` (scanner hit, unverified) from `validated`
  (manually confirmed, reproduced). Never report a candidate as validated.

## Path

A path connects findings into a narrative sequence.

| Field | Values |
|---|---|
| `id` | `P-001`, etc. |
| `title` | Short label |
| `path_type` | `attack` / `callflow` / `solve` |
| `start` | Entry point |
| `goal` | End state |
| `steps` | Each step: action, evidence reference, finding reference (or none) |
| `residual_risks` | What remains unaddressed after the path |

**Path type interpretation:**

| Task context | Path meaning |
|---|---|
| Penetration testing | Attack path: initial access → escalation → goal |
| Reverse engineering | Call flow: entry → key functions → algorithm output |
| CTF / challenge | Solution steps: input → transformation → flag |

**Rules:**

- Each step may reference evidence and a finding.
- If a path claims to reach a goal (e.g., "obtained admin access"), the
  final step must reference a validated finding with supporting evidence.

## Severity Definitions

| Severity | Criteria |
|---|---|
| Critical | Data loss, security exposure, crash, or fundamentally wrong result. Immediate action required. |
| High | Likely exploitable vulnerability, missing security control, or significant design flaw. Should be fixed before release. |
| Medium | Bounded issue that increases risk or reduces defense depth but is not directly exploitable alone. |
| Low | Minor hardening or clarity improvement that does not block use. |
| Info | Observation or note with no direct security impact. |

## Confidence Levels

| Level | Criteria |
|---|---|
| High | Reproduced independently, root cause identified, impact confirmed. |
| Medium | Reproduced once, root cause likely identified, impact probable. |
| Low | Observed but not fully reproduced, or root cause uncertain. Note residual risk. |

## Report Structure

A security analysis report should contain, at minimum:

1. **Scope summary** — what was analyzed, what was excluded, and why.
2. **Evidence** — key observations, organized by finding.
3. **Findings** — each finding with its severity, status, evidence
   references, and remediation.
4. **Paths** — at least one path connecting findings into a narrative.
5. **Residual risks** — what was not tested, what remains uncertain.

## Common Pitfalls

- Treating a scanner output as a validated finding without manual
  verification. A scanner hit is a `candidate`; it becomes `validated`
  only after reproduction and impact confirmation.
- Reporting evidence without a `repro_command`. If no one else can
  reproduce the observation, its value is limited.
- Mixing observation and conclusion in the same evidence item. Evidence
  is what was seen; the finding is what it means.
- Omitting sanitization. Real targets, credentials, tokens, and internal
  paths must be redacted from evidence excerpts unless the user
  explicitly requests full output in a private context.
