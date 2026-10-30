# Compact map previews · Lineup 2.4.1

When List and Map are separate views (below 60rem), a marker opens a small venue preview while the map remains visible. The preview contains the venue name, type, authored event count and a native View venue details link. Close, Escape or a pointer press outside dismisses it. Keyboard dismissal returns focus to the invoking marker. Opening a preview does not change the URL fragment or map camera.

At 60rem and above, both panes are visible: markers remain native links to their venue row, and cards remain native links to the adjacent map point. No preview popup is exposed. Crossing into that layout closes an open preview. Fragment changes also dismiss open previews, including leaving Map for List. Compact list cards continue to open the venue and its events directly.

## Component ownership and positioning

`venue-map-panel.html` is one registered shared partial rendered for the six venues. It consumes the unchanged Tide Panel, Panel title/description, Link and quiet icon Button. The private outer popover supplies geometry only; Panel type, 24px padding, 12px gaps, surface, border and radius remain Tide-owned. Counts come from the same structured event collection as the venue list, not a new fixture copy.

Native `popover="auto"` supplies non-modal dismissal and focus behavior. The button/popover relationship supplies the CSS anchor: the panel prefers the area above its marker with 8px separation, then tries below/side-aligned placements when constrained. A 16px viewport inset keeps it away from the edges. Browsers without anchor positioning retain a centered native popover; browsers without popover support retain the existing marker-to-list link. Browser support beyond the tested Chromium build remains unverified.

The map module only closes popovers when entering the split layout or changing the fragment. It does not intercept marker clicks, construct panel content, rewrite destinations, create a modal focus trap or change camera behavior. The native preview also remains available over the illustrated map when map enhancement is disabled or fails. Pinned map dependencies and geographic fixtures are unchanged.

## Verification

- `npm run build` and `npm run check` pass: all 138 tests and generated-document checks. The existing venue test now checks native popup invokers, dialog labels, unchanged Panel ownership, Close targets and correct per-venue links; CSS compaction parity covers the map stylesheet too.
- At 390×844, all six keyboard-opened previews preserve `#venue-map`, leave the list hidden, expose exactly one popup, fit the viewport and return focus to their marker after Escape. Pointer Close and outside dismissal also pass.
- The Sister preview opens its current nine-event document, and Back returns to Map. Back from an open map preview to the preceding List fragment closes the popup and restores List. Compact list cards still open their venue directly.
- Ten theme/mode pairs at 390×844 retain the current map state and unchanged Panel values: 24px padding, 12px gap, 20px title, weight 580. All tested previews fit the viewport.
- Responsive checks cover 320×568, 390×844, 543×780, 544×780, 959×800, 960×800, 1280×720 and 844×390. Narrow views expose six preview buttons and no marker-to-list links; split views expose six links and no preview buttons. Long-name panels fit after camera fitting settles, including the short/narrow layouts; placement was rechecked after the fit animation rather than relying on transient geometry.
- An open preview closes when resizing into the split layout. Desktop Dry Heat card-to-marker and marker-to-row selection preserve the fixed 720px document with zero popups.
- `?map=off` retains native preview opening and the correct Sister link over the illustrated fallback.
- All 135 protected Tide, reference-site and shared-tooling files remain byte-identical. Map CSS is 4,831 bytes after lossless compaction; the map module is 8,190 bytes. Existing budgets, pinned vendor bytes and geographic fixtures are unchanged.

Evidence is retained under ignored `build/qa/mobile-map-preview/`. Windows Chromium is the current browser target; Firefox, Safari, physical touch devices and screen-reader testing remain unverified. Pointer and keyboard actions were tested; these results do not claim a physical touchscreen test.
