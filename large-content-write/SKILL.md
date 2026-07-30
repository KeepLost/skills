---
name: large-content-write
description: Use when a tool call needs a long argument, content or command parameters disappear, the tool receives empty `{}`, a required `content`/`command` property is reported missing, or output is truncated. Provides prevention, chunking, recovery, and verification strategies for reliable large writes.
---

# Reliable Large Content Writes

## Core Principle

Treat large tool arguments as a transport risk. Keep each call small enough to inspect, retry safely, and verify independently. Prefer several bounded edits over one monolithic write or command.

The final purpose of the skill is to avoid silent truncation of large tool output. Such error most probably occurs when writing very large content to file. Any means that meet this skill's end could be considered a valid technique. Following instructions could be considered optional advise as long as you have better way. (Considering that tool name may vary in different AI agents.)

## When to Apply

Use this workflow when either risk or symptoms are present.

Risk indicators:

- A tool argument embeds a large document, diff, script, JSON object, or prompt.
- The payload is large in bytes, even if it has few lines.
- Content contains dense quoting, backticks, escapes, heredocs, or nested JSON.
- One call creates a large new file or changes many distant sections.

Failure symptoms:

- The tool receives `{}` or an expected argument is absent.
- Validation reports `missing required property`, `missing content`, or `missing command`.
- The result ends mid-file, omits sections, or differs from the submitted patch.
- Small calls work while structurally similar larger calls fail.

Do not infer a universal line limit or a single root cause. Judge risk from payload bytes, serialization complexity, tool feedback, and observed truncation.

## Prevention

1. Estimate the largest string argument before calling a tool.
2. Remove unnecessary context, repeated text, and unrelated file changes.
3. Separate independent files or sections into separate calls.
4. For manual file changes, use `apply_patch`; use `read` to inspect files.
5. Keep shell commands short and use them for execution or checks, not as the default mechanism for reading or manually constructing files.
6. Choose stable patch anchors so every chunk has a clear insertion point.

Avoid using `cat`, `head`, `tail`, or `sed` as the default file-operation workflow when `read` and `apply_patch` express the operation directly.

## Large New Files

Never begin with one giant add-file payload when the content is substantial or quoting is complex.

1. Add a small skeleton with `apply_patch`: frontmatter, imports, top-level structure, and explicit section anchors.
2. Read the skeleton to confirm its exact state.
3. Fill one coherent section per `apply_patch` call.
4. Read affected ranges after several chunks and before relying on later anchors.
5. Finish with structural and domain-specific verification.

Prefer semantic chunks such as one function or one documentation section. There is no fixed safe line count: shrink chunks when byte size, quoting complexity, or failures rise.

## Existing Files

- Read enough surrounding context to select a unique anchor.
- Patch the smallest coherent region that implements the change.
- Do not combine unrelated replacements merely to reduce call count.
- If one patch remains large, land prerequisite anchors first, then patch between them.
- Re-read after edits if later patches depend on newly added text.

## Immediate Recovery

After an empty `{}`, missing required property, or apparent truncation:

1. Stop. Do not retry the same large call shape.
2. Read the target to determine whether nothing, part, or all of the change landed.
3. Preserve valid content already present; do not overwrite it blindly.
4. Reduce payload size and complexity substantially.
5. Resume from a verified anchor with multiple small `apply_patch` calls.
6. Verify each recovery chunk before continuing.

If even a small patch fails, isolate variables: simplify quoting, reduce to one file and one hunk, and confirm the tool schema and required arguments. Report a blocker only after safe recovery paths have been attempted.

## Quoting and Base64

Base64 can avoid shell quoting and escaping problems. It does not solve payload-size limits or dropped arguments, and encoding increases payload size. Use it only when quoting is the demonstrated problem, keep encoded chunks bounded, and decode with a short command. Prefer direct `apply_patch` when content is ordinary text.

Do not hide a large document inside a heredoc, helper script, JSON string, or base64 value and assume the transport risk disappeared; the tool argument is still large.

## Verification

Verification must establish both completeness and correctness:

1. Use `read` on the beginning, chunk boundaries, and end of the file.
2. Confirm all expected sections, delimiters, and closing syntax are present.
3. Check byte or line counts only as supporting signals, not proof of correctness.
4. Run the narrowest relevant formatter, parser, compiler, or syntax check.
5. Run targeted tests, then broader tests when the change warrants them.
6. Inspect the final diff when version control is available; confirm only intended files and content changed.

For generated or exact content, compare a checksum or deterministic regeneration result. Never claim success solely because the final tool call returned without an error.

## Red Flags

- Retrying an unchanged oversized call after `{}` or a missing argument
- Treating a line count as a universal safety threshold
- Using base64 to make an already large payload larger
- Replacing a partially written file without reading it first
- Skipping end-of-file, syntax, diff, or test verification

