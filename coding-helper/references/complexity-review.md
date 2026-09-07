# Complexity Review

This is a supplementary guidance for a complexity-focused review, not a separate workflow. Task routing, authorization, testing order, review, and completion are governed by [`../SKILL.md`](../SKILL.md).

## Review Boundary

Start by defining the review target:

- the current diff;
- named files, modules, or layers; or
- the whole repository, only when the user requests a repository-wide audit.

Record the project root, relevant languages and frameworks, application entry points, build and test entry points, external boundaries, generated areas, and the working-tree state. Do not expand a focused review into a whole-project audit merely because more candidates are visible.

The question is not whether the code could be shorter. Ask:

> What actual requirement does this complexity serve, and is that value worth
> the additional understanding, change, test, deployment, and maintenance cost?

This reference supplements the main skill's investigation, review, safety, authorization, testing, and reporting rules. Follow `../SKILL.md` when those rules overlap. This review is read-only unless the user separately requests a change and the main skill's implementation route authorizes it.

## Evidence Before Judgment

Treat every apparent simplification as a hypothesis. Before reporting it as a finding, inspect as much of the following as the review boundary requires:

- all production callers and sibling entry paths;
- exports, imports, registrations, dependency-injection bindings, and factories;
- configuration consumers, feature-flag paths, and environment-specific wiring;
- tests that use the code as a replacement seam or contract boundary;
- public APIs, plugin points, generated files, scripts, and deployment manifests;
- external services, processes, packages, and independently released modules;
- runtime or reflective consumers that static search may not reveal.

"Only one implementation", "only one caller", or "no search result" is a lead, not proof. Search results can miss dynamic registration, generated configuration, reflection, runtime loading, external consumers, and migration paths. State the uncertainty instead of calling the code dead or unnecessary.

Do not assume that a similarly named standard-library or platform API is semantically equivalent. Check supported versions, input and output behavior, failure behavior, resource ownership, accessibility, security properties, and performance before recommending replacement.

## Candidate Patterns

Look for candidates in the inspected scope, not for opportunities to delete code at any cost:

- dead code, unreachable branches, unused exports, and unconsumed flags;
- an abstraction, interface, strategy, or factory with no current boundary or meaningful substitution point;
- a wrapper or service that only forwards arguments and return values without enforcing a contract, policy, translation, or useful seam;
- duplicated business rules, conversions, validation, adapters, or configuration that must be kept consistent manually;
- a dependency used for one narrow operation when a repository capability, standard-library feature, native framework facility, or small local operation satisfies the same contract;
- handwritten versions of standard-library, platform, or framework behavior;
- compatibility layers, extension points, or configuration options with no supported consumer or stated rollout need;
- layers whose only effect is indirection and whose boundary is not independently deployed, tested, owned, or required by the framework.

Use the existing complexity tags when helpful:

- `delete`: dead code, unused flexibility, or speculative behavior;
- `stdlib`: handwritten behavior already provided by the standard library;
- `native`: duplication of a platform or framework capability;
- `yagni`: complexity without a current requirement or real boundary;
- `shrink`: equivalent behavior can be expressed by a smaller clear change.

Tags classify a finding. They do not establish its evidence, severity, or correction.

## Complexity That May Be Necessary

Do not recommend removal solely because a component is large, layered, or has one implementation today. Complexity may be justified by:

- a public API, independently released package, plugin point, or service boundary;
- multiple deployments, implementations, tenants, platforms, or versions;
- a migration or compatibility period with a documented end condition;
- a security, permission, validation, audit, reliability, or error-isolation boundary;
- a test seam that isolates a real external or nondeterministic dependency;
- generated code or framework-required structure;
- an explicit product, operational, accessibility, or user requirement.

The burden is not to predict every future use. It is to identify a current requirement, supported boundary, or documented transition that the complexity serves. If the reason is plausible but not verifiable within the review scope, report it as an uncertainty or confirmation question rather than a deletion finding.

Never use this review to remove security controls, input validation, error handling, accessibility behavior, required tests, observability, or behavior the user explicitly requested. Do not turn a performance, correctness, or security issue into a complexity finding merely because the fix might be smaller.

## Report Format

Use the main skill's `Critical`, `Important`, and `Minor` severity definitions and finding fields. For each complexity finding, include:

- the tag, if one adds useful classification;
- the exact file and narrow line range;
- the actual requirement or boundary that was checked;
- the evidence showing why the current complexity is not justified;
- the trigger or scenario and maintenance impact;
- the smallest safe correction direction, without assuming implementation authorization.

Organize the result as:

1. **Scope**: target, inspected areas, project context, and known blind spots.
2. **Findings**: evidence-backed candidates ordered by the main skill's severity.
3. **Retained complexity**: structures that appear justified and why.
4. **Open questions**: dynamic consumers, external contracts, or other evidence needed before deciding.
5. **Reduction estimate**: only when supported by inspected evidence; do not invent line, file, dependency, or cost savings.

If no supported candidate remains, say so and distinguish that conclusion from the untested areas. A complexity review is normally advisory; do not mark a finding as blocking merely because a simpler design is imaginable. Use the main skill's blocking severities only when the complexity itself meets those definitions, such as a likely regression or a missing requirement.

The review is read-only by default. It does not authorize deleting files, removing dependencies, changing configuration, editing the user's work, or performing Git writes. If the user requests implementation after the review, return to the applicable route and gates in `../SKILL.md`.

