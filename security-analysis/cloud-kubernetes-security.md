# Cloud and Kubernetes Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves assessing security of cloud infrastructure (AWS, Azure,
GCP) or Kubernetes clusters. This includes: IAM review, container escape
assessment, network policy audit, or exposed service detection.

## Methodology

### Phase 1: Identity and Boundaries

1. Identify the current identity: cloud access keys, Kubernetes service
   account, node SSH access.
2. Define scope: single account, single cluster, single namespace — or
   broader.
3. Map the attack surface from identity outward: what can this identity
   access?

### Phase 2: Cloud Control Plane

1. **Storage**: public buckets, overly permissive ACLs, unencrypted
   volumes.
2. **Metadata service**: IMDSv1 vs IMDSv2. IMDSv1 is SSRF-exploitable
   (an SSRF vulnerability can fetch IAM credentials via
   `169.254.169.254`).
3. **IAM**: role assumption chains (PassRole), privilege escalation
   paths, unused permissions.
4. **Network**: security groups, firewall rules, exposed ports.
5. **Logging**: is CloudTrail / Azure Activity Log / GCP Audit Log
   enabled?

### Phase 3: Container Security

1. **Privileged containers**: `privileged: true` grants near-host access.
2. **Host access**: `hostPath`, `hostNetwork`, `hostPID` — any of these
   can enable container escape.
3. **Capabilities**: `SYS_ADMIN`, `NET_ADMIN`, and others grant dangerous
   privileges.
4. **Writable host paths**: if a container can write to host paths,
   escape is often possible.
5. **Image security**: base image vulnerabilities, image history
   (secrets in layers), unsigned images.

### Phase 4: Kubernetes

1. **Service account tokens**: are they auto-mounted? What permissions
   do they have? (`kubectl auth can-i --list`)
2. **RBAC**: check for `cluster-admin` bindings, wildcard permissions,
   privilege escalation roles.
3. **Admission controllers**: are PodSecurityPolicy / Pod Security
   Standards enforced?
4. **Exposed services**: Kubernetes dashboard, etcd, API server without
   authentication.
5. **Network policies**: is there a default-deny policy, or is all
   pod-to-pod traffic allowed?
6. **Secrets**: are secrets stored as environment variables (visible in
   process listing)? Are they encrypted at rest?

## Key Checks

| Area | Check | Risk |
|---|---|---|
| IMDS | IMDSv2 enforced? | SSRF → credential theft |
| RBAC | `cluster-admin` count? | Over-privileged service accounts |
| Pods | `privileged` pods? | Container escape |
| Pods | `hostPath` mounts? | Host filesystem access |
| Secrets | env var secrets? | Process listing exposure |
| Network | default allow? | Lateral movement |
| API server | anonymous auth? | Unauthenticated cluster access |
| etcd | exposed? | Cluster takeover |

## Tool Roles

| Role | Tools |
|---|---|
| Cluster interaction | kubectl |
| CIS benchmark | kube-bench, kubeaudit |
| Image/IaC scanning | trivy |
| Cloud audit | Pacu (AWS), ScoutSuite (multi-cloud) |
| Vulnerability templates | Nuclei (cloud templates) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Testing requires accessing cloud resources → confirm Level 3
  authorization. Cloud testing must be explicitly authorized; "I have an
  AWS account" is not sufficient — specify which account, which
  services, and what actions are permitted.
- Do not scan other tenants' resources in shared cloud environments.
- Do not attempt privilege escalation on production cloud accounts
  without explicit authorization.
- If container escape is achieved → note the finding; do not attempt
  lateral movement or persistence without authorization.
