# Half Split · Keep your place

Open <http://127.0.0.1:4187/half-split-refinements/index.html>. Three isolated refinements of the selected Half Split desktop layout:

1. **Steady Header** keeps the header and both left panels in the same viewport positions while the event scrolls naturally.
2. **Pinned Apply** adds a bottom action dock for the original Apply filters and Clear all controls. Options scroll above the dock.
3. **Pinned Search** also keeps the original search form visible as the filter options scroll past it.

The original Half Split, width comparisons, Wide Open collection, app 1.3.1 and kit 1.2.1 are preserved. The same 48 events, half-split widths, gutters, insets, fonts, colors and component styling remain. Changes start at 75rem/1200px; mobile and tablet retain the approved layout. This is a composition experiment, not an addition to the maintained kit.

## Layout ownership

`shell.css` owns header and panel placement. The header stays in normal flow, uses the existing opaque canvas role, then sticks at the top. Panels start at header height + 24px and retain their viewport-bounded heights and 24px bottom gap.

A desktop body grid and semantic MAIN subgrid share the footer row. This extends the panels' containing block through the document footer, preventing the common sticky-parent shift at the end of a long event. The footer sits below the event column, so its text never passes behind the left panels. The MAIN and footer landmarks remain real elements. The individual event still scrolls in the document; no event scroll container, fixed-position width calculation, wheel animation or layout polling is introduced. A basic sticky-header fallback remains for engines without subgrid.

`dock.js` runs after the preserved search/navigation/layout helpers. It moves the original action row into an app-only dock, preserving its explicit form association and existing listeners. It wraps the original controls in a native scroll region, not cloned forms. The responsive adapter restores original node order and focus below the desktop threshold.

Pinned Search applies sticky placement to the app search form. ResizeObserver records its actual height for scroll padding, so focused fields and validation errors can remain visible below it. No new kit component, primitive override or product state model is added. The dock's neutral top separator marks a fixed action area; the event panes remain unframed.

## Build and preserve

Run Python with `-B` from this directory:

```text
python -B tools/build.py
python -B tools/build.py --check
python -B tools/check.py
```

Use the existing parent preview server on port4187. Do not run parent/app/kit writers. `tools/guard.py` verifies both earlier source archives, all 185 original desktop-study files, all 177 width-study files and the complete app/kit locks. This folder references those dependencies read-only and should remain in its current sibling location.

Source checks and browser evidence live in `qa/`. Saved release archives depend on the preserved parent collection and adjacent app; they are not standalone app distributions.

## Verification · 2026-10-22

All 160 HTML pages pass source and reference checks (11,996 local references). The 159 product documents match the Half Split generator after removing only the declared composition classes and CSS/script links. Preservation checks pass for all prior inventories: 185 desktop-study files, 177 width-study files, 980 app files and 180 kit files. JavaScript syntax passes. No kit files were edited or new kit components registered.

Browser execution used Codex's in-app Chromium. At 1440 × 900, the header remains at y=0 and the left panels at y=117 through right-document scrolling to the end. The list and both docked filter panels end at y=876, retaining the 24px gap. Apply filters remains visible at y=812 in the two docked versions. Scrolling Pinned Search's options moves its search form to y=117 while leaving Apply filters in place.

The 1200 × 700 and 1920 × 1080 checks retain the exact Half Split tracks and have no horizontal page overflow. Docked actions remain inside the viewport. At 390 × 844 and 1024 × 768, all three match the approved baseline's header, list, first-card geometry, title size and closed filter state. The desktop docks are removed below the breakpoint.

Functional checks cover category filtering, one result from combined date/category filters, zero results, clearing back to 48 events, reversed-date validation from a closed disclosure, draft query/date values across resizing, and avoiding duplicate inputs/actions when remounting. Query focus survives the resize; a focused dock action returns to the visible Filters summary when its original disclosure becomes closed on tablet. Invalid fields remain reachable below the sticky search. Event selection returns to the document top and browser Back restores the reading point while retaining the fixed frame. The browser exposes one banner, MAIN and contentinfo landmark.

The screenshots were saved and reviewed. Raw observations are in `qa/browser-measurements.json`. The comparison page contains live HTML frames with laptop/desktop/wide sizing controls. Firefox and Safari were not physically run; this is not a complete accessibility or cross-browser certification. Subgrid has a feature-query fallback, and native controls, focus styling and reduced-motion navigation continue to come from the preserved foundation.

Saved release: `dist/half-split-refinements-1.0.0.zip`, with a file manifest and SHA-256 checksum. The original source archives remain unchanged.
