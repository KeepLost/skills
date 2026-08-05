# Windows and Active Directory Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves assessing Windows or Active Directory security. This
includes: AD path analysis, Kerberos assessment, ACL abuse evaluation,
AD CS review, or Windows endpoint security audit.

## Core Principle: Graph Before Action

Enumerate and map the environment before taking any active action. Use
BloodHound to visualize attack paths. Do not start with exploitation.

## Methodology

### Step 1: Enumeration

1. SMB enumeration: shares, sessions, users.
2. BloodHound data collection: run SharpHound collector, import to
   BloodHound graph.
3. Identify key nodes: Domain Admins, Enterprise Admins, Kerberos
   service accounts, computer accounts.

### Step 2: Common Attack Paths

1. **Kerberoasting**: find service accounts with SPNs. These accounts'
   TGS tickets can be cracked offline. Risk: service account passwords
   are often weak and rarely changed.
2. **AS-REP Roasting**: find accounts with "Do not require Kerberos
   preauthentication" set. These accounts' AS-REP responses can be
   cracked offline.
3. **ACL Abuse**: identify excessive permissions:
   - `GenericAll` on a user → reset their password;
   - `GenericAll` on a group → add yourself;
   - `WriteDACL` → grant yourself any permission;
   - `WriteOwner` → take ownership and grant permissions.
4. **Delegation**:
   - Unconstrained: a service can impersonate any user to any service;
   - Constrained: a service can impersonate to specified services;
   - Resource-based constrained (RBCD): if you have
     `WriteAccountRestriction` on a computer, you can configure it to
     trust your machine.
5. **AD CS (Certificate Services)**:
   - ESC1: template with client authentication, enrollable by low-priv
     users, with SAN that can be spoofed;
   - ESC8: HTTP enrollment endpoint susceptible to NTLM relay.

### Step 3: Credential Assessment

1. Assess credential exposure: LSASS access, DPAPI secrets, browser
   stored credentials.
2. Credential extraction requires explicit authorization — never perform
   on production without approval.
3. Pass-the-Hash / Pass-the-Ticket / Golden Ticket — these are
   post-exploitation techniques requiring explicit authorization.

### Step 4: Report

1. Map all identified paths in BloodHound or as a Path (see
   [evidence-and-findings.md](evidence-and-findings.md)).
2. Rate each path by feasibility and impact.
3. Prioritize remediation: remove excessive ACLs, disable unconstrained
   delegation, fix AD CS templates, enforce Kerberos preauthentication.

## Attack Path Quick Reference

| Path | Prerequisite | Impact |
|---|---|---|
| Kerberoast | Any domain user | Offline crack of service account password |
| AS-REP Roast | Network access to DC | Offline crack of pre-auth-disabled account |
| ACL → DA | GenericAll on DA member or group | Domain Admin |
| RBCD | WriteAccountRestriction on target computer | Impersonate any user to target |
| ESC1 | Enrollable cert template with SAN | Authenticate as any user |
| NTLM Relay | LLMNR/NBT-NS poisoning + SMB signing disabled | Capture and relay authentication |

## Tool Roles

| Role | Tools |
|---|---|
| AD graph analysis | BloodHound, SharpHound |
| AD CS assessment | Certipy |
| Network enumeration | NetExec (formerly CrackMapExec) |
| Protocol operations | Impacket |
| Kerberos operations | Rubeus |
| Credential operations | Mimikatz (requires explicit authorization) |
| Coercion testing | Coercer, Responder |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- AD testing requires explicit authorization including: whether DC
  access is permitted, whether poisoning/relay is permitted, whether
  credential extraction is permitted.
- Do not perform DCSync or create Golden Tickets on production without
  explicit authorization — these are detectable and high-impact.
- Do not install persistence mechanisms without authorization.
- If a path to Domain Admin is found → report immediately; do not
  escalate without confirmation.
