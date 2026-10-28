# Filter-panel spacing · Lineup 2.1.9

This application patch capitalizes the visible Search & Filters headings, restores mobile/tablet drawer content clearance, and adopts Tide's existing compact Category grouping. Tide UI stays at 1.12.0. No browser scripts, new shared recipe or consumer runtime is introduced.

## Composition and ownership

The canonical `tide-filter-panel--rail` body is intentionally flush. Lineup uses that same rail for its permanent desktop column and native drawer. `filter-rail.html` now wraps the filter content in a private `tide-app__filter-content` div. Below 75rem, `filters.css` adds `var(--tide-space-6)` (24px) top padding to that wrapper. The public body/footer keep their canonical appearance. At desktop widths the wrapper has no padding, preserving the search field's placement.

Category now uses `fieldset.tide-fieldset` with adjacent `label.tide-choice` rows, matching the Category disclosure in Tide's `templates/adopted-patterns.html` and `/site/bumble-dark/frames/app-patterns.html`. The choices retain Tide's 44px minimum target and typography. Removing the generic Stack composition removes its extra 16px between rows: row starts are 44px apart rather than 60px. The When fieldset retains Stack for its hints and date fields.

Tide also has roomier form-section and stacked panel specimens; these are different compositions. This patch adopts the existing compact disclosure recipe rather than changing a shared spacing token or overriding choice internals. The previous strict-alignment record describes the earlier Stack adoption; this contract records the current application choice.

Both the drawer title and desktop utility label are authored by Lineup and now use Search & Filters. The native popover, one form/control set, associations, Reset, Close/Escape dismissal, pinned footer and responsive placement remain unchanged. Consumers of the previous release should retain their integration identifiers and use the ordinary source-update workflow; the added wrapper does not change the form or route contract.

## Verification · 2026-10-28

In-app Chromium on Windows, with actual viewport dimensions asserted:

- 30 theme/viewport spacing cases: all five themes in light/dark at 390, 1024 and 1440 × 900. Drawer search clearance is 24px; desktop content remains flush at its existing origin. Choice rows are 44px with no extra inter-row gap. Each page has one search input, one h1, no scripts and no horizontal document overflow.
- Four boundary/size cases: 320×500, 768×900, 1199×900 and 1200×900. Clearance changes from 24px in the drawer to zero additional inset at the permanent rail boundary. The short phone body scrolls to the last choice while the footer remains at the viewport bottom.
- Native global Reset clears entered query/date/category values. Close and Escape dismiss the drawer and return focus to Filters. Widening an open 390px drawer to 1440px preserves entered text and exactly one control set; the panel matches the reserved column and the content wrapper has no desktop padding.
- Sunshine Theater at 1024×900 retains the same spacing and its venue-owned Reset link. No route or form association changed.

The canonical Category disclosure in `/site/bumble-dark/frames/app-patterns.html` measured 44px rows and zero inter-row gaps, matching the updated application. The roomier full-page filter specimen uses a different form-section composition and is not the compact-group reference.

At 1440×900 in Bumble Dark, the settled before/after rectangles are identical:

| Desktop element | x / y | Width / height |
| --- | --- | --- |
| Search form | 32 / 193.667px | 252.531 / 76px |
| Search label | 40 / 193.667px | 220.531 / 20px |
| Search input | 40 / 221.667px | 220.531 / 48px |

At 390px the heading-to-search gap changed from 0 to 24px. Category row starts changed from 60 to 44px while the choice targets stayed 44px high. Transitional readings immediately after viewport changes were discarded from the before/after comparison; accepted baseline and comparison records use the settled layout.

`npm run build` and `npm run check` passed, including 72 Tide tests, 42 Lineup tests and the HTTP suite. The protected Tide/reference-site/shared-tooling fingerprint remains unchanged. Expanded measurements and screenshots are ignored artifacts under `build/qa/lineup-filter-panel/`.

Firefox/Safari, physical devices/software keyboards, screen readers, forced colors, zoom and a current-run system reduced-motion preference change remain unverified. This spacing/native-behavior check is not an accessibility-conformance claim.
