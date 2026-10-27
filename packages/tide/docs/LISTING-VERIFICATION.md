# Listing normalization verification · 2026-10-27

The [listing contract](LISTINGS.md) defines kit 1.9.0 type, spacing and native/static state boundaries. All 99 existing application files match their pre-pass SHA-256 hashes. Resolved palettes are unchanged, including Bumble Dark. The application remains 2.0.4; `main` is the only branch.

## Portable verification

Root `npm run build` and `npm run check` cover the distribution, all 988 generated HTML documents and local references, zero browser JavaScript, existing byte budgets and 600 contrast pairs. The suite contains 57 kit tests, 28 application template tests and seven local HTTP tests. Nine new listing contracts cover type/context/state geometry, date labels and unknown dates, unique IDs, native link/action nesting, truthful authored group counts, hidden separators, escaped values, registered ownership and all-theme rendering.

Card ownership now rejects type/padding/layout redefinitions while accepting only the existing preview-label display and preview-outline suppression choices. Mutation tests reject additional properties/values in those exceptions. Tests also read current app CSS to verify that no application edits are needed. Calendar/date/result ownership remains registered, with their complete supporting CSS homes recorded.

Existing performance budgets are retained. The main library links to the full listing matrix while retaining its earlier previews; no full matrix is duplicated into the already large library page. Build-time card/date templates are escaped authored fixtures, independent of application data/templates/runtime.

## Rendered and native checks

In-app Chromium: ten modes at 1280×900, 430×900 and 320×900. All 30 runs pass, each measuring 48 component cases, including four nodes hidden directly or by an ancestor. Checks cover root/slot type, card insets and copy rhythm, fixed metadata gaps, date-column alignment, covering-link geometry, independent action layers, unchanged preview geometry, calendar title/count/jump geometry, static/sticky/hidden states, result wrapping and context equality. There is no horizontal document overflow.

Inspected screenshots include Bumble Dark wide/narrow cards, Tide Light 320px result summaries and the Bumble Dark calendar viewport. The narrow review caught orphan decorative metadata dividers when a field wrapped; legacy nodes are now hidden, new recipes omit them, and fixed gaps provide separation. Inter-card visible separators remain intact. Long titles/venues/prices wrap and unknown schedules retain ordinary explanatory text.

Native keyboard focus moves from covering link to independent action and back. Cover-link focus paints the title and shows the 2px inset outline; the declared -3px offset computes to -2.66667px with engine pixel quantization. The independent action click reaches its saved-example target rather than the detail target. A card click reaches the native detail target. Month jumps focus their actual group section. After scrolling settles, the 384px-high calendar viewport has a 686px scroll extent, scrollTop 302 and a zero header/scroller top delta: the header is pinned in its native scrolling ancestor. The early sample before native scrolling settled is retained separately in the artifact.

Hover/active declarations are source-guarded and use existing audited text roles; no simulated hover classes, article button roles or live count engine are added. Static status/preview words and native time labels are explicit.

## Adjacent checks and limits

Existing Feedback, Form and Button browser probes pass in Bumble Dark at their recorded narrow/wide smoke widths. The application desktop smoke retains one filter set, zero scripts, no horizontal overflow and the left pane ending 24px above the 900px viewport bottom. Native November navigation reaches and focuses its original month ID. At 430px the native filter drawer opens with Close focus, closes and returns focus to Filters. These are smoke observations, not an application-layout redesign or complete route audit.

Ignored local evidence is in `build/reports/listing-normalization/`: source/palette parity, thirty measurement runs, native observations, app/prior-component smoke results and reviewed screenshots. `tools/listing-browser-probe.js` is read-only development tooling and is never served.

Firefox/Safari, physical devices, screen readers and an actual OS forced-colors session were not run. Custom nonzero host offsets and pointer-held active feedback have source coverage rather than exhaustive engine coverage. Dynamic counts, announcements, preview changes, matching and save behavior belong to consumers and are not implemented by these specimens. Targeted checks do not establish whole-product accessibility conformance.
