# Secure Code Audit

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves reviewing source code for security vulnerabilities,
design flaws, or misconfigurations. This includes: auditing a codebase
before release, reviewing a pull request for security issues, or assessing
a third-party library's code quality.

## Four-Phase Methodology

### Phase 1: Scope and Threat Model

1. Identify the technology stack: languages, frameworks, runtime, database.
2. Map trust boundaries: where external input enters, where it is
   consumed, where security checks are performed.
3. Identify high-value assets: authentication, authorization, payment,
   admin interfaces, secret handling, PII storage.
4. Define audit scope: which directories, services, or PR diffs are
   in scope; what is explicitly excluded.

### Phase 2: Automated Scanning

1. Run SAST tools appropriate to the language:
   - multi-language: Semgrep, CodeQL;
   - Python: Bandit;
   - Go: gosec;
   - Java: SpotBugs + FindSecBugs;
   - JavaScript/TypeScript: eslint-plugin-security;
   - Ruby: Brakeman.
2. Run dependency vulnerability scan: `osv-scanner`, `npm audit`,
   `pip-audit`, `trivy` — see
   [supply-chain-security.md](supply-chain-security.md).
3. Run secret scanning: `gitleaks`, `trufflehog`.
4. Collect all findings as `candidate` status — do not report scanner
   output as validated vulnerabilities.

### Phase 3: Manual Verification (mandatory)

For each scanner finding, determine:

1. **Reachability**: Can external input actually reach the vulnerable
   code path? Trace from entry point to sink.
2. **Exploitability**: Given the reachability, can an attacker trigger the
   condition with realistic inputs?
3. **Impact**: What happens if the condition is triggered? Data leak,
   code execution, auth bypass, DoS?
4. **False positive**: Is the scanner matching a pattern that is actually
   safe in this context (e.g., parameterized query flagged as SQLi)?

Then manually check areas scanners commonly miss:

| Category | What to look for |
|---|---|
| Authentication | IDOR, missing auth checks, session fixation, weak password reset |
| Authorization | role escalation, missing tenant isolation, horizontal/vertical privilege issues |
| Injection | SQL, command, template, LDAP, XPath, NoSQL, header |
| Crypto | hardcoded keys, ECB mode, custom crypto, weak random, timing attacks |
| SSRF | URL fetching without allowlist, metadata endpoint access |
| Deserialization | unsafe deserializer, pickle, yaml.load, ObjectInputStream |
| File upload | path traversal in filename, unrestricted types, SSRF via URL |
| Secrets | API keys in config, tokens in source, credentials in logs |
| Race conditions | TOCTOU, double-checked locking errors, file race |

### Phase 4: Report

For each validated finding, record (see
[evidence-and-findings.md](evidence-and-findings.md)):

- location (`file:line`);
- data flow (source → sink);
- proof of concept (minimal reproduction);
- severity (critical/high/medium/low);
- remediation direction (not a full patch).

## Audit Checklist

Use as a reminder, not a substitute for thinking:

- [ ] All external input entry points identified and traced.
- [ ] Authentication covers every protected endpoint.
- [ ] Authorization checks present at each privilege boundary.
- [ ] Multi-tenant data access scoped by tenant ID at query level.
- [ ] No unsafe deserialization of external data.
- [ ] No SSRF — outbound URL fetching uses an allowlist.
- [ ] Secrets not hardcoded, not logged, not in error messages.
- [ ] File uploads validated (type, size, path).
- [ ] No dangerous `exec`/`eval`/`system` with user input.
- [ ] Crypto uses standard algorithms, no custom implementations.
- [ ] Error messages do not leak internal paths or stack traces.

## Tool Roles

| Role | Tools |
|---|---|
| Multi-language SAST | Semgrep, CodeQL |
| Language-specific SAST | Bandit (Python), gosec (Go), Brakeman (Ruby), SpotBugs (Java) |
| JS/TS security | eslint-plugin-security |
| Dependency scan | osv-scanner, npm audit, pip-audit, trivy |
| Secret scan | gitleaks, trufflehog |
| Data flow analysis | CodeQL queries, manual tracing |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Source code is not available → this is a binary analysis task, switch
  to [binary-reverse-engineering.md](binary-reverse-engineering.md).
- The codebase is too large for manual review in the available time →
  prioritize by threat model: high-value assets and external input paths
  first. Document what was not reviewed.
- A finding requires runtime verification → confirm Level 2/3
  authorization before testing against a live system.
- Dependency vulnerabilities found → load
  [supply-chain-security.md](supply-chain-security.md) only if dependency
  reachability analysis is explicitly in scope; otherwise ask before opening
  the additional topic.
