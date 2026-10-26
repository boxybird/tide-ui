# App 1.1.6 ownership and integration

The example consumes Tide 1.5.0. Shared `tide-venue-profile` now owns profile padding and section/header rhythm; duplicated app rules were removed. Native URLs, authored facts and the nine runtime scripts are unchanged. `consumer-manifest.json` registers the private `tide-app`, `tide-app-document`, `tide-lineup`, `tide-filter-drawer` and `tide-venue` families. No token, color, radius or type scale changed in this adoption.

| Responsibility | Owner and source |
| --- | --- |
| Event cards, Badge/In view, calendar groups, hero/details, Page intro, Summary, Notice, Link, Button, fields, Empty, Prose/Content page, shared Filter panel | Shared maintained Tide package. Canonical existing component CSS and HTML contracts remain authoritative. |
| Approved widths, header geometry, left scrolling panels, native-gutter input, responsive flyout placement | `src/styles/base.css`, `desktop.css`, `filters.css`; `filters.js` and `rail.js`. One app composition replaces the historical variant layers. |
| Accepted sticky hierarchy | `tide-lineup__feed` in `src/templates/event-list.html` and `src/styles/lineup.css`: `isolation: isolate` on the entire feed. Summary and feed remain siblings. No extra scroller, clipping, global z-index scale or scroll listener. Existing summary/header ResizeObservers retain measured offsets. |
| Venue guide/context placement and fragment clearance | Private `tide-venue` block in `src/styles/venue.css`. The shared `tide-venue-profile` and existing kit components form the guide. Profile is visible below the list on phone and in the detail slot on tablet/desktop. |
| Venue identity/entry/exit | `src/runtime/js/venue-context.js`, authored page links and exact `sunshine-theater` ID. Event and venue links remain separate; no nested interactive links. |
| Search matching and URL state | `search-core.js`, `event-search.js`, `filters.js`. Venue narrows before keyword/date/category matching. URL and one original GET form own applied state. |
| Draft live count, commit, Reset, modal lifecycle | Existing `filters.js`. Draft count updates immediately; Show events/Enter applies to the feed through a real GET URL. Reset clears query/date/categories while retaining venue. Venue alone is context, not an active refinement. Escape cancels a draft and restores focus. |
| Event selection and return | Existing native event URLs plus the narrow `event-navigation.js` enhancement. Scoped back links retain refinements. Explicit All events/Find events exits scope. Refresh/Back/modified clicks remain native. |
| Header, filter and list HTML composition | Registered `src/templates/` partials, `tools/html_templates.py`, `data/events.json` and `data/pages.json`. One shared document and workspace consume three unique venue/help/submission fragments; six non-event route contexts and native event details render through registered templates. Eleven submission fields share sample definitions and existing kit markup. Public component markup stays the same. |
| Theme/mode examples | `tools/build.py` writes complete routes using only `data-theme`/`data-mode` changes. Page structure and behavior share source. Each theme has light and dark examples. |

Desktop order stays app navigation/dialog → permanent lineup summary → isolated feed's month headings → cards. Month handoff works in both directions. Below the desktop breakpoint the summary retains its original behavior; phone uses natural document scrolling. Neither event pane receives a decorative outer border or clipping shell.

The venue guide remains visible when its *filtered* schedule has no results. An intrinsically empty venue schedule, venue directory and additional venue compositions are possible UI studies when selected for a concrete kit/example need; they are not a required backlog. Live data fetching and operational submission processing are outside project scope. Existing native form-validation examples remain UI behavior.

Accepted contracts remain in the design-history tag under `tide-desktop-studies/release-handoffs/`; the table above is the maintained integration contract. The complete originals remain at the design-history tag. Current app/kit checks are independent of those archives.

## App stylesheet and state conventions

`consumer-manifest.json` is the ordered stylesheet inventory. The app builder emits one `runtime/css/app.css`; never edit that output. All selectors are private to this example. Public `tide-filter-panel` internals continue to come solely from the kit.

| Module | Ownership |
| --- | --- |
| `base.css` / `tide.app` | App navigation, form composition, mobile event opening, tablet split, print baseline |
| `lineup.css` / `tide.app-lineup` | Shared heading rhythm, month labels, complete-feed stacking isolation |
| `desktop.css` / `tide.app-layout` | Contained desktop grid, margin borrowing, sticky panes/summary, native-gutter allowance, reveal motion |
| `filters.css` / `tide.app-filters` | Browse-first flyout placement, visual viewport allowance and small-screen control wrappers |
| `venue.css` / `tide.app-venue` | Venue guide/context and fragment clearance; app review composition |

Runtime-only modifiers are `tide-app--desktop`, `tide-app--drawer`, `tide-app--ready`, `tide-app__browse--filters-open` and `tide-app__browse--instant`. They describe mounted layouts and disclosure state, not visual themes. `tide-app--event` and `tide-app--venue` identify routes. `headings.js` measures `--tide-lineup-month-height`; `rail.js` measures `--tide-lineup-summary-height`; `filters.js` supplies desktop-only `--tide-app-scrollbar-gutter` and the drawer's visual-viewport inputs. `preview.js` retains the original/rough/no-photo preview behavior.

The single `data-state-key` preserves existing per-theme session preferences. Historical storage key strings are centralized in `app-runtime.js`. Those keys and the parent photo-preview message are deliberately retained for compatibility; they are not CSS classes or layout variants. Native URLs, IDs, form association and sample content remain stable.

The unenhanced saved-page desktop placement is deliberately preserved as well. This refactor does not redesign that sample's layout. Source checks reject historical study/shell selectors, unregistered stylesheet modules and unused private CSS classes.

The [runtime contract](RUNTIME.md) records shared services, deferred script order, single-owner calendar navigation and accepted preview compatibility. App styles and kit inputs remain unchanged.

The [template contract](TEMPLATES.md) defines include/value syntax, escaping, route context and collection ownership. Header links and active states, filter IDs/form associations, calendar IDs/jumps, selected-card status and native URLs remain stable across the extraction.

Individual event content and presentation ownership now live in the [detail contract](DETAILS.md): `document.html`, `workspace.html`, `event-detail.html`, typed `detail-*.html` blocks and `tools/event_details.py` consume the canonical event records. All 54 event URLs remain unchanged; index/search/saved previews reuse the same content with their existing heading levels. The [page contract](PAGES.md) records document/script/skip/footer variants, shared workspace and native submission-field ownership.
