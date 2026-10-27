# Native component ownership · Lineup 2.1.3

The Lineup application kit consumes Tide 1.10.0 and contains no browser JavaScript. Shared component CSS/HTML remains kit-owned; private composition and authored result states remain app-owned.

| Responsibility | Canonical home |
| --- | --- |
| Event cards, hero/details, fields, notices, badges, prose, native controls and filter-panel internals | `packages/tide/` component recipes and CSS |
| 20/35/45 centered desktop layout, bounded left panes and natural right document | `src/styles/desktop.css`, static `tide-app--columns` body modifier and authored workspace templates |
| Saved desktop tracks | `desktop.css`: results in column 1, detail in column 2; scoped browse overrides keep their three-column placement |
| Navigation and skip-link presentation | Tide's `tide-site-header`, `__links`, `__link` and `tide-skip-link`; Lineup authors destinations, list semantics, current-page context and focusable IDs |
| Header geometry and optional preview skip | Private header width/insets/sticky placement and `tide-app__detail-skip` visibility from 60rem; no private navigation/helper appearance |
| Filter footer and status internals | Tide owns rail padding/gap, flex/wrapping status row, count alignment and Reset text flow; private child wrappers supply narrow drawer clearance without aliasing public slots |
| Split-tablet header allowance | `base.css` uses the canonical 48px control input only where Filters is present between 60rem and 75rem; navigation-only/desktop rows retain the 44px input |
| Canonical component typography | Tide recipes; `test_presentation.py` rejects private aliases that override shared type across rendered routes |
| Permanent summary and native scrolling feed | `event-list.html`, `lineup-summary.html`, `lineup.css`; private context wrapper beside canonical Results; summary outside `.tide-app__feed-scroll`, isolated complete feed inside |
| Visible browse heading | `workspace-browse.html` authors one canonical intro outside the popover; private grid placement keeps it visible on phone/tablet/desktop |
| Venue result destinations and recovery | `data/pages.json` venue owner/result map, `html_templates.py`, scope/reset/empty partials; same venue information in populated and empty states |
| Native responsive filter drawer | `filter-trigger.html`, `filter-rail.html`, `filters.css`; popover buttons, left slide/reduced motion, scrolling body/pinned footer and CSS return to the reserved desktop column; one form/control set, native disclosure/reset, browser-owned dismissal/focus |
| Result/card/month counts and label spans | Build-time `tools/html_templates.py`, `data/events.json`, `data/pages.json` and registered partials |
| Category/empty specimens and complete previews | Typed `sampleFilter` route context; four authored result pages, never browser matching or fetching |
| Venue information and exact IDs | Authored venue fragment and native route context; no DOM rewriting |
| Document, browse, results and filter body/footer | Registered `document.html`, `workspace*.html`, `filter-rail.html`, `filter-status.html`, `filter-actions.html` |
| Eleven submission fields | Registered `form-*.html`, `data/submission-fields.json` and build-time form renderer |
| Browser runtime | None. `behaviorHome` is empty; checks reject browser executables and script hooks. |

Native event paths, IDs and 54 records remain. Custom draft counts, arbitrary text/date filtering, fetched previews, session storage, photo/message hooks, delayed navigation and custom restoration are retired. Existing query strings do not activate behaviors. Native history, links and input/reset behavior belong to the browser.

CSS uses native gutter reservation and grid rows instead of JavaScript height/scrollbar measurements. The fixed summary no longer requires month headers to subtract its measured height. Original minimum 24px panel bottom clearance remains; native scrollbar space is reserved in the scrolling area through CSS.

All source ownership and theme boundaries remain explicit. No generated copies are edited. See [runtime boundary](RUNTIME.md), [desktop contract](DESKTOP-LAYOUT.md) and [policy/audit](../../../docs/NO-BROWSER-JAVASCRIPT.md).

The [strict HTML/CSS alignment closeout](TIDE-ALIGNMENT.md) supersedes sampled appearance checks. `presentation_contract.py` rejects private lookalike type/decoration, shared token changes and public interior overrides through rendered aliases. Canonical fields, choices, buttons, uploads, card slots and semantic footer structure have application guards. The sticky header canvas is on a private outer wrapper; public header padding and appearance remain in Tide.

Historical [footer/tablet verification](FILTER-FOOTER-TABLET.md) resolves the fresh audit findings. Application guards cover shared typography plus all properties on rendered footer/status/count aliases and the Reset data hook. Shared sources remain read-only.

Historical [heading/venue verification](HEADINGS-VENUE-SCOPE.md) covers the original control set, unique heading, scoped native routes and exact venue ID. Tide remains unchanged.
