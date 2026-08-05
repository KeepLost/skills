# Tool Catalog

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## How to Use This Catalog

This document records tools across all security domains so that you know
what exists, what each tool does, and whether it is appropriate for the
current task. Knowing a tool's role is required even when you will not
use it — understanding capabilities informs risk assessment and test
coverage decisions.

**Tool usage rules:**

1. User requests a security task + the tool is installed → use it.
2. User requests a security task + the tool is not installed → stop and
   ask the user. Do not install tools automatically.
3. Check tool availability with `command -v <tool>` before relying on it.

## Binary Reverse Engineering

### Development-Integrated (regular workflow)

| Tool | Role | Input | Output |
|---|---|---|---|
| `file` | File type identification | Binary file | Format, architecture |
| `strings` | String extraction | Binary file | ASCII/Unicode strings |
| `objdump` | Disassembly | Binary file | Assembly listing |
| `readelf` | ELF structure analysis | ELF binary | Section/symbol info |
| `nm` | Symbol listing | Binary file | Symbol table |
| `hexdump`/`xxd` | Hex inspection | Any file | Hex dump |

### Dedicated Security Tools

| Tool | Role | Notes |
|---|---|---|
| IDA Pro | Disassembly/decompilation (commercial) | Deepest cross-reference system, MCP automation |
| Ghidra | Disassembly/decompilation (free) | Strong headless/batch, good decompiler |
| radare2 / rabin2 | CLI disassembly and triage | Fastest for quick questions |
| Binary Ninja | Disassembly with IL intermediate | Good for obfuscated code |
| Hopper | macOS/iOS disassembler (commercial) | Apple platform focus |
| dnSpyEx / ILSpy | .NET decompilation | dnSpyEx has IL editor |
| de4dot | .NET deobfuscation | ConfuserEx, SmartAssembly, Babel, etc. |
| FLOSS | Obfuscated string extraction | Deobfuscates encoded strings |
| DIE (Detect It Easy) | Packer/compiler identification | `diec` for CLI |
| Frida | Dynamic instrumentation | Cross-platform (desktop, mobile) |
| gdb / lldb | Debugging | Platform-dependent |
| x64dbg | Windows debugging | GUI, plugin ecosystem |
| windbg | Windows kernel debugging | Kernel, driver, crash analysis |
| angr | Symbolic execution | Constraint solving |
| Triton | Dynamic symbolic execution | Taint analysis, DSE |
| Qiling | Cross-architecture emulation | Run binaries in emulation |
| Unicorn | CPU emulation | Lightweight, embeddable |
| Intel Pin | Dynamic binary instrumentation | Instruction-level analysis |
| D-810 | IDA deobfuscation plugin | OLLVM, Tigress, MBA simplification |
| deflat | Control flow flattening removal | Quarkslabs |
| GOOMBA | Ghidra P-Code deobfuscation | Ghidra-native |
| Miasm | Reverse engineering framework | Symbolic execution, deobfuscation |
| GoReSym | Go symbol recovery | Restores function names from pclntab |
| BinDiff | Binary diffing (IDA plugin) | Function-level matching |
| ghidriff | Binary diffing (Ghidra CLI) | Free, markdown reports |
| Diaphora | Binary diffing (IDA) | SQLite persistence |
| radiff2 | Binary diffing (radare2) | Free, embeds in r2 workflow |
| checksec | Binary security feature check | NX, PIE, RELRO, canary |
| upx | UPX unpacking | `upx -d` for decompression |

### Attack Tools (recorded, role understood, not guided for execution)

| Tool | Role | Why recorded |
|---|---|---|
| pwntools | Python exploit development framework | Understanding exploitation feasibility for severity assessment |
| Cheat Engine | Memory scanning/editing | Understanding game/memory manipulation for assessment |
| x64dbg plugins | Anti-debug bypass | Understanding anti-analysis capabilities |

## Mobile Security

### Development-Integrated

| Tool | Role |
|---|---|
| `adb` | Android Debug Bridge — device interaction |
| `otool` | macOS/iOS binary analysis (system tool) |
| `codesign` | macOS code signature verification (system tool) |

### Dedicated Security Tools

| Tool | Role |
|---|---|
| jadx | APK Java decompilation |
| apktool | APK decompile/recompile, smali editing |
| JEB Pro | Commercial ARM/Android cross-verification |
| class-dump | Objective-C class export (iOS/macOS) |
| dsdump | Swift/ObjC class export |
| frida-ios-dump | iOS App Store binary decryption |
| Objection | Frida REPL (SSL pinning bypass, keychain dump, etc.) |
| MobSF | Mobile security framework (automated SAST+DAST) |
| APKLeaks | Hardcoded secret scanner for APKs |
| jtool2 | Mach-O analysis |

## Code Audit and Supply Chain

### Development-Integrated

| Tool | Role | Languages |
|---|---|---|
| Semgrep | Multi-language SAST | 30+ languages |
| CodeQL | Semantic code analysis | JS/TS, Python, Java, Go, C/C++ |
| Bandit | Python SAST | Python |
| gosec | Go SAST | Go |
| Brakeman | Ruby on Rails SAST | Ruby |
| eslint-plugin-security | JS/TS security linting | JS/TS |
| SpotBugs + FindSecBugs | Java SAST | Java |
| osv-scanner | Dependency vulnerability scan | Multi-ecosystem |
| npm audit | Node.js dependency scan | Node.js |
| pip-audit | Python dependency scan | Python |
| trivy | Container + dependency + IaC scan | Multi-purpose |
| gitleaks | Secret scanning | Git repos |
| trufflehog | Secret scanning | Git repos, filesystem |
| cdxgen | CycloneDX SBOM generation | Multi-language |
| Syft | SPDX SBOM generation | Container, filesystem |
| hadolint | Dockerfile linting | Docker |
| Cosign | Container/artifact signing | Supply chain |
| Dependency-Track | Enterprise SCA platform | Continuous monitoring |

### Dedicated Security Tools

| Tool | Role |
|---|---|
| Snyk | Commercial SCA with reachability analysis |
| Docker Scout | Container security scanning |

## Web and API Security

### Development-Integrated

| Tool | Role |
|---|---|
| browser DevTools | Client-side analysis, network inspection |
| Postman | API testing |

### Dedicated Security Tools

| Tool | Role |
|---|---|
| Burp Suite | Web proxy, interception, repeater, intruder |
| mitmproxy | Scriptable HTTP proxy |
| ZAP | Web application scanner (OWASP) |
| Nuclei | Template-based vulnerability scanner |
| FFUF | Directory/parameter fuzzer |
| Gobuster | Directory/subdomain brute force |
| SQLMap | SQL injection automation (authorized targets only) |
| XSStrike | XSS detection |
| SSTImap | SSTI detection |
| jwt_tool | JWT analysis and testing |
| Nikto | Web server vulnerability scanner |
| httpx | HTTP probing and tech detection |
| Subfinder | Subdomain enumeration |

### Attack Tools (recorded, not guided for execution)

| Tool | Role | Why recorded |
|---|---|---|
| Metasploit | Exploitation framework | Understanding exploit availability for risk assessment |
| Hashcat | GPU hash cracking | Assessing password policy strength (offline) |
| John the Ripper | CPU hash cracking | Same as above |
| Hydra | Online brute force | Understanding attack feasibility (do not use without authorization) |

## Network, Cloud, and Infrastructure

### Development-Integrated

| Tool | Role |
|---|---|
| `kubectl` | Kubernetes cluster interaction |
| Wireshark / tshark | PCAP analysis and protocol dissection |
| `dig` / `nslookup` | DNS lookup |

### Dedicated Security Tools

| Tool | Role |
|---|---|
| Nmap | Port scanning, service identification, OS detection |
| Masscan | Large-scale fast port scanning |
| kube-bench | Kubernetes CIS benchmark |
| kubeaudit | Kubernetes configuration audit |
| Pacu | AWS security testing (authorized) |
| ScoutSuite | Multi-cloud security audit |
| aircrack-ng suite | WiFi security assessment |
| hcxdumptool | PMKID/handshake capture |
| Universal Radio Hacker | Signal analysis and decoding |
| GNU Radio | SDR signal processing |

### Attack Tools (recorded, not guided for execution)

| Tool | Role | Why recorded |
|---|---|---|
| Cobalt Strike | C2 framework | Understanding adversary capabilities |
| Sliver | C2 framework | Same |
| Havoc | C2 framework | Same |
| AdaptixC2 | C2 framework | Same |
| Impacket | Windows protocol operations (SMB/WMI/Kerberos) | Understanding AD attack paths |
| NetExec (formerly CrackMapExec) | Network service enumeration | Understanding lateral movement feasibility |
| Coercer | NTLM relay / authentication coercion | Understanding relay attack surface |
| Responder | LLMNR/NBT-NS poisoning | Understanding name resolution poisoning risks |

## Windows and Active Directory

### Dedicated Security Tools

| Tool | Role |
|---|---|
| BloodHound / SharpHound | AD attack path graph analysis |
| Certipy | AD CS vulnerability assessment (ESC1-ESC8) |
| Rubeus | Kerberos operations |
| Mimikatz | Credential extraction (requires explicit authorization) |

### Attack Tools (recorded, not guided for execution)

| Tool | Role | Why recorded |
|---|---|---|
| Mimikatz | Credential extraction, PtH, golden ticket | Understanding credential attack feasibility |
| BloodHound data | Attack path mapping | Understanding AD exposure |

## Forensics, Malware, and Detection

### Dedicated Security Tools

| Tool | Role |
|---|---|
| Volatility 3 | Memory dump analysis |
| Plaso / log2timeline | Super timeline construction |
| Timeline Explorer | Timeline analysis GUI |
| Autopsy | Disk image analysis GUI |
| Sleuth Kit | Disk image analysis CLI |
| FTK Imager | Disk imaging (Windows) |
| Eric Zimmerman tools | Windows artifact parsing (MFTECmd, EvtxECmd, etc.) |
| YARA | Pattern matching rule engine |
| Sigma / sigmac | SIEM behavior detection rules |
| pe-sieve | Process memory scanning (hook/injection detection) |
| HollowsHunter | PE dumper from running processes |
| CAPE Sandbox | Malware sandbox analysis |
| VirusTotal | Threat intelligence lookup (if network authorized) |
| MalwareBazaar | Malware sample database (if network authorized) |

### Detection Validation

| Tool | Role |
|---|---|
| Atomic Red Team | Attack simulation for detection testing (lab only) |
| osquery | Endpoint querying for threat hunting |

## LLM and AI Security

### Dedicated Security Tools

| Tool | Role |
|---|---|
| garak | LLM vulnerability probing (100+ probes) |
| PyRIT | Multi-turn attack orchestration |
| promptfoo | LLM testing and regression in CI/CD |

## Firmware and Hardware

### Dedicated Security Tools

| Tool | Role |
|---|---|
| binwalk | Firmware extraction and analysis |
| unblob | Broad-format firmware extraction (300+ formats) |
| jefferson | JFFS2 filesystem extraction |
| ubi_reader | UBI/UBIFS filesystem extraction |
| sasquatch | Non-standard SquashFS extraction |
| EMBA | Firmware automated analysis framework |
| QEMU | Firmware emulation (user-mode and full-system) |
| Firmadyne / FAT | Router firmware full-system emulation |
| AFL++ | Fuzzing (QEMU mode, persistent mode) |
| boofuzz | Network protocol fuzzing |
| flashrom | SPI flash reading/writing |
| J-Link / OpenOCD | JTAG debugging |
| USB-TTL adapter | UART serial communication |
| picocom | Serial terminal |

## Excluded Tools (recorded with reasons)

These tools were evaluated during security audit and excluded from
automatic installation or guided execution. Their roles are recorded
here so their capabilities are understood.

| Tool | Role | Exclusion reason |
|---|---|---|
| Burp MCP Full (Java HTTP service) | Burp Suite MCP bridge with 63+ tools | scopeGateEnabled/privacyStrict variables never enforced by network actions (audit H4); executable HTTP service not suitable for offline read-only skill |
| bootstrap-reverse.ps1/.sh | Auto-install security tools + write global MCP config | Writes `~/.claude/mcp.json` and `~/.codex/config.toml` without user confirmation (audit H1); unpinned npm/git installs with auto-execute (H2) |
| kali/quick-setup.sh | Kali tool installation and configuration | Root-level system changes + fixed `/tmp` file symlink risk (audit H3); overwrites user MCP config |
| case-init.ps1 | Case initialization with authorization tracking | `-AuthGranted` flag allows agent to self-set authorization status (audit C2) |
| case-guard.ps1 | Scope gate enforcement | `-Force` bypasses auth/scope/ready checks (audit M4) |
| auto-merge-journal.yml | GitHub Actions auto-merge for field journal PRs | Auto-merges PRs with regex-only filtering; `_index.md` not protected from modification (audit H5) |
| Metasploit MCP | MCP bridge to Metasploit framework | Attack tool with C2 capabilities; not appropriate for development-assistance skill |
| mcp-bridge.js (Burp) | Bridge between local Burp token and remote MCP | Can send auth token to arbitrary host via environment variable (audit M3) |
| refresh-tool-index.sh | Local tool discovery and index generation | Executes PATH-found programs to get versions (audit M5); PATH poisoning risk |
| agent-browser | Playwright browser automation MCP | npm global install, auto-downloads chromium; not needed for code-focused security review |
| anything-analyzer | Browser + HTTP capture + AI analysis MCP | Clones repo, runs `pnpm approve-builds --all`, starts hidden service (audit H2) |
| jshookmcp | JS Hook / CDP MCP | npm MCP with code execution capabilities |
| pentestswarm | AI swarm pentest MCP | Requires Go/Docker + API key; attack-oriented |
| ProxyCat | Proxy pool for IP rotation | Designed to evade rate limiting/blocking |
| Reqable MCP | Local packet capture MCP | Requires Reqable desktop app; commercial |
| update-star-history.ps1 | GitHub star history updater | Reads Git credentials (audit L2); purpose unrelated to security analysis |

## Platform Dependencies

These are not security tools but are prerequisites for many tools above.
Install via system package manager, not via skill automation.

| Dependency | Required by |
|---|---|
| Java JDK | jadx, apktool, Burp, Ghidra |
| Node.js / npm | MCP bridges, JS tooling |
| Python 3 | Most security tools (use venv, not global pip) |
| Go | Some tools (GoReSym, certipy) |
| Rust | Some tools (binwalk v3) |
