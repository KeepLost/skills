# Network and Wireless Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves analyzing network traffic, assessing WiFi security, or
evaluating RF/SDR signals. This includes: PCAP analysis, wireless
encryption assessment, or signal identification.

## Network Traffic Analysis

1. Capture or obtain PCAP. Use SPAN/mirror ports for passive capture.
2. Extract sessions: `tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e tcp.dstport`.
3. Identify anomalous traffic: unusual ports, unexpected destinations,
   beaconing patterns, data exfiltration volumes.
4. Extract and analyze suspicious streams (see
   [protocol-reverse-engineering.md](protocol-reverse-engineering.md)).

## WiFi Security Assessment

1. Put adapter in monitor mode (authorized environment only).
2. Lock to target BSSID/channel — **never scan non-target networks**.
3. Capture handshake or PMKID (target SSID only).
4. Assess offline: password complexity, encryption type (WPA2/WPA3),
   client isolation, captive portal security.
5. Report hardening recommendations.

**Do not perform deauthentication attacks outside an authorized lab.
Do not scan or capture traffic from networks you do not own or are not
authorized to test.**

## RF/SDR Analysis

1. Default to receive-only (RX). Transmitting requires explicit
   authorization and frequency coordination.
2. Identify center frequency and modulation.
3. Analyze with GNU Radio or Universal Radio Hacker.
4. Assess: can the signal be replayed? Can commands be injected? Is
   encryption used?
5. Replay testing only in a shielded room with written authorization.

**Avoid transmitting on aviation, emergency, or other protected
frequencies. Comply with local radio regulations.**

## Tool Roles

| Role | Tools |
|---|---|
| PCAP analysis | Wireshark, tshark |
| WiFi assessment | aircrack-ng suite, hcxdumptool |
| Password assessment | hashcat (offline, on captured handshakes) |
| Signal analysis | GNU Radio, Universal Radio Hacker, Inspectrum |
| SDR hardware | RTL-SDR (RX), HackRF (RX/TX, authorized) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- WiFi assessment requires monitor mode or deauth → confirm Level 3
  authorization for the specific BSSID only.
- RF analysis requires transmitting → confirm written authorization and
  frequency coordination; default to RX-only.
- PCAP contains traffic from non-target systems → filter to in-scope
  traffic only; do not analyze out-of-scope communications.
- WiFi password cracking → only on handshakes captured from authorized
  targets; offline cracking only.
