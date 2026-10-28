# Native component ownership · Lineup 2.2.2

The Lineup application kit consumes Tide 1.12.0 and contains no browser JavaScript. Shared component CSS/HTML remains kit-owned; private composition and authored result states remain app-owned.

| Responsibility | Canonical home |
| --- | --- |
| Event cards, hero/details, fields, notices, badges, prose, native controls and filter-panel internals | `packages/tide/` component recipes and CSS |
| 20/35/45 centered desktop layout, bounded left panes and natural right document | `src/styles/desktop.css`, static `tide-app--columns` body modifier and authored workspace templates |
| Saved desktop tracks | `desktop.css`: results in column 1, detail in column 2; scoped browse overrides keep their three-column placement |
| Navigation and skip-link presentation | Tide's Site header shell, compact navigation actions and `tide-skip-link`; Lineup authors destinations, list semantics, current-page context and focusable IDs |
| Primary destinations and venue directory | Consistent Find Events / Venues / Add an Event, separate Saved, footer Help, and authored `src/pages/venues.html` adopting Content page/Venue card; see [navigation and directory](VENUES-NAVIGATION.md). |
| Native mobile Menu | `header.html`, shared `navigation-items.html` and `base.css` own responsive availability, private mounting and CSS anchor placement. Tide's existing Button, navigation and Panel recipes own appearance. Canonical Panel CSS is emitted byte-for-byte as a generated dependency; see [mobile navigation](MOBILE-NAVIGATION.md). |
| Header geometry and optional preview skip | Private inner `tide-app__header-layout` grid groups primary links beside Saved with a 24px external gap; below 60rem, Saved is on row one and Filters ends row two. Outer width/insets/sticky placement and `tide-app__detail-skip` visibility remain app-owned; no private navigation/helper appearance |
| Filter footer and status internals | Tide owns rail padding/gap, flex/wrapping status row, count alignment and Reset text flow; private child wrappers supply narrow drawer clearance without aliasing public slots |
| Split-tablet header allowance | `base.css` uses the canonical 48px control input only where Filters is present between 60rem and 75rem; navigation-only/desktop rows retain the 44px input |
| Canonical component typography | Tide recipes; `test_presentation.py` rejects private aliases that override shared type across rendered routes |
| Event photo return availability | Private `tide-app__event-back` / `tide-app__event-tools` hosts in `event-detail.html` and `base.css`: hide the return link from 60rem when the list is beside the event; preserve optional Saved placement and omit an otherwise empty toolbar. Tide photo-control and toolbar appearance remain unchanged |
| Permanent summary and native scrolling feed | `event-list.html`, `lineup-summary.html`, `lineup.css`; canonical Results utility variant; summary outside `.tide-app__feed-scroll`, isolated complete feed inside. The private summary gap is 8px from 75rem and 16px below it; native fragment reservation uses the same input. Tide's calendar padding remains unchanged |
| Visible browse heading | `lineup-summary.html` authors the visible count heading outside the popover; `filter-heading.html` supplies the desktop utility label. Both use the canonical utility variant |
| Venue result destinations and recovery | `data/pages.json` venue owner/result map, `html_templates.py`, scope/reset/empty partials; same venue information in populated and empty states |
| Native responsive filter drawer | `filter-trigger.html`, `filter-rail.html`, `filters.css`; popover buttons, left slide/reduced motion, scrolling body/pinned footer and CSS return to the reserved desktop column; one form/control set, native disclosure/reset, browser-owned dismissal/focus |
| Filter content clearance and choice grouping | Private `tide-app__filter-content` adds `space-6` top clearance only below 75rem, leaving the public rail body/footer and desktop search untouched. Category adopts Tide's plain fieldset/choice recipe; When retains Stack. See [filter-panel spacing](FILTER-PANEL-SPACING.md). |
| Result/card/month counts and label spans | Build-time `tools/html_templates.py`, `data/events.json`, `data/pages.json` and registered partials |
| Category/empty specimens and complete previews | Typed `sampleFilter` route context; four authored result pages, never browser matching or fetching |
| Venue information and exact IDs | Authored venue fragment and native route context; no DOM rewriting |
| Document, browse, results and filter body/footer | Registered `document.html`, `workspace*.html`, `filter-rail.html`, `filter-status.html`, `filter-actions.html` |
| Eleven submission fields | Registered `form-*.html`, `data/submission-fields.json` and build-time form renderer |
| Browser runtime | None. `behaviorHome` is empty; checks reject browser executables and script hooks. |
| Independent consumer enhancements | Consumer-owned runtime/server and styles outside Lineup/Tide; navigation, matching, pagination, loading/error feedback, additional motion and return-state coordination. See the [integration guide](CONSUMER-INTEGRATION.md); its private-markup map adds no public selector API. |

The [2.1.4 handoff contract](HANDOFF.md) removes tutorial result-state navigation and example wording from customer-facing templates. Native form fields remain; reference layouts, fixture provenance and integration limits live outside the product interface. This does not alter shared components or add service behavior.

Native event paths, IDs and 54 records remain. Custom draft counts, arbitrary text/date filtering, fetched previews, session storage, photo/message hooks, delayed navigation and custom restoration are retired. Existing query strings do not activate behaviors. Native history, links and input/reset behavior belong to the browser.

CSS uses native gutter reservation and grid rows instead of JavaScript height/scrollbar measurements. The fixed summary no longer requires month headers to subtract its measured height. Original minimum 24px panel bottom clearance remains; native scrollbar space is reserved in the scrolling area through CSS.

All source ownership and theme boundaries remain explicit. No generated copies are edited. See [runtime boundary](RUNTIME.md), [desktop contract](DESKTOP-LAYOUT.md) and [policy/audit](../../../docs/NO-BROWSER-JAVASCRIPT.md).

The [strict HTML/CSS alignment closeout](TIDE-ALIGNMENT.md) supersedes sampled appearance checks. `presentation_contract.py` rejects private lookalike type/decoration, shared token changes and public interior overrides through rendered aliases. Canonical fields, choices, buttons, uploads, card slots and semantic footer structure have application guards. The sticky header canvas is on a private outer wrapper; public header padding and appearance remain in Tide.

Historical [footer/tablet verification](FILTER-FOOTER-TABLET.md) resolves the fresh audit findings. Application guards cover shared typography plus all properties on rendered footer/status/count aliases and the Reset data hook. Shared sources remain read-only.

Historical [heading/venue verification](HEADINGS-VENUE-SCOPE.md) covers the original control set, unique heading, scoped native routes and exact venue ID. Tide remains unchanged.
