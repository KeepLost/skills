# Full-Stack Application Engineering

This reference adds full-stack technical guidance only. Task routing, authorization, testing order, review, and completion are governed by [`../SKILL.md`](../SKILL.md).

## System Facts and Boundaries

- Identify all entry points involved: browser or app UI, API handlers, jobs, events, persistence, and third-party integrations.
- Trace one representative request from user action through storage and back to rendered state.
- Locate existing schemas, generated clients, migrations, authentication checks, error envelopes, and test helpers.
- Confirm runtime and build commands from repository files rather than assuming package managers, ports, or directory names.
- Clarify ownership, consistency, latency, privacy, compatibility, and rollback requirements when they affect the design.

## Boundaries and Contracts

- Treat every process, network, queue, file, and database boundary as untrusted input.
- Define request, response, event, and persisted-data shapes explicitly using the project's existing schema mechanism.
- Validate syntax and business constraints at the boundary; do not rely on client validation for server safety.
- Keep transport concerns separate from reusable domain decisions when doing so improves clarity or testability.
- Do not require a controller/service/repository split. Functions, modules, use cases, or framework-native units are valid when responsibilities remain clear.
- Keep database and transport details from leaking into public contracts without a deliberate compatibility decision.
- Make null, absent, empty, and default values distinct where the domain distinguishes them.
- Use consistent identifiers, timestamps, enumeration values, pagination, and error shapes across an existing API.
- Preserve HTTP method and status semantics where HTTP is used; follow the repository's established API style.
- Breaking-change documentation should describe deprecation windows and consumer migration steps.
- Keep generated artifacts generated; change their source schema rather than hand-editing output.

## Data and Consistency

- Model constraints in the database when the database is the authority: keys, uniqueness, references, and valid ranges.
- Choose nullability from domain meaning, not convenience.
- Wrap multi-step writes that must succeed or fail together in an appropriate transaction.
- Design retryable writes and jobs for idempotency; assume delivery can be repeated.
- Prevent lost updates with transactions, version checks, locking, or conflict detection as appropriate.
- Add indexes from measured query patterns and inspect query plans for critical or high-volume paths.
- Avoid N+1 access by batching, joining, preloading, or changing the query shape.
- Use migrations for schema changes and review the generated operations before release.
- For live systems, prefer expand, backfill, switch, and contract over one-step destructive migrations.
- Account for old and new application versions running concurrently during rolling deployments.
- Define retention, deletion, backup, and restoration behavior for sensitive or irreplaceable data.
- Treat caches as derived data unless the design explicitly makes them authoritative; define expiry and invalidation.

## Authentication and Security

- Select session, token, OAuth, or another established mechanism based on current clients and trust boundaries.
- Authenticate on the server and authorize each protected operation and resource, including ownership checks.
- Apply least privilege to users, services, database roles, storage access, and administrative operations.
- Keep credentials and signing material out of source, logs, URLs, browser-readable storage, and generated bundles.
- Validate redirect targets, callback state, token audience, issuer, expiry, and replay protections in federated login flows.
- Prefer secure, HttpOnly, appropriately scoped cookies when cookies carry sensitive session material.
- Protect cookie-authenticated writes against cross-site request forgery and configure cross-origin access narrowly.
- Parameterize database queries and encode output for its rendering context.
- Limit request bodies, uploads, decompression, pagination, and expensive queries.
- For uploads, validate authorization, size, media type, content, filename handling, and final object ownership.
- Direct-to-object-storage uploads such as S3-style signed URLs are an option, not a requirement; keep signatures short-lived and verify completion server-side.
- Set timeouts for outbound calls and retry only transient, safe operations with bounded backoff and jitter.
- Never expose stack traces, raw queries, credentials, or internal topology to clients.
- Review affected dependencies and remove packages made unused by the change.

## Configuration and Environments

- Use the repository's configuration mechanism and validate required values before serving traffic.
- Separate deploy-time configuration from code while keeping safe local defaults where the project expects them.
- Maintain a non-secret example or schema for required settings.
- Do not make the browser responsible for secrets; values shipped to clients are public.
- Keep development, test, staging, and production behavior aligned except for intentional configuration differences.
- Make feature flags observable, removable, and safe in both states.
- Use deterministic lockfiles and repository-supported toolchains; do not introduce stale version pins from examples.

## Frontend Integration

- Reuse the existing client, cache, form, routing, and state-management patterns.
- Derive client types from a shared contract or verify independently maintained types with contract tests.
- Represent loading, empty, success, partial, stale, offline, validation, authorization, and unexpected-error states.
- Prevent duplicate submissions and make optimistic updates reversible on failure.
- Preserve user input when recoverable requests fail.
- Map server errors to useful user messages without displaying internal details.
- Keep server state and transient presentation state conceptually distinct.
- Cancel or ignore stale requests when navigation or newer input makes their result irrelevant.
- Ensure keyboard access, visible focus, semantic controls, labels, useful error announcements, and adequate contrast.
- Test layouts at narrow and wide widths, zoomed text, reduced motion, and slow or unavailable networks.

## Async Work and Real-Time Features

- Keep long-running or failure-prone work out of synchronous request paths when users do not need an immediate result.
- Define job identity, retry limits, backoff, timeout, cancellation, dead-letter handling, and operator visibility.
- Use polling, server-sent events, WebSockets, or brokered events according to directionality, scale, ordering, and infrastructure already present.
- Authenticate long-lived connections and re-check authorization when subscriptions or memberships change.
- Handle reconnects, duplicate messages, missed events, ordering, backpressure, and cleanup.
- Do not assume exactly-once delivery.

## Errors and Observability

- Use a stable external error code or type separate from localized user-facing text.
- Preserve causal errors internally while returning sanitized responses externally.
- Attach the repository's correlation identifier across HTTP calls, jobs, events, and logs.
- Log structured operational context without passwords, tokens, personal data, or full sensitive payloads.
- Measure critical-path latency, error rate, throughput, queue depth, dependency health, and resource saturation as relevant.
- Distinguish liveness from readiness if the deployment platform uses both.
- Ensure shutdown stops new work, drains bounded in-flight work, and closes resources.
- Alerts should map to actionable user or service impact rather than raw event volume.

## Full-Stack Test Coverage

- Unit-test important domain rules and edge cases at the smallest stable boundary.
- Integration-test API, persistence, serialization, authorization, and transaction behavior with realistic infrastructure where risk warrants it.
- Add contract tests at independently deployed or generated-client boundaries.
- Keep a small set of end-to-end tests for critical user journeys across frontend and backend.
- Test happy paths, invalid input, absent data, conflicts, permission denial, timeout, retry, duplicate delivery, and partial dependency failure.
- Isolate full-stack test data; do not depend on shared remote state.
- Verify migrations against representative data and test mixed-version compatibility when rollout requires it.
- Measure performance against project budgets instead of importing arbitrary thresholds.
- Applicable checks may include the repository's formatter, linter, type checker, tests, and production build.

## Release Verification

- Verify configuration, secrets provisioning, migrations, background workers, scheduled jobs, and observability in the target environment.
- Scan release artifacts for debug settings, source maps or symbols policy, and accidental secrets.
- Document rollout order when schema and application versions depend on each other.
- Define rollback triggers and steps, including what happens to data written after deployment.
- Smoke-test health and the core user journey after deployment.
- Compare error, latency, saturation, and business signals with the pre-release baseline.
- Report unresolved rollout and operational risks.

## Full-Stack Release Coverage

- [ ] Inputs, authentication, authorization, and sensitive data handling were reviewed.
- [ ] UI states and accessibility paths cover success and failure.
- [ ] Migration, rollout, rollback, and post-release checks are actionable.

