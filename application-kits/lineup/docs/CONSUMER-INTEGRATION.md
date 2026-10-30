# Consumer integration · Lineup 2.1.8

**Current 2.4.0 boundary:** the approved map is now in `src/map/` and builds from the current Lineup templates. Review `/events/app/venues.html` on port 4187. There is no active separate consumer or copied source snapshot. Only the venue directory loads browser modules; prior no-script/map-provider-exclusion statements below describe the earlier native baseline. The current [source-of-truth contract](SOURCE-OF-TRUTH.md) takes precedence. Native event/search journeys and service limits are unchanged.


Lineup 2.1.9 retains the integration points below. Its private filter-content wrapper and compact Category grouping are documented in [filter-panel spacing](FILTER-PANEL-SPACING.md); field names, native routes and runtime boundaries are unchanged. The external consumer experiment described here consumed 2.1.8.

Lineup 2.2.0 adds `venues.html` and a consistent primary menu. Template consumers should adopt the new Venues/submission current-page values and remove the retired route-dependent secondary navigation. The [navigation/directory contract](VENUES-NAVIGATION.md) records that migration. Existing event/filter integration points remain unchanged.

Lineup 2.2.1 adds the [native mobile Menu](MOBILE-NAVIGATION.md). A shared link-item partial renders inline and popup presentations; CSS exposes only the relevant one. Adapters should scope navigation work to the active presentation rather than assuming one DOM copy of every header link. Template consumers also adopt `HEADER_MENU_ICON`, `KIT_PANEL_CSS` and the registered `navigation-items.html` partial; the builder supplies the unchanged public Panel extension as a generated dependency. No browser runtime is added.

Lineup supplies complete HTML documents, native destinations and controls, responsive composition, and authored reference states. A consuming website can retain full-document navigation or add partial navigation and its own client runtime. The kit does not require a routing framework or a multi-page-only interaction model.

This guide documents the current composition and the responsibilities of an independent consumer. It adds no runtime dependency, replacement protocol, public selector API or Tide component. Lineup's distribution remains script-free. Consumer adapters, servers, experiments and their dependencies belong outside the kit.

## Ownership

| Owner | Responsibility |
| --- | --- |
| Tide | Shared component appearance, semantic roles, tokens, themes and supported recipes. Adopt these through their documented options. |
| Lineup | Application composition, responsive panes, native drawer, headings/labels, destinations, fixtures and authored reference layouts. |
| Consumer: content and services | Real event data, search rules/counts, pagination data source, persistence, submission/upload processing and any operational services. The supplied fixtures do not implement these. |
| Consumer: optional enhancement | Requests and response selection, replacement boundaries, routing/history, cache policy, focus/reading-position restoration, loading/error feedback and additional navigation motion. |
| Consumer: compatibility | Recorded Lineup/Tide versions, local adapter hooks, upgrade review and integration verification. |

Use native HTML/CSS for the behaviors it already supplies. Retain the single native popover/control set rather than rebuilding the drawer or measuring its geometry in script. Additional consumer behavior does not require adding it to Lineup or Tide. A new shared Tide recipe is a separate UI-kit change; a consumer-specific loading indicator can stay in the consumer.

## Complete documents and enhanced navigation

Keep each event reachable through an ordinary URL with complete useful content on direct visits and refreshes. An enhanced in-site transition can request a complete document or a consumer-defined fragment while leaving that direct-document route available. Preserve modified clicks, new tabs, fragment links and ordinary navigation fallback.

Full-document rendering does not prescribe how a consumer handles later clicks. A server-rendered or pre-rendered event route can coexist with an enhanced single-page experience. The consumer chooses that architecture, its endpoint/fragment protocol and cache behavior; Lineup supplies no built-in fragment endpoint or live query interpreter.

A public website also owns event-specific metadata, canonical policy, structured data and sitemap delivery. The current kit supplies descriptive document titles and a general description, not a production indexing contract. If navigation replaces content without loading a document, coordinate its title and other route metadata as well as its visible content.

## Current integration map

These are **implementation references for 2.1.8**, not newly guaranteed extension hooks. Private `tide-app*`, `tide-lineup*` and `tide-venue*` composition remains private under the [ownership contract](COMPONENT-OWNERSHIP.md). Consumers may add their own integration identifiers in their rendering/adapter layer and should review this map on upgrades.

| Point | Current source/markup | Consumer obligation when enhancing it |
| --- | --- | --- |
| Document context | `document.html`; document title/description, HTML theme/mode, body route classes and optional `data-venue-scope` | Keep URL, route composition, theme, metadata and venue scope consistent. `data-state-key` is existing private markup, not a release identifier or storage API. |
| Browse/results | `workspace*.html`, `.tide-app__browse`, `#results`, `.tide-lineup__summary`, `#result-count` | Reconcile count, scope, heading level and current navigation context with the incoming route. Preserve a subtree only when its collection/filter context is compatible. |
| Detail or placeholder | `event-detail.html`, `#event-detail`, `#event-title`, `#event-story`, `#preview-state` | Match the incoming document's heading hierarchy and accessible names. `#event-detail` can also contain a venue profile; its ID alone does not identify an event route. Empty results need the correct placeholder or venue information. |
| Event selection | `event-card.html`; real card-link `href`, `card-{ID}` heading, `tide-event-card--in-view` and hidden/visible “In view” status | Keep record/URL identity, selected-card appearance and status aligned with the displayed event. Do not infer identity from list position. Card `data-*` fixture metadata is not a search-service API. |
| Search and actions | `filters.html`, `filter-actions.html`, `filter-reset.html`; `#event-search-form` and its associated controls | Include controls associated through `form="event-search-form"`, not just form descendants. Preserve native labels, validation and the intended Reset/recovery behavior. |
| Drawer | `#lineup-filters`, native `popover="auto"` and its `popovertarget` buttons | Keep one control set and native dismissal/focus behavior. If replacing the panel during an update, deliberately preserve or dismiss its open state and restore the appropriate focus/caret after replacement settles. |
| Reading position | `.tide-app__feed-scroll`, `.tide-app__filter-body`, outer document, native month fragments | Treat nested and document scroll positions separately. The visible summary stays outside the feed; the detail remains a natural document. Observe the actual scrolling container for near-end loading. |
| Venue context | Venue route, `#venue-information`, scoped actions and recovery links | Keep venue information available independently of matching results. Preserve same-document information jumps and distinguish venue recovery from the explicit city-wide exit. |

Relevant composition lives in [templates](TEMPLATES.md), [document structure](PAGES.md), [desktop layout](DESKTOP-LAYOUT.md), [drawer behavior](FILTER-DRAWER.md) and [heading/venue scope](HEADINGS-VENUE-SCOPE.md). The split event/list view starts at 60rem; the permanent filter column starts at 75rem. These are different layout decisions, not a single observer or routing breakpoint.

Replacing only `#event-detail` is insufficient if the rest of the route changes. A full event document uses an event h1, while a collection preview uses subordinate detail headings. Update the result heading, body classes, current navigation and selection together so the page retains one meaningful h1 and working skip targets. The photo return control is available below 60rem; its ordinary destination remains the fallback when no originating list is known.

## Search and collection state

The native GET form sends `q`, `from`, `to`, repeated `category` values and `venue`. The global action is `search.html`; the scoped venue action is `sunshine-theater.html`. Dates/categories and the submit button can be outside the form element while remaining associated with it. Global Reset restores native defaults; venue Reset/recovery can be a navigation link that retains scope.

The static kit does not interpret these query values or implement matching, date-range relationships, live counts, sorting or pagination. The consumer defines those semantics and returns corresponding content, counts, scope and empty/recovery states. Reference result documents demonstrate layouts, not an operational search engine.

Keep committed result state distinct from an unsent draft when restoring history. The consumer decides when to submit, whether live edits replace or add history entries, and how filters/page context become shareable URLs. Parameter names for page size, cursor or accumulated range are consumer-defined; they are not Lineup query contracts.

## Pagination, loading and motion

Manual pagination and automatic continuation are consumer choices. The consumer owns page/cursor rules, batch size, request scheduling, cancellation, retry and termination. For automatic continuation:

- Observe the bounded feed or the document according to the current layout, and reconnect when that layout changes.
- Append without moving focus or resetting the reading position. Keep event IDs unique, merge repeated month groups as needed, and update group/result counts accurately.
- Keep new links functional, including any consumer enhancement binding they need. Carry enough collection context to reconstruct the loaded range on direct navigation or a cache miss.
- Cancel or disregard stale batches when the query/scope changes. Prevent duplicate requests/cards, stop at the end, and retain the existing results on failure.
- Show pending feedback near the list tail, announce useful status, and provide a deliberate recovery action. Consumer-specific indicator styling stays outside Tide unless separately adopted as a shared component.

Native drawer motion remains Lineup CSS. Additional event-navigation transitions are optional consumer enhancements. Honor reduced motion, avoid intercepting subsequent input with a transition overlay, and ensure the destination is still usable when motion is absent.

## Navigation and return responsibilities

For enhanced navigation, coordinate URL/history, metadata, route classes, headings, count/scope, selected card and accessible focus targets as one transition. Retaining a feed or form also retains its old DOM state; reconcile the parts that belong to the new route.

Preserve query, category/date/venue context, loaded range, disclosure state, nested scroll, document scroll and originating link when they are relevant to the journey. Back/Forward and the event return action should recover that context. A directly opened event needs a useful ordinary return destination without assuming a prior history entry. Native fragments such as venue information must continue to work alongside enhanced history.

The consumer owns cache size/lifetime, restoration on cache misses and the choice of state storage. Saved links and authored submission fields do not provide persistence or an operational service. A failed or incomplete response should leave the current view usable, with error/retry feedback and a full-document recovery path where appropriate. Loading new results should not steal focus from typing or native controls.

## Handoff and upgrades

Record the Lineup release, its Tide dependency and the consumer adapter version separately. Review release notes and any changed source/markup dependencies before adopting a kit update. Do not assume private selectors, body attributes or response-shape assumptions are a version-independent runtime API. A supported shared integration API would need its own explicit contract and review.

Verify the consumer against direct visits/refreshes, native and enhanced links, modified clicks, history/return, fragments, one h1, scope/count/selection, form-associated controls, native drawer focus, responsive scroll containers, empty/end states, pending/error/retry, stale responses and reduced motion. Include relevant themes, keyboards, browsers, devices and assistive technology; record what was actually exercised rather than treating source checks as accessibility certification.

An isolated external consumer exercised enhanced navigation, live matching, paginated/infinite collections, loading feedback and return-state handling against this release without requiring Lineup or Tide source changes. That feasibility evidence is Chromium on Windows; it does not make the external adapter a kit dependency or establish cross-browser, screen-reader or production-service coverage. The experiment and its runtime remain separate from this repository.

## Venue directory search · 2.3.0 refinement

`venue-search-form` is a native GET form to `venues.html`; its `venue-query` search control submits `q`. It uses the unchanged Tide Field recipe. The static kit preview does not match query text or update its six-entry fixture count; the consuming server or optional enhancement supplies matching/results, URL handling and any return state. The field remains part of the delivered UI. See [venue directory](VENUE-DIRECTORY.md) for the native map/fragment and provider boundary.

## Venue selection · 2.3.1

The unreleased responsive refinement exposes a direct `{venue-id}.html` covering link below 60rem, where List and Map are separate views. At 60rem and above it retains the map selection described below. Two native links sit in private availability hosts; exactly one is exposed. Consumers should scope any enhancement to the visible action instead of assuming each card contains only one covering link. Card content, IDs, secondary details links and marker destinations remain unchanged.

The directory card's covering link now targets `#map-{venue-id}`; its separate View venue details link retains `{venue-id}.html`. Marker links target `#venue-{venue-id}` and reveal the corresponding row. Both native targets identify the same selected venue through the row Badge and photographic map-control text; selected caption links expose details and return-to-row actions. Consumers adapting the previous card/document or marker/popover hooks must update those assumptions. These private markup references are not a version-independent public API.

The kit keeps an illustrated map completely fitted so every native target is reachable. Geographic camera movement and provider lifecycle remain consumer responsibilities. A real integration should move only enough to reveal the selected location, synchronize record identity across both views, retain keyboard access/direct document links, and respect reduced motion. Native URL selection survives direct visits and history; `scroll-initial-target` progressively reveals the selected row on initial rendering in supporting browsers. A consumer requiring exact arbitrary scroll offsets and consistent restoration across engines must supply and verify that behavior. No runtime or provider requirement is introduced into Lineup or Tide.
