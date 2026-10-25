# Margin Reveal · Unified search

[Responsive prototype](http://127.0.0.1:4187/margin-reveal-unified-search/demo/index.html) · [Three-size review](http://127.0.0.1:4187/margin-reveal-unified-search/index.html) · [Preserved Browse First](http://127.0.0.1:4187/margin-reveal-browse-first/index.html)

The user prefers the tablet flyout's live matching count and one combined action. This sibling extends that exact interaction to desktop. It preserves the previous release rather than overwriting it.

## Shared interaction contract

- Search has no separate submit button while enhanced. Typing, clearing the query, changing dates and selecting categories update the matching count and Show N events label immediately.
- The status is the same polite, atomic live region at every width. The existing TideSearch rules match all query words, inclusive From/Through dates and any selected category. All48 sample cards are counted, including those hidden by the applied URL.
- One Show events action applies query, dates and categories together through the existing GET form. Enter in search also submits. The feed and URL stay on the applied choices until submission.
- Reset all clears the entire draft and restores a48-event preview. It does not navigate until Show events. The native search clear control also updates the count.
- Invalid ranges retain the existing visible explanation and native validity; the status says Check the date range and the action says Check dates. Zero matches remain a valid submission with the original empty state and recovery.
- Mobile/tablet retain the left modal flyout. Cancel, Escape and backdrop dismissal restore the opening query/filter values. Desktop retains the original persistent rail and its existing open/close behavior.
- The existing Clear all link remains in applied context. The redundant link beside the desktop submit is hidden while enhanced because Reset all occupies that action area. Without the enhancement, the original separate submits, native disclosure and Clear all remain usable.

## Placement and ownership

There is one query, one set of date/category controls, one status/reset row and one apply button. `unified-search.js` derives from the preserved Browse First controller and replaces it in these documents. Direct input/change listeners follow the original nodes between containers; the count implementation is shared at all widths. Below75rem the controls and actions live in the existing dialog. At75rem and above the status/reset row moves to the existing desktop dock above the original apply button. It returns before the frozen desktop adapter removes the dock during resizing. Open mobile drafts cancel on crossing to desktop, as in the previous release.

`unified-search.css` owns the private desktop status-row layout, caption typography, full-width apply, redundant-link visibility and spacing refinements. It consumes existing semantic tokens, adds no color or sizing primitives, and does not redefine kit control internals. Desktop header, horizontal rail/list/event geometry, left alignment and right document scroll continue to use their preserved CSS sources. At75rem and above, both bounded panes use the column-gap token (currently24px) plus the measured native list scrollbar gutter as their bottom clearance. The dock's start inset and the gap below its Reset all row both use space4 (16px); the original grid keeps Show events aligned with the list bottom. The scrollable filter body absorbs the footer size change. Smaller-screen styles are unchanged.

## Version1.0.2 — measured native scrollbar gutter

The native scrollbar and its existing styling are retained. A desktop-only ResizeObserver watches the existing event-list content box. It subtracts content-box inline size, inline padding and inline borders from border-box inline size, keeping subpixel precision before rounding to0.001 CSS px. This measures occupied scrollbar space rather than assuming a browser/platform width. The current composition uses horizontal writing mode and an unfragmented list. Older box-size shapes fall back to offsetWidth/contentRect.

The observer supplies the registered private input `--tide-unified-search-scrollbar-gutter` on the app body. Both bounded panels consume the existing shared height calculation: dynamic viewport minus panel top, pane gap and measured gutter. The existing dock keeps Show events flush with the list bottom. A zero CSS fallback retains24px when the helper is unavailable; no component/theme input changes.

Measurements update when the list resizes or its occupied scrollbar space changes. A changed-only animation-frame write prevents observer delivery loops. There is no polling, synthetic scrollbar or scroll-position write. No gutter is artificially reserved. A non-overflowing list and an overlay scrollbar have zero occupied width, so the base24px clearance applies. This follows the distinction described in [MDN's scrollbar-gutter reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scrollbar-gutter). ResizeObserver [border-box](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserverEntry/borderBoxSize) and [content-box](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserverEntry/contentBoxSize) sizes provide the layout measurements.

On leaving desktop, the observer disconnects, any queued frame is cancelled and the private property is removed before the existing adapter restores mobile/tablet nodes. It starts again on return to desktop. Modal styles, controls and behavior are unchanged. Native platform overlay settings, Firefox and Safari still need direct device/browser verification; the geometry is measured rather than inferred from their names.

This app composition has an HTML/CSS/behavior home and registration in `component-candidates.json`. The maintained kit and frozen foundation are unchanged. Broader kit adoption still needs shared-shell consolidation, all-theme specimens and device/assistive-technology verification, with removal of app duplicates. No React or service has been added.

## Build and preservation

Run Python `-B tools/build.py`, then `-B tools/check.py`; run `-B tools/package.py` after browser QA. The54 generated HTML documents preserve the original component markup after removing the declared script/stylesheet substitutions. Verification checks the previous75-file release and the entire preservation chain. Only this sibling receives new QA and packaging output. Browser evidence is recorded under `qa/`.

Version1.0.0 remains preserved in its original68-file release archive and checksum. Version1.0.1 changes only the two desktop spacing relationships above; its browser measurements live in `qa/spacing-1.0.1.json`. The earlier behavioral evidence remains the1.0.0 baseline.

Version1.0.1 remains preserved in its original70-file archive and checksum. Current1.0.2 adds measured native-gutter compensation; its evidence is `qa/gutter-1.0.2.json`. Prior QA records remain historical baselines.
