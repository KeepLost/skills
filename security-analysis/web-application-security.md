# Web Application Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves testing or reviewing the security of a web application.
This includes: OWASP Top 10 assessment, XSS/CSRF/SSRF/SQLi testing,
session management review, or front-end security analysis.

## Methodology

### Phase 1: Reconnaissance

1. Map the application: crawl with browser or proxy, identify all pages,
   forms, API endpoints, static resources.
2. Identify technology stack: server headers, framework signatures,
   JavaScript libraries, CDN.
3. Check for WAF/CDN presence: Cloudflare, AWS WAF, Akamai. Note: WAF
   affects testing approach but does not eliminate vulnerabilities.
4. Enumerate subdomains if in scope.

### Phase 2: Client-Side Analysis

1. **Surface**: collect all `src=`, `href=`, form actions, API calls
   from HTML and JS.
2. **Sink**: search JavaScript for dangerous patterns:
   - `innerHTML`, `outerHTML`, `document.write`;
   - `eval`, `Function`, `setTimeout(string)`;
   - `location.hash`, `location.search` used in DOM operations;
   - `__proto__`, `Object.assign` with user input (prototype pollution).
3. **Chain**: for each dangerous sink, trace whether user-controllable
   input (URL parameters, hash, postMessage, cookies) can reach it.
4. Distinguish `observed` (sink exists, input may reach it) from
   `validated` (PoC works, XSS fires).

### Phase 3: Server-Side Testing

| Vulnerability class | Test approach |
|---|---|
| XSS (reflected) | Inject markers in parameters, check reflection, test context (HTML/JS/attribute) |
| XSS (stored) | Inject in persistent fields, check rendering on other pages |
| XSS (DOM) | Trace from source (hash, postMessage) to sink (innerHTML) in JS |
| CSRF | Check for anti-CSRF tokens, test state-changing requests without token |
| SSRF | Test URL parameters for internal access (169.254.169.254, localhost, internal IPs) |
| SQLi | Test input fields with `'`, `' OR '1'='1`, time-based blind |
| SSTI | Test `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` in template-prone fields |
| XXE | Test XML endpoints for external entity, parameter entity, OOB |
| File upload | Test type validation bypass, path traversal in filename, content-type spoofing |
| Path traversal | `../` sequences in file parameters |
| Open redirect | URL parameters that cause browser navigation |
| Deserialization | Test serialized data in cookies, parameters, headers |

### Phase 4: Session and Authentication

1. Session token: predictability, entropy, fixation, rotation after
   login.
2. Cookie flags: `HttpOnly`, `Secure`, `SameSite`.
3. Session timeout and concurrent session limits.
4. Password reset flow: token predictability, token reuse, email
   enumeration.
5. Multi-factor authentication: bypass possibilities, SMS interception
   resistance.
6. Remember-me functionality: token structure and revocation.

### Phase 5: Configuration Review

1. Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options.
2. TLS configuration: protocol versions, cipher suites, certificate
   validity.
3. Directory listing, backup files, source maps in production.
4. Error handling: custom error pages vs stack traces.
5. Admin interfaces: default credentials, exposure, access control.

## Risk Tiering

| Action | Tier | Rule |
|---|---|---|
| Passive crawl, read public pages | Low | proceed |
| Send single test requests with markers | Medium | proceed with rate limit |
| Fuzzing, brute-force, automated scanning | High | confirm user approval |
| DoS testing, mass scanning | Critical | do not execute without per-action authorization |

## Tool Roles

| Role | Tools |
|---|---|
| Proxy and interception | Burp Suite, mitmproxy |
| Crawling | browser, Burp Spider |
| Scanning | ZAP, Nuclei (templates) |
| Fuzzing | FFUF, Gobuster |
| XSS detection | XSStrike, manual testing |
| SQL injection | SQLMap (authorized targets only) |
| SSTI detection | SSTImap, manual testing |
| Directory brute force | FFUF, Gobuster |
| Client-side analysis | browser DevTools, manual JS review |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Testing requires sending payloads to a live application → confirm
  Level 3 authorization.
- A WAF blocks testing → do not attempt to bypass WAF by flooding;
  adjust technique (encoding, alternative payloads, slower rate) or
  note the WAF as a finding.
- CSRF testing requires a victim user to click a link → do not send
  links to real users; use a test account.
- File upload testing could place executables on the server → confirm
  the test environment is isolated and cleaned afterward.
- Testing reveals a critical vulnerability (RCE, auth bypass) → report
  immediately; do not attempt post-exploitation without authorization.
