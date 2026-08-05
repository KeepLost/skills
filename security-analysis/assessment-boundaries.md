# Assessment Boundaries

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## Three Analysis Levels

Every security task falls into one of three levels. The level determines
what actions are permissible and what authorization is required. When
ambiguity exists about which level applies, stop and ask the user.

### Level 1: Offline Static Analysis

**Definition:** Analysis performed on local files, copies, or artifacts
without any network interaction or live target contact.

**Typical activities:**

- disassembly, decompilation, and static reading of binaries or source;
- string extraction, entropy analysis, structure identification;
- configuration file and manifest review;
- dependency manifest and lockfile audit;
- YARA/Sigma rule authoring and testing against local samples;
- memory dump and disk image analysis (offline);
- protocol frame layout analysis from captured PCAP files.

**Authorization:** User must have the files legitimately (own system, authorized
download, CTF sample, public dataset). No target contact occurs. This is
the default level when no live target is involved.

**Stop conditions:**

- The sample is known to be live malware and analysis requires executing it
  → escalate to Level 2.
- The file originates from a system you do not have permission to access
  → stop.

### Level 2: Controlled Dynamic Analysis

**Definition:** Running or observing code in an isolated environment under
controlled conditions, with no contact to unauthorized external systems.

**Typical activities:**

- sandboxed malware execution in an isolated VM or container;
- dynamic instrumentation (Frida, gdb, lldb) on local test binaries;
- firmware emulation in QEMU with no network or lab-only network;
- automated test execution against a local or lab instance of the target;
- fuzzing in an isolated environment.

**Authorization:** User must have a controlled environment (isolated VM,
lab network, CTF sandbox). If the target is a live service, the user must
explicitly state that a test instance is available and authorized.

**Stop conditions:**

- The dynamic analysis would cause outbound network traffic to
  unauthorized hosts → stop or reconfigure to lab-only network.
- The sample attempts C2 communication → block and note as a finding; do
  not allow exfiltration.
- The environment is not actually isolated (shared host, production
  network) → stop and ask the user to provide an isolated environment.

### Level 3: Active Target Interaction

**Definition:** Sending requests, probes, or payloads to a live target
system, network, or service.

**Typical activities:**

- port scanning and service enumeration against a target;
- web application vulnerability testing (XSS, SQLi, SSRF, etc.);
- API authentication and authorization testing;
- Active Directory enumeration and path testing;
- wireless network assessment (monitoring, handshake capture);
- protocol replay against a live service.

**Authorization:** User must explicitly identify the target, the scope
(in-scope and out-of-scope assets), and the permitted activities. A
generic statement like "test this" is insufficient — the specific target,
allowed actions, and exclusions must be clear.

**Mandatory preconditions:**

- In-scope assets are explicitly listed (hosts, domains, applications,
  IP ranges).
- Out-of-scope assets are explicitly listed.
- Permitted activities are specified (e.g., "read-only recon" vs "active
  exploitation" vs "credential testing").
- Network profile is set (authorized targets only, no lateral expansion).
- Destructive actions (DoS, data deletion, persistence installation,
  lateral movement) are separately authorized or explicitly prohibited.

**Stop conditions:**

- A finding suggests impact beyond the stated scope → stop and report.
- An action would affect availability (DoS) → stop unless explicitly
  authorized.
- An action would install persistence or move laterally → stop unless
  explicitly authorized.
- Credentials are captured → handle per authorization; do not use them
  beyond the stated scope.
- The target appears to be a production system with no test window →
  stop and confirm maintenance window or dedicated test instance.

## Risk Tiering for Active Interaction

When operating at Level 3, classify each planned action before executing:

| Tier | Examples | Rule |
|---|---|---|
| Low | passive recon, reading public APIs, analyzing captured traffic | proceed |
| Medium | sending controlled HTTP requests to in-scope targets, non-destructive probing | proceed with rate limiting |
| High | fuzzing, brute-force, exploitation attempts, file upload, auth bypass, OAST callbacks | proceed only with explicit user approval for this action class |
| Critical | DoS, mass scanning, credential spraying, destructive exploitation, persistence, lateral movement, data exfiltration | do not execute without explicit per-action authorization |

## Decision Flow

```
Task involves security analysis
  │
  ├─ Is there a live target to interact with?
  │   ├─ No → Level 1 (offline static)
  │   └─ Yes → Will you send traffic/probes to it?
  │       ├─ No, just observe captured data → Level 1
  │       ├─ Yes, but in an isolated lab → Level 2
  │       └─ Yes, against the real target → Level 3
  │           └─ Check: scope defined? activities authorized?
  │               ├─ Yes → proceed, classify each action by risk tier
  │               └─ No → stop and ask user for scope + authorization
```

## What This Document Does Not Do

- It does not grant authorization. The user's explicit request defines
  scope and permissions; this document only classifies the levels.
- It does not replace SKILL.md Stop Conditions. When scope, permissions,
  or destructive impact are genuinely ambiguous, stop and ask — regardless
  of which level the task appears to be in.
- It does not define workflow steps. The primary route (Investigation,
  Bug, Design, etc.) in SKILL.md determines the workflow; this document
  helps classify the analysis boundary within that workflow.
