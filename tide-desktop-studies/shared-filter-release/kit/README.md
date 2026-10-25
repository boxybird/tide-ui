# Tide 1.3.0 — shared filter panel

Additive successor to 1.2.1. New Filter panel and documented search/filter compositions, all six theme/mode specimens, and an independently tested consumer. See [Search/filter contract](docs/SEARCH-FILTERS.md). Earlier distributions are retained unchanged.

# Tide HTML + CSS kit · 1.2.1

Version 1.2.1 documents the unframed event-list and individual-event composition: no decorative outer borders or rounded clipping shells are added for larger screens. Shared component styles are unchanged; the correction is in app 1.3.1. The prior 1.2.0 archive remains preserved.

Version 1.2.0 adds scoped Prose and a reusable Content page layout, with a realistic help page and rich-HTML specimen in every theme/mode. Open `index.html#content-pages` or read [the HTML/CSS contract](docs/CONTENT.md). Existing primitives, theme inputs and app visuals are preserved; the previous 1.1.0 package remains in `dist/`.

This is the maintained kit consumed directly by the app playground. The approved original remains a preserved reference in `tide-ui-kit/`. Version 1.1.0 adopts reusable discoveries from the app: native disclosure, calendar groups, selected-preview card state and result-summary elements. The neutral In view label reuses Badge. See [adoption and ownership](docs/ADOPTION.md); type, spacing, radius, target and theme inputs are preserved.

The selected Tide/Date Line structure, implemented as a themeable, framework-free HTML/CSS foundation. Three named themes each have light and dark modes. A system mode follows the device preference. The earlier studies remain untouched.

## Open

Use the app server and open <http://127.0.0.1:4186/kit/index.html#adopted-patterns>. The library includes Foundations, Components, Screens, Coverage, Tokens, Themes and Extend. Theme links retain the selected section. Open a screen separately for its full mobile composition. The files are static and portable; use the local server for consistent font and asset loading. The original reference on port 4185 remains preserved.

The library and all component/screen specimens use plain HTML; no browser JavaScript, dependency installation or application framework is required. Native inputs, radio/checkbox selection, reset, required-field validation, disclosure controls and links work. Search results, saves, submissions and confirmations are illustrative fixtures, not working services.

## Use in a page

```html
<!doctype html>
<html lang="en" data-theme="tide" data-mode="dark">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="css/tide.css">
  </head>
  <body class="tide">
    <a class="tide-button" href="event.html">View event</a>
  </body>
</html>
```

Copy `css/tide.css` and `assets/` with the same relative folder arrangement; font and texture URLs are relative to the stylesheet. Include the Manrope and icon licenses from `licenses/`. The delivered entry point is a generated single CSS bundle, so a consuming page does not pay a stylesheet-import waterfall. Keep the source CSS modules when developing the kit. `css/docs*.css` belongs only to the reference site.

Use `data-theme="tide|summer|bumble"` and independently choose `data-mode="light|dark|system"`. Omitting data-mode also follows system appearance. Put both on the document root. Persistence and any application-level mode picker belong to the consuming application; this CSS kit does not store preferences.

## What stays fixed

- Manrope, the existing hierarchy and measured line heights. Body 14/24, form values 16/24, card headings 24/32, page headings 28/36, event headings 36/40 at the default 16px root size.
- A rem-based 4px spacing rhythm, 24px insets, edge-to-edge touching cards, 44px icon targets, 48px fields/actions.
- Square 2px control corners and 4px documentation/panel corners. Flat surfaces.
- Full-screen event photography with richer detail below it. Clear event headings even when a photo is missing.
- Uniform neutral callout outlines, with explicit status wording and no colored left stripe.

Dimensions scale with the browser's font preferences and zoom. Optical exceptions are explicit (11px labels, 26px date numerals, a 1px rule, 2px corners/focus outlines); they are not a second ad hoc spacing system. Theme definitions cannot set typography, spacing or radii.

## Token contract

| Level | Example | Owner |
| --- | --- | --- |
| Fixed primitive | `--tide-space-6`, `--tide-font-size-card`, `--tide-radius-control` | `css/tokens.css` |
| Theme input | `canvas: [0.925, 0.06, 65]` in an OKLCH light-mode seed | `tokens/themes.json` |
| Mode-specific palette value | `--tide-palette-canvas-light` / `--tide-palette-canvas-dark` | Generated `css/themes.css` |
| Stable semantic role | `--tide-color-canvas`, `--tide-color-text-primary` | Components consume this level |
| Component extension point | `--tide-panel-padding: var(--tide-space-6)` | That component's documented contract |

Names describe a purpose, not a color or a current theme. Components do not read palette implementation tokens or contain selectors for a specific theme. Light and dark share the same semantic names; `light-dark()` resolves the mode using `color-scheme`.

The theme source contains OKLCH triples: lightness 0..1, chroma >=0, hue in degrees. CSS is emitted as `oklch()` colors, not hex/RGBA. `color-mix(in oklab, …)` supplies the primary hover state. Alpha OKLCH is used for the photo scrim. See [theming](docs/THEMING.md) for the complete authoring workflow and its limits.

## Files

```text
css/tide.css           generated single-file entry point and cascade order
css/tokens.css         fixed primitives
css/themes.css         generated paired theme colors
css/base.css           font, type defaults, focus and user preferences
css/layout.css         composition, screen anatomy and spacing between blocks
css/components.css     BEM blocks, elements and state modifiers
css/utilities.css      small explicit helpers
css/content.css        scoped rich text and informational-page composition
templates/             independent BEM HTML source of truth
tokens/themes.json     editable theme inputs (three themes, two modes each)
tokens/resolved.json   generated machine-readable colors
tools/build.py         contrast gate, CSS bundle and static-page generation
tools/check.py         structural checks for the distributable
tools/test_palette.py  meaningful color/contrast/schema regression checks
extensions/           working additive panel example
docs/                  naming, theme, component and compatibility guidance
qa/                    contrast, layout and screenshot evidence
```

Each `theme-mode/` directory contains the same library and fourteen identical screen/specimen compositions. These generated fixtures are deliberately repeated so there is no runtime script or query-string dependency. Edit a BEM source in `templates/`, not each generated copy. `tools/import_reference.py` is a historical, one-time migration helper; do not rerun it during normal development.

## Build and check

Python 3.10+ and Node 18+ are sufficient. They are development utilities; the delivered CSS/HTML needs neither at runtime.

```text
python tools/build.py
python tools/build.py --check
python tools/check.py
python -m unittest discover -s tools -p "test_*.py"
node server.cjs
```

The compiler validates all theme definitions and pairs before writing generated files. `--check` performs the same validation and fails if generated files are stale. A failed contrast check is a failed build. The structural check catches missing assets/links, duplicate IDs, legacy/unprefixed classes, inline styles, scripts, unbound descriptions and missing labels in the HTML fixtures. It also checks shared content/structure across all six modes.

These checks are targeted safeguards, not a claim of complete WCAG conformance. Native platform rendering, keyboard flows, uploaded images, and real application behavior need their own review. Actual browser observations and the cross-engine compatibility research are recorded separately in [QA](qa/REPORT.md) and [browser support](docs/COMPATIBILITY.md).

## Extend

Read [component contracts](docs/COMPONENTS.md), [adoption rules](docs/ADOPTION.md) and [extension rules](docs/EXTENDING.md). Reuse an existing block first. A new reusable block needs its CSS/HTML home, registry entry, state/behavior contract and fixtures in every theme/mode; update the consuming app and remove duplicated styling in the same change. Additive CSS belongs under `@layer tide.components.extensions`. Do not add global sibling margin rules or mutate the shared foundations to solve a single component's problem.

This kit is a UI foundation, not a ticketing backend, authentication system, form processor or application accessibility audit. Coverage notes distinguish included static layouts from future journeys. All event details are fictional. The locally stored assets and licenses are reused from the selected studies.

The adopted disclosure uses the existing Radix ChevronDown asset, copied to `assets/icons/ChevronDownIcon.svg`; its MIT licence remains in `licenses/radix-icons-MIT.txt`. A standalone extracted kit can use its own `node server.cjs` preview; use the printed local URL.
