# Identity Federation Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves testing or reviewing SSO, OAuth, SAML, OIDC, or other
federated identity systems. This includes: redirect_uri validation
testing, token handling review, session management assessment, or
federation protocol flow analysis.

## Methodology

### Phase 1: Protocol Flow Mapping

1. Map the complete authentication flow: User → Service Provider (SP) →
   Identity Provider (IdP) → Token → SP.
2. Collect metadata: `/.well-known/openid-configuration` (OIDC), SAML
   metadata XML.
3. Identify: authorization endpoint, token endpoint, userinfo endpoint,
   supported scopes, supported grant types, registered redirect URIs.
4. Trace the flow in browser DevTools: follow redirects, note parameters
   at each step.

### Phase 2: Common Misconfiguration Testing

1. **redirect_uri validation**:
   - exact match vs prefix match vs wildcard;
   - test path traversal (`/callback/../evil`);
   - test open redirect chains (`/callback?next=//evil.com`);
   - test subdomain takeover (dangling DNS pointing to your server).
2. **state parameter**:
   - present? bound to session? validated on callback?
   - missing state → CSRF on authorization callback.
3. **PKCE**:
   - used on public clients (SPA, mobile)?
   - `code_verifier` validated? `code_challenge_method` = S256?
4. **nonce**:
   - present in OIDC implicit/hybrid flows?
   - validated in ID token?
5. **SAML-specific**:
   - signature covers full assertion (not just parts)?
   - signature algorithm (SHA-1 should be deprecated)?
   - comment injection in assertion (`<!-- -->` within signed content)?
   - XSW (XML Signature Wrapping) variants?
6. **JWT-specific**:
   - algorithm confusion (RS256 → HS256 with public key as secret);
   - `alg: none` acceptance;
   - weak HMAC secret (crackable);
   - `kid` parameter injection (path traversal, SQL injection);
   - JWK header injection (attacker embeds own key).

### Phase 3: Session and Token Lifecycle

1. **Session fixation**: does the session ID change after authentication?
2. **Token replay**: can an access token be used after logout?
3. **Refresh token rotation**: is the refresh token rotated on each use?
   Does the old token get revoked?
4. **Token storage**: where are tokens stored client-side (localStorage
   → XSS accessible, sessionStorage, HttpOnly cookie)?
5. **Logout**: does logout invalidate tokens server-side, or just clear
   client storage?

### Phase 4: Account Linking and Federation

1. Can a user link an external identity to an existing account without
   re-authentication?
2. Email verification: can an attacker claim an email they don't own
   during federation?
3. Tenant isolation: in multi-tenant IdP, can a user from tenant A
   access tenant B's resources?

## Checklist

- [ ] redirect_uri exact match enforced
- [ ] state parameter present and session-bound
- [ ] PKCE used on public clients
- [ ] SAML signature covers full assertion
- [ ] JWT algorithm pinned (not accepting `none`)
- [ ] Refresh tokens rotated
- [ ] Logout invalidates tokens server-side
- [ ] Account linking requires re-authentication
- [ ] Email verified before federation linking

## Tool Roles

| Role | Tools |
|---|---|
| SAML testing | SAML Raider (Burp extension), manual |
| JWT testing | jwt_tool |
| Flow tracing | browser DevTools, Burp Suite |
| Token inspection | jwt.io, manual decoding |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Testing requires creating accounts on the IdP → confirm Level 3
  authorization and use test accounts, not real user accounts.
- Do not perform brute-force on real user accounts — this can lock them
  out.
- SAML assertion manipulation requires sending modified requests to the
  SP → confirm the SP is a test instance.
- If token theft is possible → note the finding; do not use stolen tokens
  to access other users' data without authorization.
- Pure API JWT testing → may overlap with
  [api-security.md](api-security.md); use that reference for REST API
  endpoint testing.
