# Browser Extension Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves analyzing a browser extension's security — permission
model, content script behavior, data exfiltration, or supply chain
extension poisoning.

## Methodology

### Phase 1: Package Analysis

1. Extract the extension: unpack `.crx` (it's a ZIP), or read from the
   browser profile directory.
2. Read `manifest.json` (MV2 or MV3):
   - `permissions` and `host_permissions`: assess over-granting
     (`<all_urls>`, `*://*/*`);
   - `webRequest` / `webRequestBlocking`: can intercept and modify all
     traffic;
   - `nativeMessaging`: can communicate with a native host process;
   - `externally_connectable`: allows web pages to send messages to the
     extension;
   - `content_scripts`: which scripts run on which sites, in which world
     (isolated vs main).
3. Identify entry points: background/service_worker, content scripts,
   popup, options page.

### Phase 2: Logic Analysis

1. Read the service worker / background script: what events trigger
   actions? What APIs are called?
2. Read content scripts: what data do they extract from pages? Do they
   send it anywhere?
3. Trace message passing: `runtime.sendMessage`, `tabs.sendMessage`,
   `port.postMessage` — who sends, who receives, what data?
4. Check `chrome.storage` / `IndexedDB`: are sensitive values (tokens,
   passwords) stored unencrypted?
5. Check `nativeMessaging`: what does the native host do? Is it a
   command execution risk?

### Phase 3: Dynamic Analysis

1. Load the unpacked extension in developer mode.
2. Attach DevTools to the service worker (`chrome://extensions` →
   inspect).
3. Observe network requests, message passing, and storage changes.
4. Test with controlled inputs on test pages.

## Risk Signals

| Manifest field | Risk | Assessment |
|---|---|---|
| `host_permissions: <all_urls>` | Can read/write any site | Is full access justified? |
| `webRequestBlocking` | MITM all traffic | Can it modify financial/health sites? |
| `nativeMessaging` | Escape browser sandbox | What does the native host do? |
| `externally_connectable` | Web pages can drive extension | Is the allowed origin list restrictive? |
| `content_scripts` on sensitive sites | Can steal data from banking/email | Is content script scope minimized? |

## Tool Roles

| Role | Tools |
|---|---|
| Extension unpacking | unzip, browser profile |
| Manifest analysis | jq, manual reading |
| JS analysis | browser DevTools, manual review |
| Service worker debug | chrome://extensions DevTools |
| Pattern matching | YARA (for malicious extension detection) |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- The extension communicates with a native host that executes commands
  → analyze the native host binary (see
  [binary-reverse-engineering.md](binary-reverse-engineering.md) or
  [thick-client-security.md](thick-client-security.md)); do not execute
  the native host without authorization.
- The extension exfiltrates data to an unknown server → note as finding;
  do not interact with the server.
- Complex obfuscated JS → use JS debugging tools; if beyond scope,
  document what was found and what requires deeper analysis.
