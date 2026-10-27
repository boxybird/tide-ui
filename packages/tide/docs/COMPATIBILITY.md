# Browser support and evidence

Target: the latest stable Chrome, Firefox and Safari releases, including their modern mobile engines. Feature compatibility was researched on 22 October 2026 using MDN's browser compatibility data and the primary specifications/documentation below. No preprocessor, runtime CSS-in-JS, experimental flag or vendor-only layout feature is required.

## Core features

| Feature used | Chrome | Firefox | Safari | Purpose |
| --- | --- | --- | --- | --- |
| OKLCH colors | 111+ | 113+ | 15.4+ | Perceptual palette inputs and CSS output |
| `color-mix()` (two colors, OKLab) | 111+ | 113+ | 16.2+ | Checked primary-action hover state |
| `light-dark()` (color values) | 123+ | 120+ | 17.5+ | Stable semantic roles in both modes |
| Cascade `@layer` | 99+ | 97+ | 15.4+ | Explicit ordering without specificity escalation |
| `:has()` | 105+ | 121+ | 15.4+ | Native choice selection, card hover, section-preserving theme links |
| Small viewport units (`svh`) | 108+ | 101+ | 15.4+ | Mobile photo opening with stable viewport height |

The CSS also uses Grid/Flexbox, custom properties, logical properties, `:where()`/`:is()`, `:focus-visible`, range media queries, native `accent-color`, `font-display`, variable fonts, and user-preference media features. These are supported by the requested current engines. `text-wrap: balance` is supported across the target engines. The one optional typography enhancement is `text-wrap: pretty`: the current MDN data still lists Firefox as unsupported. An explicit `text-wrap: wrap` declaration precedes it, so Firefox keeps ordinary wrapping. Content does not depend on a particular line-break algorithm.

The minimum versions above describe individual feature support, not a promise to support all older combinations down to those versions. The kit's target remains current stable engines. The support data is not a visual test result.

## Deliberate choices

- Relative colors are available in current engines, but emitted OKLCH role values are resolved ahead of time so the same values can be measured by the build gate and inspected in tokens JSON.
- `contrast-color()` is present in current Chrome/Firefox/Safari compatibility data. It is not used to choose the kit's foreground hierarchy because its black/white result does not define branded secondary text, status colors or action states. This is a palette-contract choice, not a claim that the function lacks current support.
- Only the color form of `light-dark()` and the two-color form of `color-mix()` are used; newer extensions to those functions are not required.
- No View Transition, animation, anchor positioning, customizable select, scroll-driven animation or other unrelated feature is added to this static kit.
- Native controls are kept native. Platform date/time/search/select rendering can differ even when the CSS feature set is fully supported.

## Actual verification

Kit 1.7.0 adds optional `:user-invalid` styling and an SVG-mask disclosure fallback. Kit 1.7.1 aligns collapsed native selects and disclosures with a shared chevron and padding; the select popup and selection behavior remain native. Explicit `aria-invalid` and browser constraint-validation messages remain available if interaction-based invalid styling is unsupported. See [form verification](FORM-VERIFICATION.md) for Chromium measurements, native select line-height reporting and remaining engine/assistive-technology limits. The [normalization status](NORMALIZATION-STATUS.md) records completed passes and remaining audit work.

The local in-app Chromium browser is the rendering test surface available for this handoff. `CSS.supports()` confirmed OKLCH, light-dark and color-mix support there. Layout, theme navigation, native form behavior and screenshot observations are recorded in `qa/REPORT.md` and its linked evidence.

Firefox and Safari support is verified at the feature-data level; those engines were not physically run in this environment. A release should still receive native Firefox and macOS/iOS Safari visual/keyboard tests, especially date/time fields, forced-colors/high-contrast handling and text wrapping. Do not label those as passed engine tests based only on this document.

## Primary sources

- [MDN browser compatibility data — CSS colors](https://github.com/mdn/browser-compat-data/blob/main/css/types/color.json)
- [MDN — light-dark()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/light-dark)
- [MDN — color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix)
- [MDN — contrast-color()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/contrast-color)
- [MDN compatibility data — cascade layers](https://github.com/mdn/browser-compat-data/blob/main/css/at-rules/layer.json)
- [MDN compatibility data — :has()](https://github.com/mdn/browser-compat-data/blob/main/css/selectors/has.json)
- [MDN compatibility data — length units](https://github.com/mdn/browser-compat-data/blob/main/css/types/length.json)
- [MDN compatibility data — media features](https://github.com/mdn/browser-compat-data/blob/main/css/at-rules/media.json)
- [MDN compatibility data — text wrapping](https://github.com/mdn/browser-compat-data/blob/main/css/properties/text-wrap.json)
- [web.dev — Color themes with Baseline CSS features](https://web.dev/articles/baseline-in-action-color-theme)
- [W3C — WCAG 2.2, Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [W3C — WCAG 2.2, Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

Contrast checks use the WCAG 2 relative-luminance calculation in sRGB. OKLCH lightness alone is not treated as a contrast ratio. Targeted checks do not establish whole-product WCAG conformance.
