# API Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves testing or reviewing the security of an API — REST,
GraphQL, WebSocket, or gRPC. This includes: authentication/authorization
testing, input validation assessment, rate limiting evaluation, or
reviewing API design for security flaws.

## Methodology

### Phase 1: Discovery and Mapping

1. Identify API endpoints: documentation (OpenAPI/Swagger), JS files,
   robots.txt, common paths (`/api/`, `/graphql`, `/v1/`, `/v2/`).
2. If OpenAPI spec exists: parse it for endpoints, parameters, auth
   schemes, content types.
3. If no documentation: crawl with a browser or proxy (Burp, mitmproxy)
   to capture API calls. Generate an OpenAPI spec from observed traffic.
4. GraphQL: check for introspection (`{__schema{types{name}}}`). If
   enabled, extract the full schema. If disabled, try `__type` queries
   on known types.

### Phase 2: Authentication Testing

1. **JWT**: check algorithm confusion (alg=none, HS256 vs RS256 confusion),
   weak HMAC secrets, claim tampering, `kid` injection, JWK embedding.
2. **OAuth 2.0**: check `redirect_uri` validation, `state` parameter
   presence and binding, PKCE usage on public clients, scope escalation,
   token leakage via Referer.
3. **API keys**: check for predictable keys, key leakage in URLs/logs,
   key rotation policy.
4. **Session**: check session fixation, session timeout, concurrent
   session limits.

### Phase 3: Authorization Testing

1. **BOLA/IDOR**: replace resource IDs (numeric, UUID, username) with
   those of another user. Test horizontal (same role) and vertical
   (different role) access.
2. **Method switching**: try GET on POST-only endpoints, PUT on GET
   endpoints.
3. **API version downgrade**: test `/v1/` endpoints that may have weaker
   authorization than `/v2/`.
4. **Batch operations**: test if batch endpoints bypass per-item
   authorization.
5. **GraphQL**: test field-level authorization — different fields in the
   same query may have different auth requirements.

### Phase 4: Input Validation

1. **Injection**: SQL, NoSQL, command, template (SSTI), LDAP, XPath.
2. **Content-Type manipulation**: send JSON where XML expected, form-
   encoded where JSON expected.
3. **SSRF**: test URL parameters for internal endpoint access (metadata
   service, localhost, internal IPs).
4. **XXE**: test XML endpoints for external entity processing.
5. **Parameter pollution**: duplicate parameters, add unexpected
   parameters (mass assignment).
6. **GraphQL-specific**: alias overload, batch query overload, field
   repetition, directive overload, circular queries, nested deep queries.

### Phase 5: Business Logic

1. **Price/quantity manipulation**: negative values, zero, extreme values.
2. **Race conditions (TOCTOU)**: concurrent requests for coupon
   application, balance deduction, vote casting.
3. **Workflow bypass**: skip steps in a multi-step process.
4. **State manipulation**: modify client-side state that the server trusts.

### Phase 6: Data Exposure

1. Compare response payloads with what the UI displays — look for
   over-exposure of fields (password hashes, internal IDs, PII).
2. Check error messages for information leakage (stack traces, internal
   paths, SQL errors).
3. Check pagination for enumeration — sequential page IDs, count
   leakage.
4. GraphQL: check for nested queries that traverse authorization
   boundaries (e.g., `user { posts { author { email } } }`).

## Tool Roles

| Role | Tools |
|---|---|
| API discovery | Burp Suite, mitmproxy, Postman |
| OpenAPI generation | Vespasian (from traffic), manual |
| JWT testing | jwt_tool |
| Authorization testing | Burp Autorize, AuthMatrix |
| GraphQL testing | FireTail, manual queries |
| Fuzzing | FFUF, ffuf-poster |
| Rate limit testing | custom scripts |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.

## Stop Conditions

- Testing requires sending requests to a live API → confirm Level 3
  authorization (see
  [assessment-boundaries.md](assessment-boundaries.md)).
- An action would cause data modification (not just read) → confirm
  the user authorizes write operations on the test instance.
- Rate limit testing could cause DoS → use single requests, not floods;
  confirm the user authorizes load testing.
- GraphQL introspection is disabled and schema recovery requires
  brute-forcing field names → confirm this is authorized; it generates
  significant error traffic.
- JWT/identity testing overlaps with SSO → load
  [identity-federation-security.md](identity-federation-security.md) only if
  OAuth/SAML/OIDC protocol-level analysis is explicitly in scope; otherwise
  ask before opening the additional topic.
