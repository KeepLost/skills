# Android Application Engineering

This reference adds Android technical guidance only. Task routing, authorization, testing order, review, and completion are governed by [`../SKILL.md`](../SKILL.md).

Do not replace Views with Compose, Compose with Views, or one architecture with another merely for consistency with a generic template. Mixed UI stacks and incremental migrations are valid when ownership and state flow remain clear.

## Project and Platform Facts

- Inspect Gradle settings, version catalogs, build logic, modules, variants, manifests, and existing verification tasks.
- Use the checked-in Gradle wrapper and repository-supported JDK and Android toolchain.
- Identify minimum and target SDK policy, supported form factors, locales, themes, and distribution constraints.
- Trace the screen from navigation entry through state holder, data source, persistence or network, and back.
- Locate existing patterns for dependency injection, serialization, coroutines, testing, analytics, and error presentation.
- Do not paste dependency versions from examples; use the repository's dependency management and compatibility constraints.

## Kotlin and Boundary Contracts

- Use idiomatic Kotlin naming and keep visibility as narrow as practical.
- Model finite UI and domain states with sealed types or another exhaustive representation already used by the project.
- Choose `data class`, regular class, interface, or value class from semantics rather than a blanket rule.
- Make fields nullable only when the source contract permits absence or null, or the domain genuinely represents an unknown value.
- Keep required response fields non-null when guaranteed by a validated contract; let decoding or validation expose contract violations.
- Distinguish absent, null, empty, default, and malformed values at serialization boundaries.
- Avoid `!!` for recoverable data. A deliberate assertion is acceptable only for a proven invariant with an immediate, diagnosable failure.
- Do not silently replace invalid required data with empty strings, zeroes, or placeholder objects.
- Catch exceptions where context allows recovery, translation, cleanup, or logging; preserve cancellation and causal errors.
- Keep Android framework types out of reusable domain code when that separation has practical value.
- Validate intent extras, deep links, files, database records, and network payloads before use.

## Coroutines, Threads, and State

- Keep blocking disk, database, cryptographic, and network work off the main thread.
- Non-blocking suspend APIs do not need an `IO` context merely because they perform network or database operations.
- Let the component that performs blocking work own the dispatcher switch so callers can use it safely from the main thread.
- Use a compute-oriented dispatcher for substantial CPU work and measure before adding parallelism.
- Prefer lifecycle-owned scopes and structured concurrency; avoid process-wide or untracked scopes for screen work.
- Propagate cancellation and clean up child work when owners disappear.
- Treat mutable Compose snapshot state according to Compose's snapshot rules and keep UI side effects on the appropriate UI context.
- `StateFlow` is not inherently main-thread-only. Emission context follows the producer's work and invariants, while UI collection must respect lifecycle and rendering rules.
- Expose immutable state to consumers and keep mutation ownership clear.
- Collect UI flows with lifecycle-aware APIs so stopped screens do not keep unnecessary work active.
- Make one-off effects explicit when replaying durable state would repeat navigation, messages, or permission prompts.
- Test races, cancellation, rapid retries, process recreation, and stale responses where they can affect behavior.

## Compose and Views

- Hoist state to the lowest owner that needs to coordinate it; keep reusable UI driven by parameters and events.
- Avoid creating state holders, repositories, formatters, or expensive objects on every recomposition.
- Use stable item keys for dynamic lazy collections where identity matters.
- Keep side effects in the appropriate effect API and key them to the values that should restart the work.
- Avoid performing business work directly during composition or view binding.
- For Views, pair listener, observer, callback, and resource registration with lifecycle-appropriate removal.
- Do not retain Activity, Fragment, View, or composition references beyond their lifecycle.
- Use the repository's navigation pattern and pass identifiers or compact arguments rather than large mutable object graphs.
- Preserve saveable user input and navigation state across configuration change and recreate durable state after process death.
- Preview or screenshot-test reusable components when that tooling already exists.

## Resources and Design System

- Use resources for user-visible strings, plurals, dimensions, colors, and localized content as established by the repository.
- Follow Android resource identifier syntax and project prefixes; do not invent a list of forbidden generic names.
- Names such as `background`, `icon`, or `content` are not universally reserved. Rename only for an actual collision, platform restriction, or clearer meaning.
- Prefer semantic design tokens over copying literal colors and dimensions throughout screens.
- Support light, dark, and dynamic color behavior according to product requirements and the current design system.
- Use vector or appropriately density-qualified assets and adaptive launcher icons where supported.
- Keep text translatable: avoid string concatenation, preserve placeholders, and test expansion and right-to-left layout.
- Motion should communicate state or continuity, avoid jank, and respect reduced-motion preferences where available.

## Adaptive Layout and Input

- Design for the current window, not a hard-coded device category or orientation.
- Use supported window size and posture APIs already present in the project; do not infer layout solely from device model.
- Let compact, medium, and expanded arrangements share behavior while adapting navigation and content density.
- Avoid placing essential controls behind cutouts, system bars, display folds, or on-screen keyboards.
- Preserve state while rotating, resizing, entering multi-window, folding, or moving between displays.
- Do not assume full-screen ownership, touch-only input, or a single fixed aspect ratio.
- Provide visible focus, sensible traversal, keyboard activation, directional navigation, hover, and pointer behavior where applicable.
- Test the minimum supported window and at least one wider or multi-pane arrangement relevant to the product.

## Accessibility

- Prefer semantic platform controls and expose accurate role, state, value, and action information for custom controls.
- Give meaningful non-text controls concise labels; mark decorative content as excluded rather than describing it.
- Do not duplicate visible text or include redundant control types in announcements.
- Maintain logical reading and focus order, including after dynamic content and navigation changes.
- Provide alternatives for swipe, drag, long-press, and multi-pointer gestures.
- Keep interactive touch areas at least 48dp in ordinary cases, even when the visible icon is smaller.
- Do not convey state by color alone; combine color with text, shape, iconography, or semantics.
- Use semantic text sizing and ensure layouts reflow at large font scales without losing essential actions or content.
- Verify contrast against the project's accessibility target and current platform guidance.
- Test manually with TalkBack and keyboard or Switch Access, plus automated accessibility checks where available.

## Privacy and Platform Security

- Request only permissions required for a user-initiated feature and ask at the point of use.
- Explain the benefit before a request when context is not self-evident, then handle denial, restriction, and revocation gracefully.
- Prefer system pickers and scoped access over broad contacts, media, file, or location permissions.
- Minimize collected data and document collection, retention, deletion, and sharing accurately for distribution disclosures.
- Keep secrets out of source, resources, manifests, logs, backups, and client-delivered configuration.
- Store sensitive keys with Android Keystore-backed facilities and use maintained platform cryptography.
- Use encrypted transport for production endpoints and do not weaken trust globally for development convenience.
- Validate exported components, intent filters, URI hosts, MIME types, extras, and caller authorization.
- Explicitly choose component exposure and protect non-public components.
- Use immutable `PendingIntent` values unless the receiving API genuinely requires mutation.
- Restrict WebView capabilities, bridge methods, navigation, and loaded origins to the minimum needed.
- Redact credentials, tokens, personal data, and sensitive payloads from logs and crash reports.

## Background Work, Media, and Notifications

- Select lifecycle coroutine work, scheduled deferrable work, foreground service, alarm, or push based on user visibility and timing guarantees.
- Do not use background mechanisms to evade platform restrictions.
- Make durable work idempotent and define constraints, retry policy, cancellation, and user-visible status.
- Release wake locks, listeners, sensors, camera, microphone, media sessions, and location updates on every exit path.
- Respect audio focus, interruption, noisy-route, playback, and foreground-service requirements for media features.
- Create meaningful notification channels and let users control non-essential categories.
- Notifications must be timely, actionable, non-sensitive on lock screens, and deep-link to a valid destination.

## Performance and Stability

- Establish a baseline before optimization and use current platform metrics rather than copied historical thresholds.
- Keep startup work minimal; defer non-critical initialization and avoid hidden synchronous I/O.
- Profile slow frames, recomposition, layout, allocation, memory retention, battery, and network usage on representative devices.
- Downsample images and bound caches, collections, retries, and queued work.
- Use debug-time diagnostics for accidental main-thread I/O and leaked lifecycle references.
- Add baseline profiles or benchmarks for measured hot paths when the project supports them.
- Handle low-memory, offline, background, process-death, and dependency-failure paths without data corruption.

## Testing and Release Verification

- Unit-test domain rules, state transitions, serialization boundaries, and coroutine cancellation with deterministic dispatchers or clocks.
- Integration-test storage, migrations, networking adapters, permissions, intents, and dependency wiring at the suitable level.
- UI-test critical journeys, accessibility semantics, back behavior, configuration changes, and error recovery.
- Test representative API levels, window sizes, themes, font scales, locales, and input modes from the support policy.
- Applicable Android checks may include repository formatting, static analysis, unit tests, instrumentation tests, and relevant release-build tasks.
- Inspect the merged manifest, packaged resources, permissions, exported components, signing mode, and shrinker output.
- Verify install, upgrade, migration, deep links, notifications, offline startup, and core flows on a release-like artifact.
- Review current distribution policy, privacy disclosure, target SDK, and release notes before submission.
- Compare startup, crash, ANR, rendering, battery, and business signals after staged rollout; keep a rollback or halt plan.

## Android Release Coverage

- [ ] Nullability and threading choices reflect real contracts rather than blanket rules.
- [ ] Adaptive layout, accessibility, lifecycle, privacy, and denial paths were verified.
- [ ] Checks cover the intended variant and a release-like artifact where applicable.
- [ ] Distribution requirements and staged-release monitoring are actionable.

