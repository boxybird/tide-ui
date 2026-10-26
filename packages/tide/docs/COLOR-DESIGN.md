# Color design policy · kit 1.4.0

Reviewed 2026-10-26. Accessibility is a requirement; it does not determine whether a palette feels balanced. The user accepts Bumble Dark and rejects the broad yellow wash in Bumble Light. The implementation therefore keeps Bumble Dark unchanged and makes neutral surfaces the starting point for new pairs.

## Research and application

- [IBM Carbon: Color](https://www.carbondesignsystem.com/building-blocks/foundations/color/overview) uses dominant neutral layers and purposeful action color. Tide application: canvas, ordinary surfaces, fields and reading text should remain neutral or subtly tinted; reserve stronger color for interaction emphasis.
- [Material: Color roles](https://m3.material.io/styles/color/roles) separates surface roles from accent and paired foreground roles. Tide application: preserve semantic roles across modes and verify each intended foreground/background pair. A theme's identity need not cover the page background.
- [Radix: Composing a palette](https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette) distinguishes accent, gray, status and text scales and cautions against saturated grays competing with colorful components. Yellow/amber solid scales use dark text. Tide application: use restrained neutrals; never assume white text works on honey.
- [Radix: Understanding the scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale) distinguishes app backgrounds, component states, borders, solid fills and text. Tide application: evaluate those roles independently rather than treating one brand swatch as a complete theme. Radix's stated APCA guarantees do not replace Tide's WCAG 2 ratio checks.
- [WCAG 2.2 text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) requires 4.5:1 for ordinary text and 3:1 for qualifying large text. Tide retains its stricter all-normal-text gate, including supporting labels.
- [WCAG 2.2 non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) requires 3:1 for visual information necessary to identify controls/states against adjacent colors. Decorative separators need not meet that threshold. [Use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) also requires meaning beyond hue; retain labels, native checked state and focus outlines.

These systems support role separation and deliberate color use. They do not establish a universal accent-area percentage or guarantee aesthetic preference. The following numeric seeds are Tide design choices, not industry standards.

## Maintained directions

| Pair | Light | Dark |
| --- | --- | --- |
| Bumble | Warm paper, ink-blue actions, localized pale-honey selections | Accepted midnight-ink/honey palette, unchanged |
| Slate | Cool near-neutral canvas, blue actions | Graphite, soft blue accents |
| Grove | Near-neutral stone, evergreen actions | Forest charcoal, sage accents |
| Iris | Near-neutral porcelain, violet actions | Soft charcoal, lavender accents |

Tide remains available unchanged. Summer Light and Summer Dark were removed at the user's request on 2026-10-26. The maintained registry has five pairs (ten modes).

Bumble Light canvas chroma drops from 0.058 to 0.004 at OKLCH lightness 0.970. New light canvases use chroma 0.003; new dark canvases use 0.012. This preserves a hint of temperature without turning the reading area into the accent color. All values are gamut-mapped and their resolved roles contrast-checked.

## Authoring rules

1. Start with the reading canvas and surface hierarchy. Check the whole event list, long prose, forms and notices before considering a palette successful.
2. Concentrate strong color in primary actions, links, focus and selected indicators. Keep ordinary panes, headers, fields and notices quiet. Do not add colored notice stripes or event-pane frames.
3. Tune light and dark separately. Retain role meanings, but do not invert hex values mechanically or require the same accent lightness in both modes.
4. Check selection, hover, pressed, focus, invalid, disabled and status examples together. Brand green or honey must not become the only cue for success or warning.
5. Use the existing semantic inputs and overrides. The compiler currently shares `accent` between link text and action fill, so a readable light-mode yellow accent would be forced darker. Bumble Light deliberately retains ink-blue actions and confines pale honey to a paired selection surface. A future independent honey button fill needs a separately documented paired role; do not bypass the gate with ad hoc CSS.
6. Preserve Manrope, geometry, square controls, markup and app behavior across pairs. Evaluate color using identical specimens.

## Review and verification

`tokens/themes.json` owns inputs; `tools/palette.py` and `tools/compiler.py` own resolution. The reference-site generator emits every library/screen/extension in every pair; the example builder now discovers the same registry instead of hardcoding three names. `/events/index.html` links to every complete app mode.

Run `npm run build` and `npm run check`. Inspect Bumble Light and every new pair on desktop and narrow viewports, including the filter panel, venue no-results state, keyboard focus and form errors. Contrast reports establish tested color-pair readability, not full WCAG conformance or subjective approval. Browser observations and remaining limits are recorded below after validation.


Initial validation on 2026-10-26, before Summer removal: build and check pass for kit 1.4.0, six pairs, 988 generated HTML files and 68,146 local references (before adding the reference-site research links). All 696 foreground/background checks pass (58 per mode); 14 kit tests, 24 app-template tests, 16 search assertions and 18 runtime contracts pass. Compared against HEAD: Bumble Dark inputs and resolved roles, Tide and Summer are unchanged.

Chromium desktop screenshots reviewed Bumble Light and both modes of Slate, Grove and Iris with the existing bounded panes, unframed event detail and photo context. At a 390 by 844 CSS-pixel viewport, spot checks covered Bumble Light venue no-results information, Slate Light/Grove Dark/Iris Light lists, and Iris Light's phone filter flyout. The flyout showed zero matching events while drafting an unmatched query, visible keyboard focus on a date field, and retained pinned actions. Resetting the viewport returned to the desktop composition. These are spot checks, not a full state/browser matrix. Firefox, Safari, physical devices, screen readers, forced-colors interaction and a complete visual review of every component state remain unverified for this change. Subjective palette acceptance remains the user's decision.
