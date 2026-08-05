# Supply Chain Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves auditing software dependencies, CI/CD pipeline security,
container images, or SBOM management. This includes: assessing
vulnerability impact of a dependency, reviewing a Dockerfile for
security, or evaluating whether a CVE in a dependency is actually
exploitable in the project.

## Six-Layer Framework

### Layer 1: Source Code Trust

1. Evaluate upstream repository: maintainer activity, release history,
   number of contributors, known security incidents.
2. Check for typosquatting: similar package names, recently registered
   packages with similar functionality.
3. Review dependency manifest: who declared the dependency, when, and
   why (commit history).

### Layer 2: Build Pipeline

1. Check CI/CD configuration: who can modify pipelines, are secrets
   protected, are runners isolated.
2. Review third-party GitHub Actions / CI plugins: are they pinned to a
   SHA (not a mutable tag), who maintains them.
3. Check for secret scanning in pre-commit hooks and CI.
4. Verify build artifact signing: Cosign for containers, SLSA provenance
   for builds.

### Layer 3: Artifact Distribution

1. Verify checksums and signatures on downloaded artifacts.
2. Check for SBOM generation and attachment to releases.
3. Verify container image registry access controls.

### Layer 4: Runtime Protection

1. Container image scanning: OS packages + application dependencies +
   configuration.
2. Admission control: policies preventing unsigned or vulnerable images
   from deploying.
3. Runtime monitoring: unexpected network connections, file writes, or
   process executions.

### Layer 5: Continuous Monitoring

1. CVE tracking: subscribe to advisories for all dependencies.
2. Vulnerability reachability analysis: not every CVE is exploitable —
   check if the vulnerable code path is actually reachable.
3. Dependency freshness: stale dependencies accumulate risk; track
   update cadence.

### Layer 6: Incident Response

1. Have a rollback strategy for dependency updates.
2. Know which dependencies are critical vs optional.
3. Have a process for emergency patching.

## Vulnerability Assessment Workflow

### Step 1: SBOM Generation

Generate a Software Bill of Materials:

| Format | Tool | Use case |
|---|---|---|
| CycloneDX | cdxgen | Security analysis focus |
| SPDX | Syft | License compliance focus |

The SBOM should include: package names, versions, licenses, direct vs
transitive dependencies, and dependency relationships.

### Step 2: Vulnerability Scanning (SCA)

Scan the SBOM against vulnerability databases:

| Tool | Coverage | Notes |
|---|---|---|
| osv-scanner | OSV database | Free, fast, multi-ecosystem |
| Trivy | NVD + OSV + GitHub Advisory | Image + dependency + IaC |
| Dependency-Track | NVD + OSV + GitHub Advisory | Enterprise, continuous |

### Step 3: Reachability Analysis (critical)

A CVE in a dependency does not mean the project is vulnerable. Only
~15% of reported dependency vulnerabilities are actually reachable.

1. Filter: CVSS >= 7.0.
2. For each, check: is the vulnerable function/class called in the
   project's code? Use CodeQL data flow queries or manual tracing.
3. For reachable vulnerabilities: check exploitability conditions (does
   the project's usage pattern match the vulnerability's trigger?).
4. Test in an isolated environment if a PoC exists.

### Step 4: Prioritize

| Priority | Criteria | Action |
|---|---|---|
| P0 | CVSS >= 9.0 + public PoC + reachable | Fix immediately |
| P1 | CVSS >= 7.0 + PoC + reachable | Fix within current sprint |
| P2 | CVSS >= 7.0 + no PoC or not reachable | Fix in next iteration |
| P3 | CVSS < 7.0 | Routine update |

### Step 5: CI/CD Pipeline Security

1. Pre-commit: secret scanning (gitleaks, trufflehog).
2. PR checks: SAST (Semgrep), SCA (osv-scanner), license compliance.
3. Build: artifact signing (Cosign), SBOM generation and attachment.
4. Deploy: admission control (verify signature, scan image).
5. Runtime: continuous monitoring, alerting on new CVEs.

### Step 6: Container Image Security

1. Dockerfile review: base image choice (minimal), user (non-root),
   exposed ports, volume mounts, `HEALTHCHECK`, `.dockerignore`.
2. Multi-layer scanning: OS packages, application dependencies,
   configuration files, secrets in layers.
3. Image signing: Cosign sign + verify at deploy time.
4. Base image updates: track and update regularly.

## Tool Roles

| Role | Tools |
|---|---|
| SBOM generation | cdxgen, Syft, sbom-tool |
| Vulnerability scanning | osv-scanner, Trivy, Dependency-Track, Snyk |
| Reachability analysis | CodeQL, manual tracing |
| Secret scanning | gitleaks, trufflehog |
| Container scanning | Trivy, Docker Scout |
| Signing | Cosign |
| Dockerfile lint | hadolint |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- A dependency vulnerability is reported but the dependency is not in
  the project's dependency tree → false positive from SBOM generation;
  verify and dismiss.
- Reachability analysis requires running the vulnerable code → confirm
  Level 2 isolation before executing any PoC.
- Container scanning finds critical vulnerabilities in the base image
  → check if the vulnerable package is actually installed and used;
  many base image CVEs are for packages not present in the final image.
- The project has no SBOM → generate one; if generation fails, document
  the gap as a finding.
