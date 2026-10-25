# App 1.1.0 ownership and integration

The kit remains Tide 1.3.0, consumed read-only. `consumer-manifest.json` registers existing host adapters and the private `tide-app-release` block. No public component, token, color, radius, type scale or kit CSS changed.

| Responsibility | Owner and source |
| --- | --- |
| Event cards, Badge/In view, calendar groups, hero/details, Page intro, Summary, Notice, Link, Button, fields, Empty, Prose/Content page, shared Filter panel | Shared maintained Tide package. Canonical existing component CSS and HTML contracts remain authoritative. |
| Approved widths, header geometry, left scrolling panels, native-gutter input, responsive flyout placement | `src/runtime/css/host.css` (byte-identical baseline), `filters.js`, `rail.js`, `room.js`. Old study names remain private compatibility adapters. |
| Accepted sticky hierarchy | `tide-app-release__feed` in `src/pages/` and `src/runtime/css/app.css`: `isolation: isolate` on the entire feed. Summary and feed remain siblings. No extra scroller, clipping, global z-index scale or scroll listener. Existing summary/header ResizeObservers retain measured offsets. |
| Venue guide/context placement and fragment clearance | Private `tide-app-release` block in `app.css`. Existing kit components form the guide. Profile is visible below the list on phone and in the detail slot on tablet/desktop. |
| Venue identity/entry/exit | `src/runtime/js/venue-context.js`, authored page links and exact `sunshine-theater` ID. Event and venue links remain separate; no nested interactive links. |
| Search matching and URL state | `search-core.js`, `event-search.js`, `filters.js`. Venue narrows before keyword/date/category matching. URL and one original GET form own applied state. |
| Draft live count, commit, Reset, modal lifecycle | Existing `filters.js`. Draft count updates immediately; Show events/Enter applies to the feed through a real GET URL. Reset clears query/date/categories while retaining venue. Venue alone is context, not an active refinement. Escape cancels a draft and restores focus. |
| Event selection and return | Existing native event URLs plus the narrow `event-navigation.js` enhancement. Scoped back links retain refinements. Explicit All events/Find events exits scope. Refresh/Back/modified clicks remain native. |
| Theme/mode examples | `tools/build.py` writes complete routes using only `data-theme`/`data-mode` changes. Page structure and behavior share source. Each theme has light and dark examples. |

Desktop order stays app navigation/dialog → permanent lineup summary → isolated feed's month headings → cards. Month handoff works in both directions. Below the desktop breakpoint the summary retains its original behavior; phone uses natural document scrolling. Neither event pane receives a decorative outer border or clipping shell.

The venue guide remains visible when its *filtered* schedule has no results. A venue with no upcoming events intrinsically, venue directory/following, arbitrary additional venues, real data fetching and submission validation remain future coverage. This release does not claim those states are implemented.

Accepted contracts remain in the design-history tag under `tide-desktop-studies/release-handoffs/`; the table above is the maintained integration contract. The complete originals remain at the design-history tag. Current app/kit checks are independent of those archives.
