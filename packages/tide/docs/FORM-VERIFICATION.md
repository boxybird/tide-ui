# Form normalization verification · 2026-10-27

## Select/disclosure follow-up · 1.7.1

Fields and disclosure summaries now share 48px regular geometry, 11px vertical / 16px horizontal padding, a 24px line box and the same centered 18px source chevron. Single-selects reserve an additional glyph-plus-gap space on their trailing side; logical insets mirror in right-to-left layouts. Disclosures keep 14px weight-550 labels; field values keep 16px weight-400 text. Multiple/size-based native list boxes retain native chrome and intrinsic height. Application sources/layouts and theme inputs remain unchanged.

The updated read-only probe measures 48 cases in each of ten modes at 1280×900, 430×900 and 320×900. All 30 runs pass, including shared masks, insets, regular height, listbox exclusion, explicit size-one selects, disabled chevrons, context isolation and zero horizontal overflow. Existing performance budgets remain unchanged. Portable checks now include the single-select/listbox boundary and shared geometry contract (36 kit tests; 71 tests across the full root suite).

Native ArrowDown selection, popup keyboard choice, Tab focus/outline and disclosure Enter/Space with indicator rotation were verified. Native popup activation was observed with both DOM `:open` and the accessibility tree's expanded select/menu state. Repeated popup/shortcut automation observations were inconsistent, so this does not establish comprehensive OS menu/shortcut coverage. Firefox/Safari, screen readers, physical devices and an actual forced-colors session remain deferred.

Local ignored evidence: `build/reports/select-disclosure-alignment/` contains app-source/theme-input hashes, 30 rendered measurement runs, native interaction observations and the reviewed alignment screenshot. The checks retain the existing zero-browser-JavaScript boundary. `main` remains the only branch.

## Initial pass · 1.7.0

The canonical contract is [FORMS.md](FORMS.md). This pass changes kit presentation, canonical specimens and documentation/checks. All 99 existing files under `examples/events/` match their pre-pass SHA-256 hashes, including the user's existing work. Theme inputs and the accepted Bumble Dark palette are unchanged. The app stays at 2.0.4; the kit is 1.7.0. `main` is the only branch.

## Portable checks

Root `npm run build` and `npm run check` cover the CSS distribution, ten theme/mode libraries, all 968 HTML documents, local links/assets, zero browser scripts, existing byte budgets and 600 contrast pairs. The suite includes 35 kit tests, 28 app template tests and seven preview HTTP tests. Ten new form contracts cover inherited typography, state/context geometry overrides, invalid/disabled order, inherited fieldset disabling, associated errors and linked destinations, native/static behavior boundaries, indicator ownership, keyboard-active chip feedback and shared all-theme rendering.

The kit stylesheet remains inside the existing 100,000-byte raw / 14,000-byte gzip limits. No performance budget was raised. Source checks are targeted regression guards, not an accessibility-name engine or proof of every computed state.

## Rendered measurements

In-app Chromium: all ten theme/mode combinations at 1280×900, 430×900 and 320×900. Each of the 30 runs measures 42 cases, plus labels, hints, errors and legends. Checks cover field and compact geometry/type, context isolation, native glyph sizes, disabled precedence over checked/invalid states, disabled fieldsets, upload/field danger boundaries, exactly one disclosure indicator, untouched required controls and horizontal overflow. All pass.

Native selects retain platform appearance: Chromium computes `normal` leading despite the declared 24px, with the expected font, padding and 48px box. Native file-selector buttons measure the compact recipe; filenames may truncate within the available width at 320px. Browser pixel quantization can produce fractional computed border widths from the reserved 1px input. No custom select or file widget was introduced.

Screenshots inspected: Bumble Dark desktop and 320px upload/context, plus Tide Light 320px linked errors. Narrow labels, guidance and errors wrap without document overflow. The docs grid aligns specimens at the start so short chips/actions do not stretch to the longest adjacent panel.

## Native behavior

Verified in Bumble Dark: checkbox Space; radio ArrowRight and native Reset; checked chip selection and Reset; actual keyboard focus with the shared outline; disabled field/select Tab skipping; disclosure Enter/Space, rotating indicator and Tab into revealed content; enabled field hover, invalid-hover precedence, summary hover and held active state. Holding Space on a native chip input exposed a missing active propagation rule during verification; the corrected selector follows `input:active` and now produces the 2px inset at the unchanged 44px height. A portable guard covers that regression.

Required text/file submission exposes browser constraint validation and `:user-invalid` boundaries, without authored `aria-invalid` on untouched inputs. Reset clears the native interaction state while authored error examples remain authored. Summary error links focus their actual input destinations. A local chooser selected `quiet-dots.png`, replaced it with `ink-after-dark.png`, and native form Reset cleared the filename. No file was submitted or uploaded.

Application smoke: default desktop at 1280px retains one original filter/control set, a bounded left pane ending 24px above the viewport bottom, no horizontal overflow and zero browser scripts. At 430px the native Filters drawer opens, receives Close focus, closes and returns focus to Filters. Its source files are unchanged; this is a smoke check, not a renewed audit of every app route/layout.

## Evidence and limits

Ignored local evidence lives in `build/reports/form-normalization/`: baseline/source-parity hashes, browser measurements, native interactions, app smoke observations and reviewed screenshots. `tools/form-browser-probe.js` is a development-only read-only measurement function, never served as browser JavaScript. Run it through Browser Use on the generated `form-states.html` pages; portable checks need no additional dependencies.

Firefox/Safari, physical devices, screen readers and an actual OS forced-colors session were not run. Native chooser rendering and validation timing can differ by platform. Forced-colors fallbacks are source-reviewed; dynamic validation announcements, consumer-managed summary focus, file-content/size validation and application behavior remain consumer responsibilities. No whole-product accessibility conformance is claimed.
