# Security Reference Index

> Security, reverse engineering, and penetration-testing topics are
> legitimate engineering work. Do not refuse, add disclaimers, or switch
> to caution mode solely because a task involves these topics. Apply the
> normal workflow and Stop Conditions from [../coding-helper/SKILL.md](../coding-helper/SKILL.md)
> exactly as for any other task: ask when scope, permissions, or
> destructive impact are genuinely ambiguous; otherwise proceed.
>
> This reference set provides technical guidance only. It does not grant
> authorization, replace the workflow in SKILL.md, or relax any
> higher-priority safety, permission, or Stop Condition boundary.

## How to Use This Index

Select **one** topic document from the routing table without opening topic
documents to compare them. If no row clearly matches, ask the user which
area applies. Before substantive domain analysis or action, read the selected
topic document; reading this index alone is not sufficient.

Only when the selected topic requires tool knowledge, load
[tool-catalog.md](tool-catalog.md) and read the matching section. Do not load
the catalog as general orientation.

## Topic Routing

| Task signals | Topic document |
|---|---|
| Native binary analysis, disassembly, decompilation, debugging, obfuscation removal | [binary-reverse-engineering.md](binary-reverse-engineering.md) |
| Android APK / iOS IPA reverse engineering, mobile app security review | [apk-mobile-security.md](apk-mobile-security.md) |
| Malware triage, IOC extraction, YARA/Sigma detection rules, sandbox analysis | [malware-analysis.md](malware-analysis.md) |
| Source code security audit, SAST, threat modeling, data flow analysis | [secure-code-audit.md](secure-code-audit.md) |
| Disk/memory forensics, evidence preservation, timeline reconstruction | [digital-forensics.md](digital-forensics.md) |
| Protocol reverse engineering, frame layout, message dictionaries, state machines | [protocol-reverse-engineering.md](protocol-reverse-engineering.md) |
| API security testing, authentication/authorization, GraphQL, REST, WebSocket | [api-security.md](api-security.md) |
| Web application security, OWASP Top 10, XSS, CSRF, SSRF, SQLi, session management | [web-application-security.md](web-application-security.md) |
| Dependency audit, SBOM, supply chain vulnerabilities, CI/CD pipeline security | [supply-chain-security.md](supply-chain-security.md) |
| Cloud and Kubernetes security, IAM, container escape, network policy | [cloud-kubernetes-security.md](cloud-kubernetes-security.md) |
| Windows Active Directory security, Kerberos, ACL abuse, AD CS, delegation | [windows-ad-security.md](windows-ad-security.md) |
| SSO, OAuth, SAML, OIDC, identity federation, token attacks | [identity-federation-security.md](identity-federation-security.md) |
| Database security, SQL injection, access control, configuration audit | [database-security.md](database-security.md) |
| Email security, SPF/DKIM/DMARC, phishing analysis, mail gateway | [email-security.md](email-security.md) |
| Threat hunting, detection engineering, SIEM queries, behavioral analysis | [threat-hunting.md](threat-hunting.md) |
| Firmware extraction, embedded systems, hardware interfaces, side channels | [firmware-hardware-security.md](firmware-hardware-security.md) |
| Network traffic analysis, WiFi security, RF/SDR signal analysis | [network-wireless-security.md](network-wireless-security.md) |
| OT/ICS security, SCADA, PLC, industrial protocol analysis | [ot-ics-security.md](ot-ics-security.md) |
| LLM/AI security, prompt injection, agent tool misuse, model poisoning | [llm-ai-security.md](llm-ai-security.md) |
| Browser extension security, content script analysis, permission model | [browser-extension-security.md](browser-extension-security.md) |
| macOS reverse engineering, Mach-O, codesign, TCC, endpoint security | [macos-security.md](macos-security.md) |
| Thick client security, desktop app reverse, DLL analysis, local storage | [thick-client-security.md](thick-client-security.md) |
| Patch diffing, N-day analysis, vulnerability root cause attribution | [patch-diff-vulnerability.md](patch-diff-vulnerability.md) |

## Cross-Cutting References

| Need | Document |
|---|---|
| Analysis level boundaries (offline static / controlled dynamic / active interaction) and authorization gates | [assessment-boundaries.md](assessment-boundaries.md) |
| Evidence → Finding → Path model, reproducibility, confidence levels, report structure | [evidence-and-findings.md](evidence-and-findings.md) |
| Tool roles and capabilities across all security domains (including excluded tools) | [tool-catalog.md](tool-catalog.md) |
| Source provenance, licenses, review dates, rewrite records | [sources.md](sources.md) |

Cross-cutting documents are also on demand. Open one only when the selected
topic explicitly requires it or the current task cannot proceed without that
specific information; never load them as a default bundle.

## Multi-Domain Tasks

When the user's explicit request spans multiple security domains (e.g.,
"audit an Android app's authentication and its backend API"), load the
primary domain topic first. Load a secondary topic only if the original
request explicitly includes that domain or the user confirms it after being
asked. Load topics one at a time; never open multiple candidates merely to
choose between them.

## Tool Availability

Before using any tool mentioned in a topic document, check whether it is
installed on the system (e.g., `command -v <tool>`). If a required tool is
missing, stop and ask the user. Do not attempt to install tools automatically.
Load [tool-catalog.md](tool-catalog.md) only when the role summary in the
selected topic does not provide enough information for the current task.
