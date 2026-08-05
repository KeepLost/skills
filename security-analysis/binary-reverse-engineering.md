# Binary Reverse Engineering

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves analyzing a native binary (ELF, PE, Mach-O, raw firmware
blob) to understand its behavior, algorithm, or security properties —
without source code. This includes: understanding what a suspicious
dependency does, verifying a binary patch, analyzing obfuscated code, or
reverse-engineering a protocol implementation embedded in a binary.

## Four-Phase Methodology

### Phase 1: Triage (5–15 minutes)

Goal: establish what the binary is, not how it works.

1. Identify file type, architecture, and format: `file`, `rabin2 -I`.
2. Detect packing, obfuscation, or anti-analysis: entropy analysis, packer
   signatures (UPX, Themida, VMProtect).
3. Extract strings: `strings`, `rabin2 -z`, FLOSS for obfuscated strings.
4. Map imports and exports: `rabin2 -i`, `rabin2 -E`.
5. Form initial hypotheses: language, compiler, framework, purpose.

**Do not** jump to conclusions from strings alone. Strings suggest, they
do not prove.

### Phase 2: Static Analysis

Goal: locate and understand key functions without executing the binary.

1. Load into a disassembler/decompiler (IDA, Ghidra, radare2, Binary Ninja).
2. Run auto-analysis; record identified architecture, entry point, base
   address.
3. Survey: list functions, globals, strings with cross-references.
4. Locate key functions by following:
   - entry point → main → business logic;
   - string references (error messages, URLs, format strings);
   - imported API calls (crypto, network, file, registry, auth);
   - exported functions.
5. Decompile key functions; rename variables and functions; add comments.
6. Trace data flow: where does user input arrive? Where is it consumed?
   Where are security checks performed?
7. If obfuscated (OLLVM, control flow flattening), apply deobfuscation:
   identify the obfuscation type, use appropriate plugins (D-810 for IDA,
   deflat, GOOMBA for Ghidra), or trace through manually.

**Tool selection:**

- **IDA Pro**: deepest decompilation, best cross-reference system, MCP
  automation available. Commercial.
- **Ghidra**: free, strong headless/batch analysis, good decompiler.
  Use when IDA is unavailable or for CI/automated pipelines.
- **radare2**: fastest CLI triage, good for quick questions without
  loading a full GUI. Use `rabin2` for info, `r2 -A` for analysis.
- **Binary Ninja**: strong IL intermediate representation, good for
  obfuscated code analysis.

These are interchangeable backends. The methodology (survey → locate →
decompile → trace) is the same regardless of tool.

### Phase 3: Dynamic Analysis

Goal: verify static hypotheses by observing runtime behavior.

1. Set up an isolated environment (VM, container, lab network).
2. Attach a debugger (gdb, lldb, x64dbg) or instrumentation (Frida).
3. Break at key functions identified in Phase 2.
4. Observe: function arguments, return values, memory state, control flow.
5. Test one hypothesis at a time. Change one variable per run.
6. If anti-debugging is detected, work around it (hardware breakpoints,
   Frida stealth, emulation).
7. For obfuscated code: let the program compute the answer, then dump
   memory at the comparison point.

**Dynamic analysis is for verification, not guessing.** Every runtime
observation should test a specific static hypothesis.

### Phase 4: Synthesis

Goal: produce a coherent understanding and document it.

1. Summarize findings: what algorithm, what security check, what
   vulnerability, what behavior.
2. Document the call flow or data flow as a Path (see
   [evidence-and-findings.md](evidence-and-findings.md)).
3. Record evidence: addresses, decompiler output excerpts, debug session
   logs — all sanitized and reproducible.
4. Identify cross-references to other domains:
   - core logic in `.so` (Android) → [apk-mobile-security.md](apk-mobile-security.md);
   - C2 protocol → [protocol-reverse-engineering.md](protocol-reverse-engineering.md);
   - malware behavior → [malware-analysis.md](malware-analysis.md);
   - macOS-specific → [macos-security.md](macos-security.md).

## Language-Specific Notes

### .NET (managed)

Use dnSpyEx / ILSpy, not IDA. Identify with `mscoree._CorExeMain` import
or CLR metadata streams. If obfuscated, run de4dot first. Patch at IL
level, not C# level — IL patches are more reliable. See
[thick-client-security.md](thick-client-security.md) for .NET thick
clients.

### Go

Recover function names via GoReSym or IDA Go plugin. Find `runtime.main`
and `main.main` via `pclntab`. Go strings are not null-terminated — use
runtime string structures. Prioritize string-driven analysis to avoid
getting lost in runtime library code.

### Rust

Look for panic strings (`rust_begin_unwind`, crate paths) as anchors.
Generics cause code bloat — locate business logic via string cross-
references, not function listing. Async/tokio state machines require
following cross-references through `MoveNext` equivalents.

### Obfuscated Code (OLLVM)

Identify obfuscation type: control flow flattening, bogus control flow,
instruction substitution, MBA (mixed boolean arithmetic). Apply matching
deobfuscation: D-810 (IDA), deflat (Quarkslabs), GOOMBA (Ghidra P-Code),
or manual symbolic execution (angr, Triton). If deobfuscation fails, use
dynamic analysis to let the program simplify the control flow at runtime.

## Tool Roles

| Role | Tools | Notes |
|---|---|---|
| File identification | `file`, `rabin2 -I`, `diec` | Fast, no execution |
| String extraction | `strings`, `rabin2 -z`, FLOSS | FLOSS for obfuscated |
| Disassembly/decompilation | IDA Pro, Ghidra, radare2, Binary Ninja | Interchangeable backends |
| Debugging | gdb, lldb, x64dbg, windbg | Match to target platform |
| Dynamic instrumentation | Frida, Intel Pin, DynamoRIO | Frida for cross-platform |
| Emulation | Qiling, Unicorn, QEMU | For anti-analysis or cross-arch |
| Symbolic execution | angr, Triton | For constraint solving |
| Deobfuscation | D-810, deflat, GOOMBA, Miasm | Match to obfuscation type |
| Go symbol recovery | GoReSym, redress | Go-specific |
| .NET decompilation | dnSpyEx, ILSpy, de4dot | .NET-specific |
| Diff | BinDiff, Diaphora, ghidriff, radiff2 | See patch-diff-vulnerability.md |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is
insufficient for the current task.

## Stop Conditions

- The binary is live malware and analysis requires executing it → ensure
  Level 2 isolation (see
  [assessment-boundaries.md](assessment-boundaries.md)).
- The decompiler produces garbage for a critical function → try a
  different tool, then fall back to manual disassembly, then dynamic
  analysis. Do not guess from incomplete decompilation.
- Three different analysis approaches have failed to understand a
  function → stop, document what is known and unknown, and report.
- The binary requires network access to a live target to complete analysis
  → confirm Level 3 authorization before proceeding.
