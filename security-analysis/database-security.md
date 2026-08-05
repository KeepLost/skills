# Database Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves assessing database security — SQL/NoSQL injection,
access control, configuration hardening, or data access audit.

## Methodology

1. **Exposure assessment**: listening address, TLS, firewall/security
   group, default ports.
2. **Authentication**: default/weak credentials, password policy, account
   lockout, role separation.
3. **Authorization**: grantee audit, sensitive table access control,
   principle of least privilege.
4. **Configuration**: dangerous features (`xp_cmdshell`, `file_priv`,
   `load_file`, `COPY TO`), audit logging enabled, encryption at rest.
5. **Injection testing**: SQL injection (authorized), NoSQL injection
   (MongoDB operators, Redis commands).
6. **Backup security**: backup access controls, encryption, retention.

**Production databases: configuration audit (read-only) is default. Do
not run injection tests or destructive statements without explicit
authorization.**

## Tool Roles

| Role | Tools |
|---|---|
| SQL injection | sqlmap (authorized targets) |
| Configuration audit | cloud RDS console, manual queries |
| Known exposure | Nuclei (database templates) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.
