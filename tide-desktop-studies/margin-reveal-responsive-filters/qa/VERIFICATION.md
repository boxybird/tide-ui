# Responsive filter verification · 2026-10-24

Verified in the live in-app Chromium browser over the existing local4187 server. This is responsive browser testing, not a claim of physical iOS/Android, Firefox/Safari or screen-reader certification. The implementation uses established native dialog methods, native form controls and the existing search helper; references and adoption requirements are in the README.

## Approved desktop preservation

All66 aligned source/release files and the entire preserved chain pass SHA-256 verification. All53 product documents compare exactly with their approved source after removing only declared new hidden modal/launcher markup and dependency links. No original component HTML was rewritten.

At1440×900, screenshots of the same Black Ink, Bright Paper event have identical PNG hashes in both states:

| State | Baseline and new SHA-256 |
| --- | --- |
| Sidebar open | `02eafdfaaa438b983a50b4637defdffa13348e25525f6fb4564b899804cd2b00` |
| Sidebar closed | `38aeb56f81e87587f15cf2218aa7ca8899b32082f048a5fbb05c60ff4f8245fd` |

List, event, rail and action-dock rectangles also match at1200×600 and1920×1080. The desktop inner disclosure remains hidden, Apply remains pinned, and the event retains natural document scroll. Resizing from an open mobile/tablet panel back to desktop restores one original query/date control set, the secondary Apply class, visible actions and the original filter nodes inside the approved rail. Uncommitted panel choices are cancelled.

## Smaller-screen flow

- 390 × 844: modal fills the screen, footer ends at 844px and Apply ends at 820px. The title receives initial focus. Same date/category inputs remain associated with the original GET form.
- 1024 × 768: 448px drawer at the right edge, footer at 768px. Scrolling the backdrop does not scroll the underlying page. The underlying app columns are not resized by the drawer.
- 320 × 568: central body scrolls from 33px to 293px while footer position is unchanged; Apply ends at 544px. No duplicate query or date IDs. A draft checkbox survives resizing between phone and tablet.
- Draft From/Through 2026-11-01 + Workshops yields one match while the applied feed remains 48. Cancel restores empty fields and 48 matches; focus returns to Filters.
- Applying that draft navigates to the original GET search URL, shows one event, focuses the result count and brings the lineup into view. Opening First Sunday Print Exchange then browser Back retains dates, category and one result.
- Reset changes only the panel draft. Cancelling Reset restores the previous applied one-event date/category choice.
- Query Ink After Dark + Music yields zero draft matches and can be applied. The original empty state appears. Clear all restores 48 events.
- An end date before the start date shows the existing inline error, native validation focuses Through, and the panel stays open. Escape discards the draft and returns focus to Filters.
- Tab/Shift+Tab loop between the last action and the visible Cancel control. Native modal inertness prevents interaction with background content. A small endpoint guard also keeps embedded-browser Tab traversal from moving into browser chrome.

`browser-check.json` contains structured assertions and measurements. `mobile.png`, `tablet.png` and `mobile-short.png` show the new composition. `desktop-baseline.png` and `desktop-responsive.png` show the identical open desktop rendering.
