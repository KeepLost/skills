# macOS Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves reverse engineering or security analysis of macOS
software — Mach-O binaries, `.app` bundles, dylibs, frameworks, or
system extensions. This includes: code signature analysis, TCC
permission assessment, or macOS malware analysis.

## Methodology

### Phase 1: Package and Signature

1. `file` — identify Mach-O type (32/64-bit, universal binary).
2. `codesign -dv --verbose=4` — code signature details: TeamID,
   entitlements, flags.
3. `spctl -a -vv` — Gatekeeper assessment.
4. `otool -L` — linked libraries and frameworks.
5. Check entitlements: `com.apple.security.*` — what sandbox
   privileges does the binary request?

### Phase 2: Static Analysis

1. Objective-C: `class-dump` or `dsdump` to export class hierarchy,
   method signatures, property declarations.
2. Swift: `swift-demangle` for symbol names. Swift symbols are less
   descriptive than ObjC selectors — rely more on string cross-
   references.
3. Disassemble/decompile: Hopper, Ghidra, or IDA (see
   [binary-reverse-engineering.md](binary-reverse-engineering.md) for
   methodology).
4. Focus areas:
   - XPC service names and interfaces;
   - TCC-protected API calls (contacts, calendar, photos, location);
   - `LC_LOAD_DYLIB` commands and rpath — dylib injection paths;
   - Hardened Runtime flags and library validation.

### Phase 3: Dynamic Analysis

1. `lldb` — native debugger (comparable to gdb).
2. Frida — dynamic instrumentation (hook ObjC methods, Swift methods,
   C functions).
3. `fs_usage` — filesystem activity monitoring.
4. `log stream` — unified logging (system and process level).
5. Network analysis: see
   [protocol-reverse-engineering.md](protocol-reverse-engineering.md)
   or use a proxy.

## macOS-Specific Security Concepts

| Concept | Description |
|---|---|
| Code signing | Required for distribution; verifies identity and integrity |
| Hardened Runtime | Prevents code injection, debug attachment, dylib loading |
| Library Validation | Only allows Apple or same-team-signed dylibs to load |
| TCC (Transparency, Consent, Control) | User-facing permission system for sensitive data |
| Sandbox | Restricts file system and network access per-app |
| Notarization | Apple's automated security scan for distributed software |
| Endpoint Security Framework | Kernel-level monitoring for security products |

## Tool Roles

| Role | Tools |
|---|---|
| Binary analysis | otool, nm, jtool2 |
| Code signing | codesign, spctl |
| ObjC class export | class-dump, dsdump |
| Disassembly | Hopper, Ghidra, IDA |
| Debugging | lldb |
| Dynamic instrumentation | Frida |
| Filesystem monitoring | fs_usage |
| Logging | log stream |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- The binary is a system extension or kernel extension → analysis
  requires elevated privileges; confirm authorization.
- Dynamic analysis requires disabling SIP (System Integrity Protection)
  → this is a significant security change; confirm the user authorizes
  it and understands the risk.
- The binary is macOS malware → follow
  [malware-analysis.md](malware-analysis.md) methodology; ensure Level 2
  isolation.
- iOS analysis → use
  [apk-mobile-security.md](apk-mobile-security.md) for iOS-specific
  methodology.
