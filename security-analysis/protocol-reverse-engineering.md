# Protocol Reverse Engineering

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves understanding a network protocol's structure, message
format, or state machine — without documentation. This includes:
analyzing a custom binary protocol used by a client application,
understanding a proprietary IoT protocol, or reverse-engineering a
mobile app's backend communication format.

## Four-Phase Methodology

### Phase 1: Capture and Triage

1. Obtain samples: PCAP files, proxy exports (Burp/mitmproxy), client
   logs, or binary with embedded protocol code.
2. Determine direction: client→server, server→client, bidirectional.
3. Identify session structure: handshake, authentication, heartbeat,
   reconnection, data transfer, close.
4. Look for structure indicators:
   - fixed headers or magic bytes (constant first bytes);
   - length fields (usually 2 or 4 bytes before payload);
   - TLV (type-length-value) patterns;
   - delimiters;
   - compression (zlib, gzip, lz4 — detect via entropy and signatures);
   - encryption (high entropy throughout, no readable strings, no
     recognizable structure).

5. Extract payloads with `tshark`:
   ```
   tshark -r capture.pcap -T fields -e data
   ```

### Phase 2: Frame Layout Reconstruction

1. Align multiple messages of the same type. Find bytes that never
   change (headers, magic, version fields).
2. Find bytes that increment (sequence numbers, counters).
3. Locate length fields: check if the value matches the remaining payload
   size. Determine endianness. Check if the length includes the header
   itself.
4. Locate checksum/CRC/MAC fields: positions after payload, value
   changes with payload content.
5. Draw the frame layout:

   ```
   Offset  Size  Field        Description
   0       2     magic        0xDEAD (constant)
   2       1     version      0x01
   3       1     msg_type     enum: 0x01=auth, 0x02=data, ...
   4       4     length       payload length (big-endian, excludes header)
   8       2     checksum     CRC16 over bytes 0-7
   10      N     payload      message-specific
   ```

6. Build a state machine: which message types follow which?
   ```
   Connect → Auth_Request → Auth_Response → Data_Request → Data_Response → Close
   ```

### Phase 3: Serialization and Encryption

1. **Protobuf**: if fields look like varint-prefixed data, try
   `protoc --decode_raw` or `blackboxprotobuf`. Recover `.proto` schema
   from observed messages.
2. **gRPC**: HTTP/2 headers + protobuf body. Extract headers for metadata,
   body for protobuf.
3. **JSON/XML**: straightforward; look for field name obfuscation or
   nested encoding (base64 within JSON).
4. **Encryption**: if frames are high-entropy:
   - find the key exchange in the handshake (look for RSA/ECDH patterns
     in early messages);
   - find nonce/IV (usually adjacent to ciphertext, changes per message);
   - identify cipher mode (block size suggests AES; stream suggests
     ChaCha/RC4);
   - trace key derivation in the client binary (see
     [binary-reverse-engineering.md](binary-reverse-engineering.md) or
     [apk-mobile-security.md](apk-mobile-security.md) for dynamic
     extraction of encryption keys).

5. **Replay assessment**: determine whether captured messages can be
   replayed. Replay testing requires Level 3 authorization (see
   [assessment-boundaries.md](assessment-boundaries.md)).

### Phase 4: Produce Artifacts

Three deliverables are required:

1. **Message type table**: name, opcode/type, fields with offsets and
   types.
2. **Reproducible decoder**: a script or command that takes raw bytes and
   produces decoded output. Must be runnable by a third party.
3. **Evidence**: raw hex excerpts (sanitized) paired with decoded results.

## Common Protocol Patterns

| Pattern | Recognition | Analysis approach |
|---|---|---|
| Fixed header + body | First 2-4 bytes constant | Check if length field includes header |
| Magic bytes | Fixed 0xDEAD etc. at offset 0 | Use for stream re-synchronization |
| TLV | Repeating type-length-value | Type values form the message dictionary |
| Protobuf | Varint field numbers, wire types | Use `protoc --decode_raw` |
| Encrypted frames | High entropy, no readable strings | Find key exchange first, then nonce |
| Compressed payload | Recognizable header (zlib 0x78, gzip 0x1f8b) | Decompress before analysis |

## Tool Roles

| Role | Tools |
|---|---|
| PCAP parsing | tshark, Wireshark |
| Hex inspection | hexdump, xxd, ImHex, 010 Editor |
| Structure templates | Kaitai Struct, 010 Editor templates |
| Protobuf decoding | protoc, blackboxprotobuf, pbtk |
| Custom decoder | Python 3 |
| Client binary analysis | IDA, Ghidra, radare2 (for key extraction) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- The protocol is encrypted and the key cannot be extracted from the
  client binary → document the encryption scheme; the protocol structure
  above the encryption layer is still analyzable from the handshake.
- Replay testing is needed → confirm Level 3 authorization for the
  target before sending any replayed messages.
- The protocol analysis requires understanding the server-side
  implementation → this becomes a code audit task (see
  [secure-code-audit.md](secure-code-audit.md)) if source is available.
- The protocol is TLS and the issue is certificate validation → this is
  not protocol RE; check the client's TLS configuration instead.
