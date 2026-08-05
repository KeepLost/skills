# APK and Mobile Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves reverse engineering or security review of a mobile
application — Android (APK) or iOS (IPA). This includes: understanding
an app's authentication logic, reviewing its network communication,
assessing its local data storage, or analyzing a suspicious SDK.

## Android (APK) Methodology

### Phase 1: Triage

1. Decompile: `jadx -d output app.apk` (Java layer), `apktool d app.apk`
   (smali/resources).
2. Read `AndroidManifest.xml`: package name, permissions, exported
   components, Intent filters, backup flag, debuggable flag.
3. Scan for hardcoded secrets: API keys, tokens, URLs in strings and
   resources.
4. Detect packing/hardening: 360, Tencent, Bangcle, ijiami — look for
   custom Application class, native loader, or unusual dex structure.
5. Identify native libraries: check `lib/*/` for `.so` files.

**Do not** begin patching or hooking before understanding the app's
entry points and key classes.

### Phase 2: Java/Kotlin Logic Analysis

1. Locate key classes from `jadx` output:
   - `MainActivity` / `Application` / entry classes;
   - classes matching: login, sign, encrypt, cipher, token, root,
     certificate, trust, okhttp, retrofit, webview;
   - SDK initialization classes.
2. Trace authentication flow: where credentials are collected, how they
   are transmitted, what validation occurs.
3. Trace network layer: OkHttp interceptors, Retrofit interfaces, custom
   TLS configuration, certificate pinning.
4. Trace local storage: SharedPreferences, SQLite, KeyStore usage,
   external storage writes.
5. Trace WebView: JavaScript interface exposure, URL loading, file access.

### Phase 3: Smali and Resource Layer

Use when `jadx` output is incomplete, obfuscation is heavy, or patching
is needed.

1. Switch to `apktool` output: `smali*/` directories, `res/values/strings.xml`,
   `AndroidManifest.xml`.
2. Identify patch targets: exported component flags, root detection return
   values, login validation branches, certificate verification branches.
3. Patch smali directly when needed. Rebuild with `apktool b`, align with
   `zipalign`, sign with `apksigner`.

### Phase 4: Dynamic Analysis (Frida)

Use when static analysis is insufficient.

1. Hook Java methods: login, OkHttp, Retrofit, WebView, `javax.crypto`,
   `MessageDigest`, root detection, SSL pinning.
2. **Print arguments and return values before modifying anything.**
3. Observe runtime behavior: what methods are called, in what order, with
   what data.
4. Only after understanding the flow, consider targeted modifications.

### Phase 5: Native Library Analysis

When core logic is in `.so` files (signal: Java is a thin JNI wrapper,
core signing/validation not in Java, `System.loadLibrary` followed by
logic disappearance):

1. Triage the `.so` with `file`, `strings`, `rabin2`.
2. Quick analysis: radare2. Deep analysis: IDA or Ghidra.
3. See [binary-reverse-engineering.md](binary-reverse-engineering.md) for
   the full native analysis methodology.

## iOS (IPA) Methodology

### Phase 1: Triage

1. Decrypt if from App Store: `frida-ios-dump` or Clutch.
2. Read `Info.plist`: App Transport Security (ATS) settings, URL schemes,
   query schemes, background modes.
3. Export class structure: `class-dump` (Objective-C), `swift-demangle`
   for Swift symbols.
4. Check dependencies: `otool -L` for linked frameworks.
5. Detect obfuscation or hardening.

### Phase 2: Static Analysis

1. Objective-C: use `class-dump` output to map class hierarchy. Locate
   key methods by string references and method names.
2. Swift: use `swift-demangle`; locate business logic via string cross-
   references (Swift mangled names are less useful than ObjC selectors).
3. Mach-O analysis: `jtool2` or `otool` for segment/section layout,
   entitlements, code signature.
4. Decompile native code: Hopper, Ghidra, or IDA (see
   [macos-security.md](macos-security.md) for Apple platform specifics).

### Phase 3: Dynamic Analysis

1. Frida: hook Objective-C methods (`ObjC.classes`), Swift methods, and
   C functions.
2. Objection: REPL for common tasks (SSL pinning bypass, keychain dump,
   NSUserDefaults, pasteboard, UI dump).
3. Keychain analysis: dump and assess stored credentials, tokens.
4. Network: Burp Suite or mitmproxy with SSL pinning bypass.

## Cross-Platform Tool Chain

| Role | Android | iOS | Both |
|---|---|---|---|
| Decompile | jadx, apktool | class-dump | Ghidra, IDA |
| Dynamic hook | Frida | Frida | Frida |
| REPL | Objection | Objection | Objection |
| Network proxy | Burp, mitmproxy | Burp, mitmproxy | Burp, mitmproxy |
| Automated scan | MobSF | MobSF | MobSF |
| Native analysis | radare2, IDA | Hopper, IDA | radare2, Ghidra |

## Detection Layers (for assessment)

When evaluating an app's anti-analysis or anti-tamper defenses:

| Layer | What it checks | Assessment approach |
|---|---|---|
| Static | Package manager, file paths, permissions | Read manifest, resources |
| Runtime | Process list, port scan, memory, call stack | Frida hook detection points |
| Environment | ptrace, `/proc`, `build.prop`, direct syscalls | Trace system calls |

## Tool Roles

| Role | Tools |
|---|---|
| APK decompile | jadx, apktool, JEB Pro (commercial, optional) |
| Smali edit | apktool, baksmali |
| Device interaction | adb |
| Dynamic instrumentation | Frida, Objection |
| iOS decryption | frida-ios-dump, Clutch |
| iOS class export | class-dump, dsdump |
| Mach-O analysis | otool, jtool2, nm |
| Network interception | Burp Suite, mitmproxy, Wireshark |
| Automated scan | MobSF |
| Secret scanning | APKLeaks, manual string search |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- The app requires a live backend to test → confirm Level 3 authorization
  for the backend target.
- Dynamic analysis requires a rooted device or jailbroken device → ensure
  the user has authorized this and the test device is isolated.
- Frida hooking reveals credential exfiltration to an unknown server →
  note as finding; do not interact further with the unknown server
  without authorization.
- Native `.so` analysis exceeds this topic → load
  [binary-reverse-engineering.md](binary-reverse-engineering.md) only if
  native binary analysis is explicitly in scope; otherwise ask before opening
  the additional topic.
