# Browse-first flyout · Verification

Verified locally in the in-app Chromium browser on 2026-10-24. This records responsive browser checks, not physical-device keyboard, Firefox/Safari or screen-reader certification. Those remain adoption requirements.

## Arrival and browsing

At 390 × 844, the first event starts at y=289px rather than y=640.67px in the previous proposal: approximately 352px earlier. The query field is absent from the visible feed; the existing event cards are unchanged. Two complete cards and most of a third are visible on arrival. The original H1 remains visually hidden and available to assistive technology.

The header stays at y=0 while browsing farther down the phone feed. Sticky month labels remain underneath it and cannot cover its action. A native coordinate click on the persistent search action, followed by Cancel, retains root scroll at 470px. Backdrop dismissal also restores the draft without moving the feed. A genuine stacking overlap with the calendar was found during testing and fixed by isolating the results stacking context, with a matching phone/portrait-tablet calendar offset.

## Search and filter task

- Query Ink After Dark + Workshops previews one match while the feed remains unchanged. Cancel restores the empty query and original category choices.
- Enter in the flyout query submits the original GET form and produces one matching event. The result heading remains below the persistent header.
- Reset all clears the draft query and filters; cancelling Reset restores the applied query.
- Ink After Dark + Music can be applied as zero results. The original empty state appears; Clear all restores 48 events.
- An end date before the start date shows the existing error, focuses Through, blocks submission and leaves the flyout open. Escape discards those dates and returns focus to the header action.
- Tab from the final Show events action returns to Cancel; Shift+Tab from Cancel returns to Show events. Opening focuses the title rather than forcing a software keyboard immediately.
- Applying Ink After Dark + Workshops shows the Workshops Badge, the query in the result count and the Clear all row. Opening the event and browser Back preserve query/category choices.
- From/Through 2026-11-01 + Workshops applies the expected GET parameters and yields one event.

## Responsive ownership

At 1024 × 768, the flyout is 384px wide at x=0. The underlying list rectangle (x=24, y=121, width=390, height=623) and event rectangle are unchanged when it opens. The footer remains at the viewport bottom.

At 320 × 568, the flyout is about 272.67px wide and Show events ends at y=544px. The body scrolls from 173px to 437px while the footer position stays fixed. Draft query/category choices survive phone/tablet resizing. Visual-viewport height handling is implemented; a physical software keyboard was not available for verification.

Widening an open draft to desktop cancels its uncommitted query/categories and restores one query and date-control set to the original rail. The search submit becomes visible again, the secondary Apply class returns, original actions become visible, and the extra header action is hidden. No console errors were reported.

## Frozen desktop

At 1440 × 900, the same Black Ink, Bright Paper event produces identical screenshot hashes between the approved aligned version and this sibling:

| State | SHA-256 in both versions |
| --- | --- |
| Sidebar open | `02eafdfaaa438b983a50b4637defdffa13348e25525f6fb4564b899804cd2b00` |
| Sidebar closed | `38aeb56f81e87587f15cf2218aa7ca8899b32082f048a5fbb05c60ff4f8245fd` |

Source checks verify all 53 original product documents after stripping only declared additions, and every file in the preserved release chain. The prior 73-file responsive proposal, aligned desktop and kits remain unchanged. The app-owned composition is registered in `component-candidates.json`.
