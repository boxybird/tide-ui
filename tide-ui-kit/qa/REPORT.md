# Tide HTML/CSS kit — verification

Date: 22 October 2026. Result: targeted checks passed. The selected Tide/Date Line layout and every prior study are preserved; this kit is an isolated sibling.

## Contract and structure

- Three named themes (Tide, Summer, Bumble), each with light/dark definitions; system appearance is independent from the theme.
- A single generated CSS entry point with explicit layers. Modular authoring sources remain separate; the browser does not load an import waterfall.
- BEM HTML sources, no inline component styles and no browser scripts/framework runtime.
- Eleven identical screen/state templates per mode. Same structure, content, type, spacing, radii and target sizes across all six versions.
- Neutral, equal borders on all four sides of every callout. Explicit wording retains meaning.
- An additive panel example uses the existing contract in all six theme/mode combinations.

## Automated evidence

- `contrast.json`: 324 passing WCAG 2 foreground/background checks across six mode palettes. Normal-size text is checked at 4.5:1; meaningful control/focus boundaries at 3:1. Includes the actual OKLab hover recipe, selected controls, status text/badges and the photo context's opaque base.
- Eight palette regression tests: known WCAG values, sRGB gamut mapping, changed orange backgrounds, foreground polarity, incompatible surface rejection, shipped themes, missing modes/geometry injection, and duplicate names/unknown role rejection.
- `structure.json`: local reference/fragment checks, valid prefixed BEM classes, unique IDs, labelled inputs, bound descriptions, no scripts/inline styles, no private palette consumption from components, no raw component colors, no unbound CSS tokens, and identical screen markup/content across themes.
- `tools/build.py --check`: generated outputs match source inputs.

The theme checks found and fixed a real state edge case: mixing a just-passing action background toward its foreground could make hover fail. The state recipe now moves the background away from the label and measures both normal and hovered/pressed pairs.

## Rendered verification

Actual rendering surface: local in-app Chromium browser. No extension, headless browser, physical phone, Firefox or Safari session was used.

- `browser-390.json` / `reference-comparison.json`: all eleven refactored Tide screens compared against the preserved Tide reference at 390×844. Text, measured card/title/meta/field/action/callout/hero/detail positions, dimensions and type metrics match (0.1px comparison tolerance).
- `themes-390.json` / `theme-invariance.json`: all 66 theme/screen combinations at 390×844; no horizontal overflow and no measured geometry/content differences between themes. Stylesheets were awaited before measurements; fonts reported loaded.
- `themes-320.json`: all 66 screen combinations and all six library pages at 320×740; no horizontal overflow. Callout side colors/widths were checked for equality.
- `resilience-320.png`: an independent 320px fixture with a 200% root font size (32px), an exceptionally long title and unbroken word, wrapping label/help text and long button label; no horizontal overflow. This is an enlarged-root-text test, not a claim of a physical browser zoom session.
- Native filter checkbox changed and Reset restored its initial state. Submitting with an empty required title stayed on the form and focused that invalid field.
- Theme navigation retained the selected Components section. The Tokens section also displayed the correct section-preserving theme links.
- System-mode page matched the current light OS preference. Explicit light and dark modes were rendered throughout the fixture matrix. The OS preference itself was not changed during testing.
- `CSS.supports()` confirmed OKLCH, light-dark and color-mix in the rendered engine.
- Search, status/callout, event hero, submission and documentation screenshots were inspected. Comparison boards are `preview.png`, `compare-states.png` and `compare-01-event.png`.

## Compatibility research and limits

The core features are supported by current Chrome, Firefox and Safari according to the primary data linked in `docs/COMPATIBILITY.md`. Firefox currently falls back from optional `text-wrap: pretty` to explicit ordinary wrapping. Firefox and Safari were not physically rendered here; their native date/time/select styling, keyboard behavior and wrapping still need native-engine checks before a public release.

The contrast gate validates named color pairs, not a complete product's WCAG conformance. Uploaded photographs can change local contrast beneath a scrim; new images need review or a solid fallback. Forced-colors and increased-contrast rules are included but were not physically exercised in those OS modes. Live search/save/upload/submission/notification behavior is outside this static HTML/CSS kit.

No prior collection was overwritten, nothing was published, and no application data was transmitted.
