# Events 1.1.1 â€” app CSS refactor

This is an app-only maintenance patch against commit `003885b82e24e4a753a34caf7364a9c89c5d9d1b`. The approved appearance and behavior are retained. Tide kit 1.3.0, its 59 source files, templates, themes, assets and compiler are unchanged.

## What changed

Five ordered stylesheet modules replace the concatenation of historical study layers. `consumer-manifest.json` registers their cascade order and five private class families. The app builder emits one stylesheet; public kit styles remain a separate shared dependency. App CSS source falls from 40,434 to 23,407 bytes (42%).

All 60 authored pages and runtime selectors now use purpose-based app, lineup, filter drawer and venue classes. Inactive panorama/open-book, width, calendar/index and middle-rail comparison variants are removed. The heading helper composes only the selected lineup hierarchy at every width. `media.js` retains rough/original/absent-photo preview behavior. Existing session preference namespaces and the parent photo-preview message remain compatible.

The bounded list, natural right document, unframed panes, 24px-plus-native-gutter clearance, aligned Show events actions, measured sticky offsets, feed isolation and one original set of filter controls retain their contracts. Saved/help/submission samples keep their existing layouts and content.

## Actual verification

- Compared computed geometry and 55 standard style properties on every HTML element across 22 states: desktop, short/wide windows, tablet, portrait tablet, phone list/event, 320px phone, venue/zero-results/wrapped query, help/saved/submission, six theme modes, collapsed rail and open tablet drawer. No differences in the recorded fields or horizontal overflow.
- Compared five viewport screenshots: desktop, tablet, phone list, phone event and venue. The matched captures are pixel-identical. Tablet was repeated at a fixed matching viewport after the first raster captures differed while DOM geometry matched.
- Confirmed all 60 authored pages retain identical content, public kit classes, links, IDs, form associations and native semantics after accounting for private names and stylesheet bundling.
- Exercised draft count versus applied feed, Escape cancellation/focus restoration, one/zero results, Reset, venue scope/exit, inclusive dates/categories, invalid date prevention, open-drawer resize rollback, month jumps/sticky stacking, smooth event selection and browser Back restoration. All recorded checks passed; no captured console warnings/errors.
- Desktop at 1440Ã—900: occupied native gutter 10px; list and Show events bottom both 866px, leaving 34px. Month jump lands at 249px, immediately below the summary. Browser Back restores the recorded 900px document reading position.

The [browser record](browser-checks.json) and [source/pixel record](source-and-pixel-checks.json) contain the measured results. Screenshots: [desktop](desktop.png), [tablet](tablet.png), [phone list](phone-list.png), [phone event](phone-event.png), [venue](venue.png). The 22-case comparison is a recorded Chromium observation, not a replacement for native browser coverage.

Normal source checks now also reject historical app selectors, unregistered stylesheet modules and unused private app CSS classes. The existing palette/contract tests and venue/search assertions remain required. Firefox, Safari, physical-device and screen-reader checks remain deferred; no such tests are claimed here.

No historical tag or preserved original was modified. The pre-refactor app remains recoverable from the baseline commit; complete design history remains at `design-history/2026-10-25`.
