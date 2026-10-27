# Button normalization verification · Tide 1.6.0

Scope: regular/compact geometry, context-independent typography, text/icon/photo action states, canonical specimens, documentation and ownership checks. Existing app layout/template sources are outside this pass. The accepted theme inputs and existing resolved color roles are preserved; active colors are additive roles.

## Automated contracts

Root `npm run build` and `npm run check` pass. The check runs 7 local HTTP tests, 25 palette/contract tests and 28 app-template tests. All 600 configured contrast pairs pass. Portable checks exercise the concrete audit failures: quiet/plan geometry overrides, implicit viewport density, inherited type, consumer button overrides, missing state combinations, hover/active selector precedence and equivalent forced-colors selected selectors. Canonical output remains browser-JavaScript-free.

## Browser coverage

Rendered measurements and screenshots are stored as ignored evidence in `build/reports/button-normalization/`. The measurement function is development tooling at `tools/button-browser-probe.js`; no script is added to a specimen or consumer.

Chromium on Windows, 27 October 2026:

- All ten theme/mode matrices measured at 1280×900, 430×900 and 320×900: 30 passing runs, 32 cases per run. Regular padding/type, compact targets, 18px glyphs, border reservation and disabled-over-selected precedence match the contract; no document overflow.
- Identical action labels retain the same width/type in ordinary body, 16px reading-header and emphasized uppercase contexts. Longer labels wrap and grow vertically.
- All ten desktop matrices were visually inspected, with additional Bumble Dark phone/narrow screenshots. The reference library and canonical event recipe were inspected after the rebuild.
- Enabled primary, secondary, quiet, legacy icon and photo controls were clicked and observed in actual hover state in Bumble Dark. Their heights/padding remain stable.
- Space was held on those five action families and three selected examples to observe actual active styles. Primary hover/active colors differ; selected active uses a 2px inset keyline after correcting a hover-specificity regression.
- Tab shows real 2px focus with a 3px offset, including selected buttons. It skips native disabled examples. Pressed fixtures remain explicitly authored states.
- Source parity compared 99 existing app files with their pre-change bytes: none changed. Every pre-existing resolved palette role is unchanged; only the two active roles were added. App controls consume the updated shared CSS, so their appearance reflects the kit normalization.

Ignored evidence includes `browser-measurements.json`, `interaction-checks.json`, `active-checks.json`, `selected-active-checks.json`, `source-parity.json` and screenshots. Source guards and the CSS distribution remain within the existing performance budgets. No dependencies were installed.

Firefox/Safari, physical devices, screen readers, enlarged-root-font settings and actual forced-colors mode require their own runs. Static selector coverage does not establish those results or whole-product WCAG conformance.
