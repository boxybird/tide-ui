# Events 1.1.5 — app JavaScript cleanup

This app-only refactor starts from `66ae1c7dedafbe8bc20a3e3bf95b59cb8d2cd389`. Tide kit1.3.0, reference-site sources, app styles, authored content, native URLs and accepted behavior remain intact.

## Changes and boundaries

- Added one small app-only shared-services home for optional storage, compatible keys, cached breakpoint/reduced-motion queries, URL/form state, destination URLs, count labels and primary clicks. Search refinement counting also has one pure owner.
- Removed the duplicate desktop month-jump listener. Navigation now handles calendar focus, pending-navigation cancellation and measured desktop-summary clearance once; tablet/phone behavior is preserved.
- Replaced the mixed `media.js` entry point with `preview.js`, moving inspection positioning out of venue context. Original/rough/no-photo modes, guarded parent messages, inspect positioning, preview-ready coordination and post-mount timing remain active. Historical keys/parameters are retained deliberately, rather than removed as apparently old names.
- Removed repeated storage/media/state/count logic, inherited empty scaffolding and the misleading legacy-clear variable name. The existing fallback CSS modifier and no-script controls remain unchanged. Filters/rail still own their original mount, close, resize, focus and gutter behavior.
- Registered all nine deferred scripts in execution order; added syntax, ownership and behavior contracts. No new runtime dependency, framework, router, service or kit component was introduced. See `examples/events/docs/RUNTIME.md`.

## Verification performed

All 420 generated pages remain byte-identical after applying only the intended script-tag changes to the predecessor: app-runtime after search-core and the media-to-preview filename change. All 77 protected files across the kit, reference site, app CSS, unique content fragments and sample data are unchanged.

Geometry and 55 computed style properties per HTML element match across 26 states: all six themes/modes, desktop/short/wide/tablet/portrait/phone/small-phone, filtered and zero-result previews, invalid date URL, venue and venue-empty, inspection placement, each photo mode, saved/help/submission. No horizontal overflow was recorded. Four screenshot pairs are pixel-identical: desktop, tablet, phone event and original-photo desktop. The default desktop screenshot was repeated at a fixed viewport after an initial raster difference despite identical geometry/styles.

Seventeen interaction states were performed on both preserved/current apps and matched exactly: desktop month jump and rail close, inclusive date/category draft, Enter commit and fetched preview, attendance focus, smooth native event selection, Back reading restoration, Reset draft, invalid date recovery, tablet draft and bidirectional focus wrapping, completed Escape rollback/focus, open-drawer resize rollback, phone Enter/result-count focus, venue-empty guide and scoped reset. Native gutter remains 10px at the measured Windows desktop: list and Show events both end at 866px in a 900px viewport.

No captured console warnings/errors. Eighteen Node runtime contracts cover script inventory/syntax, storage denial/values, historical keys, distinct media queries, URL/form normalization, label/refinement counts, desktop/tablet/phone/modified calendar navigation, pending cancellation, reduced motion, download/new-window behavior and guarded photo messages. The existing 24 app-template, 14 kit and 16 venue/search contracts remain required.

Measured records: [source/markup/pixel parity](parity-checks.json), [browser comparisons](browser-checks.json). Screenshots: [desktop](desktop.png), [tablet](tablet.png), [phone event](phone-event.png), [original photo](photo-original.png).

Browser evidence is Windows in-app Chromium. Native Firefox/Safari, physical-device and screen-reader checks remain deferred; reduced-motion and blocked-storage paths were exercised in Node rather than represented as browser coverage. The app continues to use authored sample data and existing static HTML navigation. Historical tags and preserved versions remain untouched.
