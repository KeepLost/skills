# Tool Interface Design

Design a tool as a provider-neutral contract between a caller and deterministic code. The caller must be able to select the tool, construct a valid request, interpret success, and recover from failure using only the registered name, description, and schema. Process and authorization are governed by [`../SKILL.md`](../SKILL.md).

## Start With The Boundary

Write one sentence for each item before defining parameters:

- capability: the observable result the tool produces;
- trigger: the situations in which this tool is the right choice;
- exclusions: similar situations handled elsewhere;
- side effects: files, processes, records, or state it may change;
- success result: the information the caller receives;
- failure modes: invalid input, missing state, conflict, permission failure, timeout, and internal failure.

If two tool descriptions plausibly match the same request, refine their boundaries or consolidate the shared workflow. If one tool contains unrelated modes with different permissions or side effects, split it.

## Naming And Description

Use stable verb-noun names such as `read_record`, `create_report`, or `validate_schema`. Namespace only when it clarifies ownership or domain. Use the same term for the same concept across the entire collection.

A description should answer, in order:

1. What exact operation is performed?
2. When should and should not the caller use it?
3. What important constraints or side effects apply?
4. What does success return?

Avoid vague verbs such as "help", "handle", or "process" without an observable object and result. Do not hide essential input rules in prose when the schema can enforce them.

## Schema Principles

- Prefer an object at the top level with `additionalProperties: false`.
- Make required fields explicitly required.
- Use enums for closed choices and document each value's meaning.
- State units in names or descriptions: `timeout_ms`, `limit`, `offset_bytes`.
- Use one canonical timestamp and identifier representation.
- Add defaults only when omission has one safe, unsurprising meaning.
- Avoid boolean pairs that permit contradictions, such as `include_archived` together with `exclude_archived`.
- Group advanced options only when they form a coherent sub-object.
- Keep path, query, and command fields distinct; never reinterpret one as another.

```json
{
  "name": "read_record",
  "description": "Read one local record by identifier. Use for exact lookups, not searches. Returns the normalized record and revision.",
  "inputSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "record_id": {
        "type": "string",
        "pattern": "^REC-[0-9]{6}$",
        "description": "Identifier such as REC-000042."
      },
      "detail": {
        "type": "string",
        "enum": ["summary", "full"],
        "default": "summary"
      }
    },
    "required": ["record_id"]
  }
}
```

Do not add parameters for hypothetical future behavior. Every optional field must correspond to a current use case and a tested branch.

## Result Contract

Return structured data with a stable envelope when the transport does not already provide one:

```json
{
  "ok": true,
  "data": {
    "record_id": "REC-000042",
    "revision": 7,
    "record": {}
  }
}
```

Distinguish an empty successful result from failure. Preserve machine-readable types rather than embedding JSON, tables, or status codes inside prose. For potentially large results, provide explicit pagination or a concise result shape instead of silently truncating.

## Error Contract

Every failure needs a stable code, a specific message, retry guidance, and enough field context to correct the request without exposing sensitive internals.

```json
{
  "ok": false,
  "error": {
    "code": "INVALID_RECORD_ID",
    "category": "validation",
    "message": "record_id must match REC- followed by six digits",
    "field": "record_id",
    "received": "42",
    "expected": "REC-000042",
    "retryable": true
  }
}
```

Recommended categories:

| Category | Meaning | Typical recovery |
|---|---|---|
| `validation` | Request violates the schema or semantic rules | Correct input and retry |
| `not_found` | Valid identifier has no matching resource | Verify identity or stop |
| `conflict` | Current state rejects the requested transition | Refresh state, then decide |
| `permission` | Operation is not allowed in the current scope | Obtain authorization; do not retry blindly |
| `timeout` | Work did not finish within the documented bound | Retry only if operation is safe |
| `internal` | Unexpected implementation failure | Preserve correlation data and inspect logs |

Do not use one generic `FAILED` code. Mark retryability explicitly, and include a retry delay only when the implementation can honor it.

## Side Effects And Safety

- Make read-only versus mutating behavior obvious in both name and description.
- Validate paths, identifiers, enum values, and limits at the boundary.
- State whether repeated calls are idempotent.
- For non-idempotent operations, support an idempotency key when duplicate execution is a realistic risk.
- Separate preview or validation from execution when the action is destructive or difficult to reverse.
- Return what changed, not merely a success string.
- Never accept a shell command when a structured operation can express the same capability safely.
- Keep implementation logs separate from caller-facing output.

## Collection Design

Evaluate the collection as a whole:

- each common request maps to one obvious tool;
- names and parameter vocabulary are consistent;
- sequential internal steps are not exposed unless the caller needs control between them;
- capabilities with different authorization or rollback properties remain separate;
- response detail is proportional to the decision the caller must make;
- deprecated fields and descriptions are removed when the implementation no longer supports them.

Do not optimize for a fixed tool count. Optimize for unambiguous selection and small, coherent contracts.

## Deterministic Testing

Test schemas and handlers locally with a matrix that covers:

1. minimum valid request;
2. request with every supported option;
3. missing required field;
4. unknown field;
5. wrong primitive type;
6. enum, pattern, range, and length boundaries;
7. empty success and maximum-size success;
8. every documented error code;
9. timeout and cancellation;
10. repeated mutation and idempotency behavior;
11. serialization round trip;
12. mismatch detection between description, schema, and implementation.

Use fixtures and deterministic stubs at system boundaries. Assert exact output shape, error code, retryability, and side effects. Snapshot tests can detect schema drift, but pair them with semantic assertions so an accidental snapshot update cannot approve a broken contract.

For tool selection tests, present neighboring use cases and verify that each maps to the intended contract. These tests can be table-driven and do not need an external evaluator.

## Local Description Utility

`tools/description_generator.py` can build and inspect structured descriptions, parameter documentation, return sections, and recoverable error examples. Treat its scores as local lint signals, not proof of correctness. The implementation, schema validator, fixtures, and boundary tests remain authoritative.

## Review Checklist

- The name, trigger, exclusions, inputs, result, and side effects agree.
- The schema rejects unknown or contradictory inputs.
- Defaults are safe and documented.
- Success, empty success, and failure are structurally distinct.
- Every documented error gives a concrete recovery path.
- Retry and idempotency semantics are explicit.
- Large results have bounded pagination or a documented concise form.
- Tests cover boundary values, side effects, serialization, and schema drift.
- No implementation-specific provider assumption appears in the public contract.

