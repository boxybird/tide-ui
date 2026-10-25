# Search and filters · 1.2.0

The preserved 48-event layout now supports real local search. Use the search arrow or Enter to apply the complete form, or open **Filters**, choose dates/categories and select **Apply filters**. Changes apply together, on submission. **Clear all** removes the query, date range and categories and returns all 48 events.

Dates are inclusive, based on the event's Albuquerque calendar date; either boundary can be left empty. Multiple categories include any selected category. Search, dates and categories intersect. With no categories selected, all categories are included. Results stay in chronological order.

Search matches words in the title, venue, category, subtitle and description. It ignores case, accents and punctuation; all search words must match. It does not provide fuzzy spelling correction. Named query parameters (`q`, `from`, `to`, repeated `category`) retain choices through refresh, event navigation and browser Back. A filtered search preview follows the first match if Ink After Dark is excluded. Actual event links still open their own static HTML page. Back-to-results links retain the applied filters.

## Try these

| Action | Expected result |
| --- | --- |
| Clear all | 48 events: 16 October, 32 November |
| Search `Ink After Dark` | One event |
| From and Through `2026-11-01`, Workshops | One event: First Sunday Print Exchange |
| From `2026-10-31`, Through `2026-11-01` | Results on both sides of the month boundary |
| Through `2026-10-31`, no categories | 16 events |
| From `2026-11-01`, no categories | 32 events |
| Search `Ink After Dark`, Music | No events, with clear recovery |
| Search `unfindablexyz` | No events |
| From `2026-12-01` | No events |
| End date before start date | Inline explanation and native validation; submission blocked |
| Open a filtered result, read down, choose another | Same smooth desktop navigation and retained list/filter state |
| Browser Back or refresh | Applied query and choices retained |

The same generated HTML and rules serve all six theme/modes. Card geometry, font, palettes, tokens and viewport behavior remain unchanged. Month counts and jump links include only visible results. The empty state uses the existing kit's empty-state component and semantic colors.

## Implementation boundaries

No framework or backend. `search-core.js` contains shared, tested matching/URL rules; `event-search.js` enhances the existing cards. GET navigation and real event URLs keep browser navigation native. Desktop previews load only a matching local HTML event document. A failed preview falls back to opening the working result link. Local search works directly from disk, but automatic preview loading should be tested over the provided localhost server. Without JavaScript, all events remain browsable and a notice explains that filtering needs the enhancement. Saved remains an illustrative shortlist; submissions and reservations remain unavailable.

The previous 1.1.0 long-feed package remains intact in `dist/tide-responsive-app-1.1.0.zip`, along with all earlier packages. The original kit and frozen three-event baseline retain their hash locks.
