# Theme authoring

A **theme** is a named color family. A **mode** is light, dark or system. Every named theme must ship both a light and dark definition; system chooses between them using the user's device setting. Never encode a theme name in a component class.

## Stable names

Components use these roles in both modes:

| Family | Public CSS variables after `--tide-color-` |
| --- | --- |
| Surfaces | `canvas`, `surface`, `raised`, `field` |
| Text | `text-primary`, `text-secondary`, `text-muted`, `text-label` |
| Actions | `accent`, `on-accent`, `accent-hover`, `focus` |
| Boundaries | `border-subtle`, `border-strong`, `border-control` |
| Selection | `selected-surface`, `selected-text`, `selected-border` |
| Status | `status-success-text/surface/border`, `status-warning-text/surface/border`, `status-danger-text/surface/border` |
| Photo context | `photo-canvas`, `photo-text-primary`, `photo-text-secondary`, `photo-text-muted`, `photo-accent`, `on-photo-accent`, `photo-accent-hover` |

For example, `--tide-color-text-secondary` must remain readable on every ordinary surface on which supporting text can appear. `--tide-color-border-control` must identify a field or actionable outline. A decorative separator uses `border-subtle` and is not expected to identify a control. Status hue never replaces words such as Cancelled, Published or Pending review.

Generated implementation values follow `--tide-palette-{role}-{light|dark}`. Semantic aliases use `light-dark()`, for example:

```css
--tide-color-canvas: light-dark(
  var(--tide-palette-canvas-light),
  var(--tide-palette-canvas-dark)
);
```

Do not consume the implementation names in components. There is no `text-primary-dark` component contract to maintain separately.

## Add a seed-based theme

Add one entry in `tokens/themes.json`. This example intentionally has an orange-tinted canvas. It is sufficient input; you do not need to manually recolor each component.

```json
"apricot": {
  "name": "Apricot",
  "description": "A warm surface with plum actions.",
  "light": {
    "canvas": [0.925, 0.060, 65],
    "accent": [0.410, 0.105, 340]
  },
  "dark": {
    "canvas": [0.200, 0.021, 55],
    "accent": [0.810, 0.105, 55]
  }
}
```

Run `python tools/build.py`, review both generated modes, then run the remaining checks in the README. The compiler generates the selector, semantic role values, reference pages, all eleven screen fixtures, tokens JSON and contrast report for the new theme. Component HTML/CSS does not change.

The recipe derives surfaces and tinted text from the actual canvas. It determines foreground polarity from measured luminance, not from a theme name. It reduces OKLCH chroma to fit sRGB, then searches for the closest passing foreground lightness against every applicable background. Status hues retain meaning; their text values are also checked against ordinary surfaces for inline validation. The full-screen photo opening uses the theme's dark photo-context colors in both page modes; the details below it follow the page's active mode.

## Curated overrides

Tide carries explicit role overrides imported from the approved Tide/Mist palettes so the selected appearance is preserved. An optional `overrides` object may set known semantic role colors as OKLCH triples. Every override is still gamut-mapped and contrast-checked; text/control lightness can be adjusted to pass. The allowed role list is validated by the compiler.

For a new background-led theme, start with the minimal seed example above rather than copying Tide's curated overrides. Existing surface overrides are explicit colors: they do not automatically follow a changed canvas seed. Remove them to use the generated surface recipe, or intentionally specify the complete new surface family. The gate rejects incompatible mixtures for which one shared foreground cannot be found.

## Accessibility gate

The report is `qa/contrast.json`. Each theme/mode measures:

- Primary, secondary, muted, label and accent text on canvas, surface, raised and field: at least 4.5:1 for ordinary-size text.
- Inline status/error text on those same surfaces and badge text on its badge surface: at least 4.5:1.
- Primary action labels on the normal and actual OKLab-mixed hover/pressed background: at least 4.5:1.
- Selected labels on their selected surface: at least 4.5:1.
- Control boundaries, selected boundaries, and focus outlines on their supported adjacent surfaces: at least 3:1. A surface-colored offset separates the focus ring from a filled control.
- Photo text/action colors against the photo context's opaque base. These measurements do not validate every pixel of an uploaded image.

The generator aims slightly above the thresholds to avoid rounding-edge failures. It cannot make every arbitrary set of background colors share an accessible foreground. When surfaces need opposite foreground polarities, introduce a separate, documented surface context with its own paired roles instead of forcing one text token to serve both.

Do not bypass the workflow by changing only `--tide-color-canvas` inline and assume the rest is automatically accessible. Modern CSS color notation and mixing are useful color tools; they are not a universal accessibility guarantee. `contrast-color()` now has current-engine support, but it chooses black or white and does not resolve a full branded hierarchy or status palette. This kit uses checked, colored foreground pairs instead.

## Modes and user preferences

Use `data-mode="light"` or `dark` to force a mode with `color-scheme: only …`. Use `system` or omit the attribute to follow the OS. Form controls inherit that color scheme. The theme recipe itself is compiled ahead of time; no theme JavaScript is required.

`prefers-contrast: more` promotes supporting text to primary and removes the dotted texture. Forced colors restores system colors and visible control boundaries without disabling the browser's adjustments. No motion is added, so reduced-motion users receive the same resting UI. Photo scrims are functional readability treatments; new uploads still require image review or a solid fallback.

Theme inputs are deliberately restricted to palette colors and texture opacity. Geometry, font families, type weights, margins, insets, target sizes and corner radii are not theme inputs.
