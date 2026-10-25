# Lineup · Control Bars

Open <http://127.0.0.1:4187/lineup-control-bars/index.html>. Three desktop arrangements of the original Lineup controls, beneath the header and above both event columns:

1. **Inline** keeps search, dates, categories and Apply in one horizontal control row, below a compact context line.
2. **Search First** gives search its own wide position beside the familiar introduction, followed by an open filter row.
3. **Filter Shelf** keeps search visible and uses the original native Filters disclosure to reveal a horizontal shelf on demand.

All three use the same 40/60 event-list/detail proportions, original 48 events, touching cards, Lineup headings, Manrope and Bumble Dark tokens. The maintained kit, current Lineup 1.1.0, earlier collections and source releases remain unchanged. This is a private app-composition experiment, not a kit addition.

## Composition and behavior

The desktop breakpoint stays at 75rem/1200px. The header remains sticky. A second sticky bar owns the original controls, while the event list fits the remaining viewport height with the existing 48px bottom clearance. The individual event continues to scroll in the document. No outer event-pane border, modal, wheel handler or second event scroller is introduced.

ResizeObserver measures the actual bar height, including disclosure expansion and wrapped content. CSS uses that value for list height, its sticky top position and root anchor clearance. On short desktop windows the control bar can scroll natively, reserving space for the list. A semantic MAIN subgrid spans the footer row, keeping the frame in place through the end of the event document. The footer occupies the detail column.

`controls.js` replaces the previous Workbench/dock composition adapters for these pages only. It runs after the original search helper, moves the actual nodes and preserves their explicit form associations, IDs and listeners. Inline and Search First temporarily move fieldsets/actions outside the original disclosure. Filter Shelf keeps the existing disclosure, summary and body. Date-group instructions and the all-categories hint remain accessible via the existing screen-reader utility in desktop bars; visible From/Through and category labels remain intact. Invalid-date feedback is retained.

Below the breakpoint the adapter restores the original node order, visibility, disclosure state and focus, and removes its private layout classes. Tablet and mobile retain selected Lineup's heading hierarchy, original search/filter placement and card/detail composition. Native GET search, inclusive dates, category combinations, empty states, clearing, event links and Back remain the preserved app's behavior.

## Ownership and preservation

`control-bars.css` targets private `tide-control-study` classes and the existing study placeholder. It consumes existing color, type and spacing tokens, without redefining kit components or primitives. Geometry owns its private measured-height variables and overrides only the preceding shell's private panel-height variable. No new registered kit component is needed.

Run Python with `-B` from this folder:

```text
python -B tools/build.py
python -B tools/check.py
node --check controls.js
```

Use the parent `server.cjs` on port4187. Its `/base/` mount reads the approved app. Do not run parent/app/kit writers. `tools/bar_context.py` verifies the full earlier preservation chain and every source file in the preserved Lineup 1.1.0 release before and after work. This source collection depends on its preserved siblings and adjacent app; it is not a standalone app package.

## Verification · 2026-10-23

All 160 generated HTML pages pass source/reference checks (12,364 local references). After removing only declared private composition classes, data attributes and CSS/script references, the 159 product documents match the preserved Lineup generator. JavaScript syntax passes. All prior inventories remain unchanged: 185 original desktop-study files, 177 width-study files, 177 earlier refinement files, 182 Lineup files, 980 app files and 180 kit files. No kit component was added or edited.

Browser checks used the in-app Chromium. At 1440 × 900, the sticky header remains at y=0 and the bar at y=117. The list starts at y=289 for Inline, y=385 for Search First and y=333 for the closed Filter Shelf. Opening the shelf moves its list start to y=445. Every list ends at y=852, retaining the 48px bottom gap; root anchor clearance follows each measured bar height. Native document scrolling to the event end keeps the frame in place. Flat canvas paint covers the sticky bar's gaps so event text does not appear between the header and controls.

The 1200px desktop and 1920px wide checks show no horizontal page or control-bar overflow. In a 1200 × 600 window, an expanded shelf scrolls inside its own bound and reserves 288px for the event list. Keyboard scrolling can still reach Apply filters. This is the tradeoff of keeping the bar present in a short desktop window.

Combined date/category filters produce one workshop; a nonmatching query produces zero results; clearing restores all 48. Reversed-date validation stays visible and correction permits submission. November navigation, event selection's return to the top and browser Back continue working with the original helpers. Query/date drafts survive resizing, six original inputs remain present, and a focused action returns focus to the visible Filters summary when its original disclosure closes on tablet.

At 1024 × 768 and 390 × 844, all three restore the preserved Lineup's header, introduction, summary, list and first-card geometry, heading count and disclosure state. One immediate resize read preceded the media-query handler; the screenshot-backed recheck confirms the restored layout. Raw observations and final responsive comparisons are stored in `qa/`.

The three default desktop screenshots and expanded-shelf screenshot were saved and inspected. The comparison page has working live HTML frames and viewport controls. Firefox and Safari were not physically run in this pass; this is not a complete accessibility or cross-browser certification.

Saved source release: `dist/lineup-control-bars-1.0.0.zip`, with an internal file manifest and adjacent SHA-256 checksum. This package references its preserved dependencies and is not standalone.
