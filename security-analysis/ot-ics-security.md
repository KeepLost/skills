# OT/ICS Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves assessing Operational Technology (OT) or Industrial
Control Systems (ICS) security — SCADA, PLC, RTU, HMI, engineering
stations. This includes: network protocol analysis, configuration audit,
or safety system review.

## Critical Safety Rules

OT environments can cause **physical harm** if disrupted. These rules
override testing convenience:

1. **Default to passive/read-only.** Prefer traffic mirroring (SPAN)
   over active scanning.
2. **Never write to PLC coils/registers** without explicit authorization.
3. **Never high-rate scan** production OT networks.
4. **Never interrupt Safety Instrumented Systems (SIS)** related paths.
5. **Stop immediately** if any action causes unexpected behavior in the
   physical process.

## Methodology

### Phase 1: Mapping and Inventory (read-only)

1. Draw Purdue model levels: L0 (field devices) → L1 (control) → L2
   (supervision) → L3 (site operations) → L4 (enterprise).
2. Inventory: PLCs, RTUs, HMIs, engineering stations, historians, jump
   hosts.
3. Map protocols and ports: Modbus TCP (502), DNP3 (20000), EtherNet/IP
   (44818), S7comm (102), BACnet (47808).
4. Identify: which devices are on the network, what firmware versions,
   what protocols are in use.

### Phase 2: Passive Analysis (read-only)

1. SPAN/mirror port → capture PCAP → analyze with Wireshark (ICS
   dissectors).
2. Parse industrial protocols: identify commands, responses, data
   exchanges.
3. Review engineering files offline: PLC programs, HMI projects,
   configuration exports.
4. Identify: default passwords, cleartext protocols, missing
   authentication, firmware vulnerabilities.

### Phase 3: Limited Active (only with explicit authorization)

1. Low-speed identification only.
2. During maintenance windows.
3. Prefer read-only function codes.
4. Every action requires evidence recording.
5. **Stop immediately and notify** if any anomaly occurs.

### Phase 4: Firmware and Patch Assessment

1. Inventory firmware versions on controllers.
2. Map to known CVEs — do not blindly apply patches.
3. Analyze firmware offline (see
   [firmware-hardware-security.md](firmware-hardware-security.md)).

## OT Security Assessment Checklist

- [ ] Authorization scope includes emergency contacts
- [ ] Active probing explicitly permitted (default: no)
- [ ] Maintenance window and rollback plan defined
- [ ] Traffic mirroring preferred over port scanning
- [ ] High-severity findings trigger immediate stop and notify
- [ ] Report distinguishes remote-exploitable vs requires-physical-access

## Tool Roles

| Role | Tools |
|---|---|
| Protocol analysis | Wireshark (ICS dissectors) |
| Asset identification | Nmap NSE (limited, low-speed) |
| Configuration audit | vendor engineering software (offline) |
| Firmware analysis | binwalk, Ghidra (offline) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Any active scanning requires explicit written authorization
  specifying the maintenance window and permitted actions.
- If a scan causes unexpected PLC behavior → stop immediately, notify
  the control engineer.
- Do not use standard web scanning tools with default parameters on OT
  devices — they are not designed for industrial protocol resilience.
- Findings that involve physical process risk → report as Critical
  immediately; do not continue testing.
