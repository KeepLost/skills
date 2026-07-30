# Frontend UI Engineering

Use this reference when visual direction, responsive layout, interaction, accessibility, or frontend polish is a material part of the task. It adds frontend technical guidance only; process and authorization are governed by [`../SKILL.md`](../SKILL.md).

## Visual Facts to Establish

1. Identify the page type, audience, primary action, and content hierarchy.
2. Inspect existing components, design tokens, breakpoints, dependencies, and accessibility conventions.
3. Inventory repository assets and user-provided assets, including their aspect ratios, resolution, licensing notes, and intended placements.
4. State a concise design read: page type, audience, visual character, and the existing system to preserve or extend.
5. Treat materially different plausible visual directions as design ambiguity governed by `SKILL.md`.

Do not begin from a fashionable default. Purple glow, generic glass panels, centered hero copy, equal feature cards, and arbitrary gradients are not a design direction unless the brief supports them.

## Local Asset Policy

Use only:

- assets already present in the repository;
- files directly supplied by the user;
- simple local placeholders that clearly state the required subject, dimensions, and aspect ratio.

Do not add external image, font, icon, video, or stylesheet URLs. Do not make asset acquisition a prerequisite for a working page. When a required asset is missing, keep the layout functional with a local placeholder such as:

```html
<div class="media-placeholder" role="img"
     aria-label="Placeholder for product photograph, 4 by 3 aspect ratio">
  Product photograph, 1600 x 1200
</div>
```

Prefer project fonts or the system font stack. Do not copy bundled font files into the project. Use an icon library only when it is already installed; for a small structural symbol, plain text or a simple CSS shape is acceptable.

## Establish A Visual System

Prefer a small set of semantic tokens over isolated component values:

```css
:root {
  --surface: #f4f4f0;
  --surface-raised: #ffffff;
  --text: #191a1c;
  --text-muted: #62656a;
  --accent: #155eef;
  --border: #d8d9d5;
  --radius-control: 0.5rem;
  --radius-panel: 1rem;
  --space-section: clamp(4rem, 9vw, 8rem);
}
```

- Use one accent family and one neutral temperature across the page.
- Choose a documented radius rule; avoid random mixtures of sharp, soft, and pill shapes.
- Use elevation only when it communicates hierarchy. Prefer spacing, dividers, and surface contrast over wrapping every group in a card.
- Keep body copy to a readable measure, normally `55ch` to `70ch`.
- Use real content from the task. Mark invented metrics or sample records as examples rather than presenting them as facts.

## Layout And Composition

Use CSS Grid for page-level composition and Flexbox for one-dimensional control groups. Build mobile behavior into each section instead of relying on accidental wrapping.

- Keep desktop navigation on one line or switch deliberately to compact navigation.
- Fit the primary message and action into the initial viewport when the page has a hero. Use `min-height: 100dvh`, not `100vh`, for full-height mobile sections.
- Limit hero copy to one focused headline, a short explanation, and at most two actions.
- Avoid repeating the same section composition consecutively. Alternate grids, editorial blocks, full-width visuals, and compact lists when the content calls for them.
- Use asymmetric layouts only above a breakpoint, with an explicit single-column mobile fallback.
- Reserve image dimensions with `width` and `height` or `aspect-ratio` to prevent layout shift.

## Responsive Baseline

Start from the narrow layout and add complexity only when space permits:

```css
.feature {
  display: grid;
  gap: 1.5rem;
  padding-block: var(--space-section);
}

@media (min-width: 48rem) {
  .feature {
    grid-template-columns: minmax(0, 5fr) minmax(18rem, 7fr);
    align-items: center;
  }
}
```

Test at narrow phone, wide phone, tablet, laptop, and large desktop widths. Check long headings, zoomed text, empty data, error messages, and translated copy rather than validating only the ideal screenshot.

## Interaction And Motion

Motion must communicate hierarchy, feedback, or state change. Prefer CSS for simple transitions and the project's existing motion library for coordinated sequences.

- Animate `transform` and `opacity`; avoid continuous layout-triggering changes.
- Do not store pointer position or scroll progress in component state on every frame. Use platform animation primitives or the existing motion-value pattern.
- Clean up observers, timers, animation frames, and event listeners.
- Keep hover effects supplementary; keyboard and touch users need the same information and actions.
- Disable or simplify nonessential movement under reduced-motion preferences.

```css
.reveal {
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: no-preference) {
  .reveal[data-state="entering"] {
    opacity: 0;
    transform: translateY(1rem);
  }

  .reveal {
    transition: opacity 280ms ease, transform 280ms ease;
  }
}
```

Avoid scroll interception unless it is central to the intended experience and has a normal-flow fallback. Do not add perpetual motion merely to make a static section appear more sophisticated.

## States And Accessibility

Implement the complete interaction cycle:

- visible labels, instructions, and validation for forms;
- loading placeholders shaped like the final content;
- useful empty states with a clear next action;
- contextual errors with recovery guidance;
- visible hover, active, focus, selected, disabled, and pending states;
- semantic landmarks and heading order;
- keyboard operation and sensible focus movement;
- text alternatives for informative local media and empty alternatives for
  decorative media.

Meet WCAG AA contrast for text and controls. Never rely on color alone. Maintain a minimum practical target size around 44 CSS pixels for primary touch controls, and verify layouts at 200 percent zoom.

## Framework Discipline

- Keep static layout server-renderable when the framework supports it; isolate browser-only behavior in small interactive leaves.
- Do not import a package absent from the project manifest.
- Reuse established primitives before creating a parallel component system.
- Do not add memoization wrappers by default. Use them only for a measured or structurally necessary reason.
- Preserve URL, form, and native browser semantics instead of replacing them with custom click handlers.

## Browser Acceptance Checks

Review the implementation in a real browser, not only from source:

1. Compare hierarchy and tone with the brief and existing product.
2. Inspect every breakpoint and both supported color schemes.
3. Read every visible string for clarity and factual support.
4. Check asset cropping, placeholder labels, focus order, and reduced motion.
5. Confirm the page has no horizontal overflow, clipped display text, wrapped desktop actions, duplicate primary actions, or unexpected layout shift.

