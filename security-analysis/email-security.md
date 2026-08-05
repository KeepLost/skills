# Email Security

> This reference provides technical guidance only. It does not grant
> authorization, replace the workflow in [../coding-helper/SKILL.md](../coding-helper/SKILL.md),
> or relax any higher-priority safety, permission, or Stop Condition
> boundary.

## When to Load

The task involves analyzing email authentication, phishing samples, or
mail gateway configuration. This includes: SPF/DKIM/DMARC assessment,
phishing email analysis, or mail tenant security review.

## Methodology

1. **Header authentication**: parse Received chain, From/Return-Path
   alignment, SPF/DKIM/DMARC results from the original headers.
2. **DNS records**: verify SPF (`dig TXT domain`), DKIM selectors
   (`dig TXT selector._domainkey.domain`), DMARC (`dig TXT _dmarc.domain`).
3. **Content analysis**: URL extraction and sandboxing, attachment
   analysis (see [malware-analysis.md](malware-analysis.md)).
4. **Tenant configuration**: anti-phishing policies, external sender
   marking, MFA enforcement, OAuth app consent policies.

**Do not re-send malicious samples to real users. Do not perform
unauthorized phishing simulations.**

## Tool Roles

| Role | Tools |
|---|---|
| DNS lookup | dig, nslookup |
| Header analysis | email client "view source" |
| URL sandbox | urlscan, browser sandbox |
| Attachment analysis | see malware-analysis.md |

Load [tool-catalog.md](tool-catalog.md) only if this role summary is insufficient.
