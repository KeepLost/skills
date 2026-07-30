# iOS Application Engineering

This reference adds iOS technical guidance only. Task routing, authorization, testing order, review, and completion are governed by [`../SKILL.md`](../SKILL.md).

Do not rewrite UIKit as SwiftUI, SwiftUI as UIKit, or an established layout approach merely to follow a generic preference. Interoperability and incremental migration are valid when lifecycle and state ownership are clear.

## Project and Platform Facts

- Inspect project or workspace settings, package resolution, targets, schemes, entitlements, capabilities, and build configurations.
- Confirm supported OS versions, device families, orientations, locales, appearance modes, and accessibility requirements.
- Trace the feature from app or scene entry through navigation, state ownership, persistence or networking, and rendered output.
- Locate established patterns for observation, dependency injection, concurrency, testing, analytics, localization, and errors.
- Schemes, simulator targets, paths, and dependency versions come from project configuration.

## Swift and Domain Modeling

- Use existing Swift naming conventions; keep access control as narrow as practical.
- Use structs for value semantics, classes or actors for identity and shared ownership, and enums for finite states when those semantics fit.
- Prefer composition and focused protocols when they create useful seams; do not introduce protocols only to satisfy a pattern.
- Choose optionality from the data contract and domain, distinguishing absent, null, empty, default, and invalid values.
- Avoid force unwraps and `try!` for recoverable runtime data. A deliberate assertion may represent a proven programmer invariant.
- Do not silently replace malformed required data with placeholders that hide contract failures.
- Define typed errors at meaningful boundaries and preserve underlying causes for diagnostics.
- Translate technical failures into actionable, localized UI states without exposing sensitive details.
- Keep framework-specific UI types out of reusable domain code when the separation improves portability or testing.
- Validate URLs, deep links, pasteboard data, files, decoded payloads, and external input before use.

## Concurrency and State

- Use structured concurrency and tie tasks to the lifecycle or operation that owns them.
- Isolate UI-observable state and UI mutations to the main actor.
- Do not mark unrelated networking, parsing, or persistence code as main-actor-isolated merely because UI calls it.
- Use actors, immutability, or explicit synchronization for shared mutable state.
- Propagate cancellation and check it in long loops, staged operations, image processing, and retry paths.
- Avoid unstructured detached tasks unless execution must intentionally outlive the caller and ownership is documented.
- Bound parallel work and preserve deterministic ordering when the product depends on it.
- Prevent stale responses from overwriting newer user intent.
- Make one source of truth for each piece of durable screen state; derive display-only values where practical.
- Persist only the state needed to restore the user journey after scene recreation or process termination.
- Test cancellation, rapid navigation, duplicate actions, races, backgrounding, and restoration.

## Memory and Resource Ownership

- Understand closure and delegate ownership before adding `weak` or `unowned`; use each according to actual lifetime guarantees.
- Break retain cycles in callbacks, timers, display links, delegates, subscriptions, and long-lived tasks.
- Remove observers and invalidate resources when the chosen API does not manage their lifetime automatically.
- Release camera, microphone, location, media, file, and graphics resources on every completion and cancellation path.
- Avoid retaining view controllers or views in model and service objects.
- Profile suspected leaks and allocations rather than applying blanket weak-reference rules.

## UI Frameworks and Layout

- Use the UI framework and layout mechanism already dominant in the feature unless change scope justifies migration.
- Auto Layout anchors, Interface Builder, stack views, frame-based layout, and layout DSLs are implementation choices, not universal requirements.
- Build from semantic system controls before creating custom interaction behavior.
- Respect safe areas for interactive content; extend backgrounds under system regions only intentionally.
- Avoid fixed widths and heights for text-bearing controls unless constraints allow content to grow and reflow.
- Use trait collections, container-relative geometry, and size classes where behavior must adapt.
- Test compact and regular widths, multitasking, rotation, keyboard presentation, and every supported device family.
- Do not design only for a named phone size. Support is defined by project settings and product policy.
- Use semantic colors or appearance-aware assets and verify both light and dark appearances.
- Use semantic text styles or scale custom fonts relative to a text style.
- Localize user-visible strings, pluralization, dates, numbers, currencies, and accessibility text.
- Test text expansion, right-to-left layout, and accessibility text sizes without clipping essential content.

## SwiftUI State and Effects

- Match property wrappers and observation tools to ownership: local value, owned model, injected dependency, or shared environment.
- Do not recreate owned observable state during routine view recomputation.
- Keep view bodies declarative and move side effects to lifecycle or task modifiers keyed to true dependencies.
- Give dynamic collections stable identity and do not use array position when identity can change.
- Avoid broad environment dependencies that hide required inputs or make previews and tests fragile.
- Keep bindings focused; pass events instead of exposing unrestricted mutable state when the child does not own it.
- Confirm availability for APIs newer than the deployment target and provide a repository-appropriate fallback.

## UIKit Lifecycle and Presentation

- Keep setup, constraint activation, data binding, appearance work, and teardown in lifecycle stages that match their semantics.
- Reuse cells safely by resetting transient state and canceling obsolete asynchronous work.
- Update collection and table models with consistent identity and apply snapshots on the appropriate context.
- Configure popover source information for presentations that require it on wider layouts.
- Provide an obvious completion or dismissal path for focused modal tasks and protect unsaved work.
- Preserve system navigation behavior unless the product intentionally replaces it with an accessible equivalent.

## Navigation

- Choose tabs, stacks, split views, columns, sheets, popovers, sidebars, menus, or custom navigation from information architecture and current platform context.
- Do not impose a tab count, stack-depth limit, or universal navigation container without product evidence.
- A drawer or menu is not categorically forbidden, but primary destinations should remain discoverable and the pattern must work with accessibility and adaptive layouts.
- Keep destination identity and restoration data serializable where navigation state must survive relaunch.
- Validate all deep-link routes and authorization before displaying destination content.
- Preserve state when switching top-level destinations where users reasonably expect continuity.
- Ensure back, dismiss, keyboard, pointer, and assistive-technology paths remain available.

## Accessibility

- Prefer native controls that already expose role, value, state, focus, and actions.
- Give icon-only and custom controls meaningful labels, traits, values, and hints; mark decorative images as such.
- Group or separate elements to create a concise, logical VoiceOver reading order.
- Post accessibility notifications only when focus or a significant dynamic update would otherwise be missed.
- Maintain at least a 44 by 44 point activation area for ordinary interactive controls.
- Do not convey meaning with color alone; combine it with text, shape, symbols, patterns, or accessibility values.
- Verify contrast against the project's accessibility target and current platform guidance.
- Support Dynamic Type through accessibility sizes and let layouts reflow rather than truncate essential text.
- Respect Reduce Motion, Differentiate Without Color, Bold Text, Increase Contrast, and reduced-transparency preferences where relevant.
- Provide accessible alternatives for drag, swipe, long-press, multi-touch, timed, and motion-based interactions.
- Test manually with VoiceOver, large text, keyboard or switch input, and relevant automated accessibility checks.

## Privacy, Permissions, and Security

- Request only capabilities needed for a user-initiated feature and request them when the benefit is clear.
- Provide accurate usage descriptions and handle authorized, limited, denied, restricted, and revoked states.
- Prefer system pickers and limited-library or one-time access over broad persistent permission where feasible.
- Keep the app useful in a reduced mode when denial does not make the core purpose impossible.
- Minimize collected data and align implementation, privacy manifest, disclosures, retention, deletion, and account controls.
- Keep credentials, tokens, signing material, and private endpoints out of source, logs, bundles, and client-visible configuration.
- Store sensitive secrets with Keychain-backed facilities and use maintained platform cryptography.
- Use protected transport and narrowly scoped exceptions only when a documented integration requires them.
- Authenticate and authorize universal links, custom URLs, notifications, activities, extensions, and shared containers at trust boundaries.
- Redact personal and authentication data from logs, analytics, screenshots, notifications, and crash metadata.
- Treat pasteboard, WebView content, JavaScript bridges, imported files, and extension input as untrusted.

## System Integration and Lifecycle

- Model inactive, background, foreground, interruption, restoration, and termination paths for the feature's resources and state.
- Do not depend on termination callbacks for essential persistence.
- Register background work with the platform mechanism that matches its duration and user value; expiration and denial are normal outcomes.
- Make background and retryable work idempotent, cancellable, and observable.
- Use system share, document, photo, authentication, and location interfaces when they reduce permissions and improve consistency.
- Validate notification categories, actions, privacy, deep-link destinations, and authorization at handling time.
- Use haptics as reinforcing feedback, not as the only signal, and prepare generators only when latency matters.
- Make scenes and multiple windows independent where the product supports them.

## Performance and Resilience

- Measure startup, hangs, frame pacing, memory, disk, network, energy, and binary size before optimizing.
- Keep startup synchronous work minimal and defer non-essential initialization.
- Decode, resize, and cache images according to display need; bound memory and disk caches.
- Avoid expensive work in rendering, scrolling, layout, and frequently evaluated computed properties.
- Handle offline operation, low memory, background expiration, interrupted requests, partial data, and dependency failure.
- Use instruments, signposts, metrics, and repository-supported benchmarks for evidence rather than guessed thresholds.

## Testing and Release Verification

- Unit-test domain rules, state transitions, decoding, formatting, error mapping, and concurrency-sensitive behavior.
- Integration-test persistence migrations, networking adapters, deep links, notifications, entitlements, and system boundaries as risk requires.
- UI-test critical journeys, accessibility identifiers and semantics, restoration, permission denial, and error recovery.
- Test the supported OS range, representative compact and regular layouts, appearances, locales, text sizes, and input methods.
- Applicable iOS checks may include repository formatting, static analysis, package resolution, tests, archive, and release-configuration builds.
- Inspect the archive for signing, entitlements, privacy metadata, usage descriptions, symbols, debug settings, and accidental secrets.
- Verify clean install, upgrade, migration, launch, deep links, offline startup, and core flows using a release-like build.
- Review current distribution rules, screenshots, metadata, disclosures, export compliance, and release notes before submission.
- Use staged release where appropriate; monitor crashes, hangs, startup, responsiveness, energy, and product signals with rollback criteria.

## iOS Release Coverage

- [ ] Layout works across supported devices, windows, text sizes, and appearance modes.
- [ ] Accessibility, permission denial, lifecycle, privacy, and restoration paths were verified.
- [ ] Relevant tests, archive, and release-like smoke checks cover the intended release path.
- [ ] Distribution metadata, monitoring, and rollout response are actionable.

