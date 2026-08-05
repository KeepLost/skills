# Threat Hunting

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves proactively searching for threats in log data, endpoint
telemetry, or network traffic — as opposed to responding to a known
incident. This includes: writing detection rules, testing detection
coverage, or investigating suspicious patterns.

## Hunting Loop

```
Hypothesis → Query → Investigate → Detect/Dismiss → Tune → Document
```

### Phase 1: Form Hypothesis

1. State a specific, testable hypothesis (e.g., "attacker is using
   living-off-the-land binaries for lateral movement").
2. Select data sources: Sysmon events (1/3/10), Windows Security
   (4624/4648), DNS logs, proxy logs.
3. Define what evidence would confirm or refute the hypothesis.

### Phase 2: Query and Triage

1. Establish baseline: what does normal look like? (e.g., normal admin
   login times, normal PowerShell usage).
2. Query for anomalies: new service creation, encoded PowerShell, unusual
   outbound connections, first-time seen processes.
3. Stack rank: sort by frequency, investigate the rarest events first.
4. Correlate: same account on multiple hosts in short time; same process
   across multiple endpoints.

### Phase 3: Rule Creation

1. Convert confirmed detections into Sigma rules.
2. Define: log source, detection fields, condition logic.
3. Note false positive potential and required tuning.
4. Map to MITRE ATT&CK technique.

### Phase 4: Validate

1. Test rule against historical logs — does it find known incidents?
2. Test against benign traffic — does it produce false positives?
3. Run atomic tests in a lab environment (authorized only) to generate
   matching telemetry.

## Tool Roles

| Role | Tools |
|---|---|
| SIEM queries | Splunk, ELK, custom SQL |
| Detection rules | Sigma, sigmac |
| Endpoint queries | osquery |
| Pattern matching | YARA |
| Detection validation | Atomic Red Team (lab only) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Hunting requires querying production SIEM → confirm read access is
  authorized.
- Atomic testing (generating attack telemetry) → only in authorized lab
  environments, never on production.
- A hunt confirms a live intrusion → report it immediately. Load
  [digital-forensics.md](digital-forensics.md) only if incident response is
  explicitly in scope; otherwise ask before opening the additional topic.
