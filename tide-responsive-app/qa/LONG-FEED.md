# Long-feed verification · 1.1.0 · 2026-10-22

## Preservation

The original kit's 176-file lock passes. The exact 1.0.3 three-event package is extracted at `versions/1.0.3/`; all 263 files pass their separate hash lock. A rendered visit confirmed three cards, the original “This weekend.” heading and the same 1120px desktop width. Earlier ZIPs remain unchanged.

The three original event records retain every original field/value. New rows extend the fixture; no original event was replaced. Kit fonts, type, spacing, corners, controls and theme inputs remain unchanged.

## Data and source checks

- 48 unique event routes: 16 October / 32 November, ordered chronologically from October 23 through November 29.
- Five Python data tests pass: volume/unique slugs; month boundary and labels; correct local UTC offsets; unchanged core event details; varied copy/length/price/age.
- Nine Node navigation tests pass, including the new list-only desktop month jump and native mobile anchor fallback.
- Twelve existing kit tests and 324 palette contrast checks pass.
- 392 current HTML documents, 24,696 local references and one registered deferred helper pass source checks. No inline styling, event-handler attributes, unregistered scripts or raw application palette colors were introduced. Frozen versions are checked by hash instead of being rebuilt.

## Rendered browser behavior

Chromium in the in-app browser:

- The 48-card list is approximately 9617px tall, inside a 578px scroll area at 1280 × 720. Its complete frame leaves 24px below it on arrival.
- A direct pointer click on the November jump moved the list to 3447.33px while the document stayed at 0. The sticky month title, count and jump links stayed available. Selecting the first November event retained that same list position and opened the event at document scroll 0.
- At list scroll 9038.67px (the last events) and document scroll 1550px, selecting One More Sunday returned the page to 0 and opened that real detail route. The list stayed at 9038.67px. Browser Back restored both 1550px reading position and 9038.67px list position.
- From that deep reading position, the October jump moved only the list to 412px; the document remained at 1550px.
- Keyboard scrolling across October 31 / November 1 showed the October heading staying above the last October event, then the November section and its independent heading entering below. Headings hand over as the boundary passes the top of the list.
- At portrait-tablet width 834, a native November fragment jump used ordinary document scrolling, placed the month heading near the top (52px), and kept all 48 cards available.
- Browse and the longest-title event were checked at 320 × 844, 834 × 1112, 1024 × 600, 1280 × 720 and 1440 × 900. No horizontal overflow or missing images. At desktop widths the frame retains its 24px bottom gap. On narrow screens the longest hero grows naturally when needed instead of clipping its title/details.
- All six theme modes keep a 1120px desktop workspace and 184px first unselected card. Month surfaces use each theme's existing canvas role; all display 48 cards without horizontal overflow.
- The one-item Saved fixture still displays one event, providing a short-list comparison.
- The test tab recorded no console warnings/errors.

Raw results: `long-feed-checks.json`, `long-feed-layouts.json`. Screenshots: `long-feed-month-boundary.png`, `long-feed-deep-selection.png`, `long-feed-tablet.png`, `long-feed-tablet-november.png`, `long-feed-november-event.png`.

## Limits

This is a fictional-data UX fixture. It does not benchmark a live search service, infinite feed, networking, cache or virtualized rendering. Search and saved are still fixed sample states. The three illustrative photos are reused by category. Native Firefox/Safari, screen readers, physical devices and OS-level motion settings still need release testing; the rendered checks here do not constitute full accessibility certification.
