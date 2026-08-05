# Firmware and Hardware Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves analyzing embedded device firmware or hardware security.
This includes: firmware extraction and analysis, UART/JTAG assessment,
or IoT device security review.

## Firmware Methodology (OWASP FTM-inspired)

### Stage 1: Information Gathering

1. Identify device: model, chipset, SDK, firmware version.
2. Search for published CVEs and security advisories.
3. Check FCC ID database for regulatory filings (reveals internal
   photos, test reports).

### Stage 2: Firmware Acquisition

1. Download from vendor website (if available).
2. Capture OTA update via proxy (if update mechanism exists).
3. Extract via UART shell (if bootlog access is available).
4. Read SPI flash directly with hardware programmer (if physical access).

### Stage 3: Firmware Analysis

1. Identify file format and header.
2. Entropy analysis: determine compressed vs encrypted regions.
   - 0.0–0.7: code, strings, uncompressed data;
   - 0.7–0.95: compressed data (gzip, lzma, squashfs);
   - 0.95–1.0: encrypted or highly compressed data.
3. String extraction and signature identification.

### Stage 4: Filesystem Extraction

1. Primary: `binwalk` for magic-based extraction.
2. Fallback: `unblob` for broader format coverage (300+ formats).
3. Filesystem-specific: `jefferson` (JFFS2), `ubi_reader` (UBI/UBIFS),
   `sasquatch` (non-standard SquashFS).
4. If encrypted: find decryption key in bootloader, dump from memory, or
   read SPI flash directly.

### Stage 5: Static Analysis

1. Scan extracted filesystem with automated tools (EMBA).
2. Manual review: hardcoded credentials, web interfaces, telnet/ssh
   configs, banner versions, busybox applets.
3. Binary analysis of key executables (see
   [binary-reverse-engineering.md](binary-reverse-engineering.md)).

### Stage 6: Emulation

1. User-mode: `qemu-*-static` + `chroot` for running individual binaries.
2. Full-system: QEMU with firmware-specific setup (Firmadyne/FAT for
   common router firmware).
3. Semi-emulated: real hardware with debug access.
4. Real hardware: most accurate but requires physical device.

### Stage 7: Dynamic Analysis

1. After emulation: attach debugger, capture network traffic, test web
   interfaces.
2. On real hardware: UART debug, JTAG debug, logic analyzer for bus
   analysis.

## Hardware Assessment

### UART

1. Find TX/RX/GND/VCC pins (look for silkscreen labels or test pads).
2. Match voltage level (1.8V, 3.3V, 5V) with a multimeter.
3. Connect USB-TTL adapter (match voltage!). Read bootlog first (read-
   only).
4. Record baud rate. Try common rates: 9600, 115200, 57600.
5. Record U-Boot interrupt key and environment variables. **Do not
   `saveenv`** without understanding the consequences.

### JTAG

1. Enumerate IDCODE via JTAG tool (J-Link, OpenOCD).
2. Check if debug access is locked.
3. If unlocked: read flash, dump firmware, attach debugger.
4. If locked: document as a finding (locked JTAG is a security measure).

### SPI Flash

1. Use flashrom with CH341A programmer (or similar).
2. **Dump entire flash before any modification** — required for recovery.
3. Verify dump hash.
4. Hand off to firmware analysis (Stages 3-5 above).

## Tool Roles

| Role | Tools |
|---|---|
| Firmware extraction | binwalk, unblob |
| Filesystem tools | jefferson, ubi_reader, sasquatch |
| Firmware analysis | EMBA |
| Emulation | QEMU, Firmadyne, FAT |
| Fuzzing | AFL++ (QEMU mode), boofuzz |
| SPI flash | flashrom, CH341A |
| UART | picocom, USB-TTL adapter |
| JTAG | J-Link, OpenOCD, bus pirate |
| Debugging | gdb-multiarch |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Hardware modification risks bricking the device → dump full flash
  first; confirm the user accepts the risk.
- UART access reveals a root shell → note as finding; do not modify
  configuration without authorization.
- Firmware emulation requires network access → use lab-only network; do
  not connect emulated firmware to production networks.
- JTAG is locked → document as a security control; do not attempt
  fault injection or hardware attacks without explicit authorization.
