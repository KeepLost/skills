# Digital Forensics

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves preserving and analyzing digital artifacts (disk
images, memory dumps, network captures, logs) to reconstruct what
happened on a system. This includes: incident response evidence
collection, timeline reconstruction, or analyzing what a compromised
system did.

## Core Principles

1. **Preserve first, analyze second.** Never work on the original
   evidence. Create a verified copy and work on that.
2. **Hash everything.** SHA-256 of the original before any work; SHA-256
   of the copy after creation; verify they match.
3. **Document chain of custody.** Who collected what, when, where, with
   what tools. Every transfer and access is logged.
4. **Read-only by default.** Mount images read-only. Use write blockers
   for physical media.

## Methodology

### Phase 1: Preservation

1. Calculate SHA-256 of the source artifact (disk, memory dump, PCAP).
2. Record collection metadata: timezone, acquisition command, tool
   versions, collector identity, date/time.
3. Create a working copy. Verify copy hash matches original.
4. Store the original safely; work only on the copy.
5. Begin chain-of-custody log.

### Phase 2: Memory Analysis (if memory dump available)

1. Load with Volatility 3.
2. Extract: process list, network connections, command-line arguments,
   loaded modules, injected code detection.
3. Identify suspicious processes: unusual names, unexpected parents,
   injectable memory regions, network connections to unknown hosts.
4. Dump suspicious process memory for further analysis.

### Phase 3: Host Artifacts

1. **Event logs**: Security (logon events 4624/4625/4648), PowerShell
   (script block logging 4104), Sysmon (process creation 1, network
   connection 3, file creation 11).
2. **Persistence points**: Run keys, services, scheduled tasks, WMI
   subscriptions, Startup folder, Office add-ins.
3. **Execution traces**: Amcache, Prefetch, BAM/DAM, Shimcache.
4. **File system**: recently modified files in user directories, temp
   directories, and system locations.

### Phase 4: Network Analysis

1. Load PCAP with tshark or Wireshark.
2. Extract session list: source/destination/protocol/ports.
3. Identify anomalous connections: unusual ports, unexpected destinations,
   beaconing patterns (regular intervals), data exfiltration patterns
   (large outbound transfers).
4. Extract suspicious streams for protocol analysis (see
   [protocol-reverse-engineering.md](protocol-reverse-engineering.md)).

### Phase 5: Timeline Reconstruction

1. Combine all artifacts into a single timeline: file system timestamps,
   log events, network connections, process executions.
2. Sort chronologically. Use consistent timezone (UTC recommended).
3. Identify the initial compromise event and trace forward.
4. Identify lateral movement: logons to other systems, remote execution.
5. Identify data access: which files were opened, copied, or modified.

### Phase 6: Report

Output a structured timeline with confidence levels:

| Time | Host | Artifact | Finding | Confidence | Evidence |
|---|---|---|---|---|---|
| 2024-01-15 03:22 UTC | WS-01 | Security 4624 | Logon type 10 (remote) from WS-02 | High | E-001 |
| 2024-01-15 03:25 UTC | WS-01 | Sysmon 1 | powershell.exe -enc <base64> | High | E-002 |

## Tool Roles

| Role | Tools |
|---|---|
| Memory analysis | Volatility 3 |
| Disk imaging | FTK Imager, dd, dcfldd |
| Timeline | Plaso/log2timeline, Timeline Explorer |
| Windows artifacts | Eric Zimmerman tools (MFTECmd, EvtxECmd, etc.) |
| PCAP analysis | tshark, Wireshark |
| Disk analysis | Autopsy, Sleuth Kit |
| Hash verification | sha256sum, Get-FileHash |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- The evidence source is a production system and acquisition would
  require shutdown or service interruption → stop and confirm the user
  has authorized the disruption and has a maintenance window.
- The evidence is encrypted and the key is unavailable → document the
  limitation; do not attempt to brute-force without authorization.
- Memory acquisition on a live system requires running a tool on the
  compromised host → note the risk that the tool itself may be
  compromised; consider alternative acquisition methods.
- Timeline analysis reveals potential malware → load
  [malware-analysis.md](malware-analysis.md) only if sample analysis is
  explicitly in scope; otherwise ask before opening the additional topic.
