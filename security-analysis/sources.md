# Sources

> This file is not loaded during tasks. It records provenance, licenses,
> and review dates for the security reference documents.
>
> `security-analysis/` is an on-demand companion resource directory owned by
> `coding-helper`; it intentionally contains no `SKILL.md` or skill metadata.

## Source Repository

| Field | Value |
|---|---|
| Repository | `github.com/zhaoxuya520/reverse-skill` |
| Commit | `79cdde737e0bf3ce7000eb3a084d47e124d70504` |
| Date | 2026-08-04 |
| License | MIT (root), GPLv3 (CTF-Sandbox-Orchestrator submodule, not used) |
| Clone location | `/tmp/reverse-skill-inspect` (temporary, for audit only) |

## Audit Status

A full security audit was performed before any content was extracted.
The audit identified Critical, High, and Medium risks that led to
excluding most of the repository's operational content. Only methodology
skeletons were extracted and rewritten. No scripts, payloads, field
journals, or configuration files were copied.

## Document Provenance

| Document | Source skill(s) | What was extracted | What was excluded |
|---|---|---|---|
| `index.md` | `MASTER-ROUTING.md` | Routing table structure | Auto-writeback, evolution directives, RULES chain |
| `assessment-boundaries.md` | `ops/scope-contract.md` | Data structure, level definitions | `precedent-auth.md` authorization override, mandatory file writing |
| `evidence-and-findings.md` | `ops/evidence-finding-path.md` | Evidence → Finding → Path model, field definitions | Journal writeback requirements, anonymization automation |
| `binary-reverse-engineering.md` | `reverse-engineering/`, `ida-reverse/`, `ghidra-reverse/`, `radare2/`, `dotnet-reverse/`, `go-rust-reverse/` | Four-phase methodology, tool roles, language notes | Machine-specific configs, version numbers, auto-install, MCP automation scripts |
| `apk-mobile-security.md` | `apk-reverse/`, `mobile-reverse/` | APK/IPA analysis phases, detection layers | Machine-specific scripts, auto-rebuild-install, SSL pinning bypass commands |
| `malware-analysis.md` | `malware-analysis/` | Six-phase analysis, YARA/Sigma, IOC extraction | Sandbox upload automation, online threat intel auto-query, anti-analysis bypass techniques |
| `secure-code-audit.md` | `code-audit/` | Four-phase audit, checklist, tool roles | Bootstrap commands, tool-index dependency |
| `digital-forensics.md` | `digital-forensics/` | Preservation, timeline, artifact analysis | Case management automation |
| `protocol-reverse-engineering.md` | `protocol-reverse/` | Four-phase protocol RE, frame layout, patterns | Replay commands, key extraction automation |
| `api-security.md` | `api-security/` | Testing phases, auth/authz, GraphQL | DoS testing commands, tool installation |
| `web-application-security.md` | `pentest-tools/` (web portion) | Client-side analysis, server-side testing, session review | Payload libraries, proxy pool evasion, auto-merge |
| `supply-chain-security.md` | `supply-chain-security/` | Six-layer framework, reachability analysis, CI/CD | Tool auto-install, manifest bootstrap |
| `cloud-kubernetes-security.md` | `cloud-k8s/` | IAM, container, K8s checks | Auto-scan commands, cloud credential handling |
| `windows-ad-security.md` | `windows-ad/` | Enumeration, attack paths, AD CS | Credential extraction commands, C2 integration |
| `identity-federation-security.md` | `identity-federation/` | Protocol mapping, misconfiguration testing, token lifecycle | Account lockout testing, brute force |
| `database-security.md` | `database-security/` | Exposure, auth, config audit | Injection commands, destructive operations |
| `email-security.md` | `email-security/` | Header auth, DNS records, content analysis | Phishing simulation, sample re-sending |
| `threat-hunting.md` | `threat-hunting/` | Hunting loop, Sigma rules, validation | Production atomic testing, SIEM auto-query |
| `firmware-hardware-security.md` | `firmware-pentest/`, `hardware-security/` | FTM stages, hardware assessment | Auto-install, firmware modification commands |
| `network-wireless-security.md` | `wifi-wireless/`, `radio-sdr/` | Traffic analysis, WiFi assessment, RF analysis | Deauth commands, transmission without authorization |
| `ot-ics-security.md` | `ot-ics/` | Purdue model, passive analysis, safety rules | Active scanning commands, PLC write operations |
| `llm-ai-security.md` | `llm-security/` | Defensive testing framework, OWASP LLM Top 10 | `agent-obedience-engineering.md` (entirely excluded), attack payload examples, prompt extraction strings |
| `browser-extension-security.md` | `browser-extension-reverse/` | Manifest analysis, content script review, risk signals | CDP automation, MCP integration |
| `macos-security.md` | `macos-reverse/` | Mach-O analysis, codesign, TCC, dynamic analysis | Machine-specific tool versions |
| `thick-client-security.md` | `thick-client/` | Boundary mapping, local/network attack surface, RE routing | DLL injection commands, credential extraction |
| `patch-diff-vulnerability.md` | `binary-diff/`, `patch-diff-exploit/` | Symbol migration, patch analysis, vulnerability inference | Weaponized PoC development, exploit code |
| `tool-catalog.md` | All skills + `bootstrap-manifest.json` + audit findings | Tool names, roles, capabilities | Installation commands, auto-execution, excluded tools' dangerous features |

## Review and Maintenance

| Field | Value |
|---|---|
| Last review date | 2026-08-05 |
| Reviewer | Initial creation |
| Next review trigger | When source repository updates, when new security domains are needed, when tool landscape changes significantly |
| Maintenance rule | Update `sources.md` when any topic document is modified. Record what changed and why. Do not modify documents without updating provenance. |

## License Compliance

The source repository is MIT licensed. The extracted and rewritten
documents in this reference set are original works derived from the
methodology structures of the source. No verbatim text was copied. The
MIT license permits use, modification, and distribution with attribution.

Attribution: Methodology structures adapted from
`github.com/zhaoxuya520/reverse-skill` (MIT license).
