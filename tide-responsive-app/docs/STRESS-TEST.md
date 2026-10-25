# Long-feed UX study · 1.1.0

This iteration expands data and calendar navigation while retaining the selected Tide layout. The exact previous three-event experience is preserved at `../versions/1.0.3/index.html`; its 263 extracted files are hash checked against the previous ZIP. The original UI kit's 176-file hash lock also remains in force.

## What to try

1. Browse all 48 events from October 23 through November 29, 2026. Sixteen are in October and 32 in November. The same card, date, type, color and spacing primitives are used.
2. Scroll the left feed across October 31 / November 1. The quiet month heading stays at the top of that scroll area, then hands over to the next month. Individual card dates also say Oct or Nov.
3. Use the Oct/Nov links in the sticky month heading. They remain available deep in the feed, so you can jump back without scrolling to the search controls. On desktop they move only the list; your place in the event details is retained. With native mobile layout/no helper, their regular fragment anchors work.
4. Pick an event far down November, read the right side, then choose another. The list keeps its deep position while the document glides up before following the real event link. Browser Back restores both reading and list positions.
5. Try the long November 12 title, free admission, all-ages events and multiple events on the same date. Each has a real detail route and distinct copy. The core three events retain their original details.
6. Compare the single saved-event sample with the full browse feed. In the preserved 1.1.0 package, search/saved were fixed previews. Current 1.2.0 makes search and date/category filters functional; see `SEARCH-FILTERS.md`. Saved remains an example shortlist. Pagination, account storage and booking remain outside this iteration.
7. Resize between portrait tablet, landscape tablet and desktop; try short browser windows as well. The closed desktop result frame should still leave 24px below it on arrival. The right detail remains ordinary document scrolling.

## Deliberate choices

All 48 events are loaded for this fixture; no infinite feed, loading delay or virtualization obscures the interaction test. This is an experience test with realistic content volume, not a backend/load benchmark. There is a visible end to the sample feed.

Month/year headings supply context, and the existing compact dates retain each event's day and month. Month jump targets are keyboard-focusable headings. Desktop scroll padding keeps focused cards below the sticky month strip. Status colors and colored left borders are not used for calendar grouping.

The three existing illustrative photo assets are intentionally reused by category. New photography is not the subject of this UX pass. The data is fictional, including venues and admission details. The first three approved event records are preserved in `data/events-core.json`.

Local dates, weekdays, ordering and ISO timestamps are consistent. The fixture includes the Albuquerque daylight-saving offset change: October evening samples use -06:00 and November samples after the change use -07:00. Offsets are stored in the committed JSON, so ordinary builds need no timezone database. Reauthoring the fixture with `tools/seed_events.py` needs Python IANA timezone data.

Source: `data/events.json`; authoring: `tools/seed_events.py`; normalization/grouping: `tools/events.py`; shared markup: `tools/build.py`. Run the Python data tests and Node navigation tests listed in README. Rendered results are recorded separately in `qa/LONG-FEED.md`.
