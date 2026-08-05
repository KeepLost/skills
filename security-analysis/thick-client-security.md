# Thick Client Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves assessing the security of a desktop application (thick
client) — C/S architecture, Electron, Qt, .NET WinForms/WPF, or native
desktop apps. This includes: local credential storage, DLL analysis,
update channel security, or IPC assessment.

## Methodology

### Phase 1: Establish Boundaries

1. Map process tree: main process, child processes, services, drivers.
2. Identify network listeners and outbound connections.
3. Identify local sensitive paths: AppData, Keychain (macOS), DPAPI
   (Windows), registry (Windows).
4. Draw trust boundary diagram.

### Phase 2: Local Attack Surface

1. **Configuration files**: plaintext configs, hardcoded keys, debug
   switches.
2. **DLL search order** (Windows): does the app load DLLs from writable
   directories? → DLL hijacking.
3. **Local database**: file permissions, encryption, stored credentials.
4. **IPC**: named pipes, Unix sockets, local HTTP — who can connect? Is
   there authentication?
5. **Credential storage**: DPAPI (Windows), Keychain (macOS), plaintext
   files — how are credentials protected at rest?

### Phase 3: Network Attack Surface

1. System proxy support: does the app respect system proxy settings?
2. Custom TLS: does the app use its own TLS stack? Does it validate
   certificates?
3. Certificate pinning: if present, can it be bypassed? (See
   [apk-mobile-security.md](apk-mobile-security.md) for pinning bypass
   methodology — same techniques apply.)
4. Hidden admin APIs: does the client connect to endpoints not visible
   in the UI?

### Phase 4: Reverse Engineering

Use this table to identify a possible follow-on methodology. Open the linked
topic only when that analysis is explicitly in scope; otherwise ask first.

| Technology | Reference |
|---|---|
| .NET (WinForms/WPF) | [binary-reverse-engineering.md](binary-reverse-engineering.md) (.NET section) — use dnSpyEx |
| Native (C/C++) | [binary-reverse-engineering.md](binary-reverse-engineering.md) — use IDA/Ghidra |
| Electron | unpack `asar`, then JS analysis |
| Qt | [binary-reverse-engineering.md](binary-reverse-engineering.md) — native analysis |
| Java/Swing | decompile with CFR/Procyon |

## Thick Client Checklist

- [ ] Installation/removal residue and file permissions
- [ ] Auto-start entries and services
- [ ] Credential storage method (DPAPI/Keychain/plaintext)
- [ ] Update URL and signature verification
- [ ] Certificate pinning and proxy compatibility
- [ ] Hidden features or debug menus
- [ ] Local port binding (0.0.0.0 vs 127.0.0.1)
- [ ] DLL search order (Windows)
- [ ] IPC authentication

## Tool Roles

| Role | Tools |
|---|---|
| Process/file monitoring | Process Monitor, Sysinternals (Windows) |
| API monitoring | API Monitor |
| Network interception | Burp Suite, mitmproxy |
| .NET reverse | dnSpyEx, ILSpy |
| Native reverse | IDA, Ghidra |
| Electron analysis | asar unpack, DevTools |
| macOS monitoring | fs_usage, lldb |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- DLL hijacking test requires placing a DLL in a system directory →
  confirm authorization; this is a system modification.
- Network testing requires a live backend → confirm Level 3
  authorization for the backend.
- Update channel testing could break the client's update mechanism →
  confirm the user accepts this risk.
- Credential extraction from DPAPI/Keychain → confirm authorization;
  these may contain other applications' credentials.
