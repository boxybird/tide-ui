# Native component ownership · Lineup 2.0.5

The Lineup application kit consumes Tide 1.10.0 and contains no browser JavaScript. Shared component CSS/HTML remains kit-owned; private composition and authored result states remain app-owned.

| Responsibility | Canonical home |
| --- | --- |
| Event cards, hero/details, fields, notices, badges, prose, native controls and filter-panel internals | `packages/tide/` component recipes and CSS |
| 20/35/45 centered desktop layout, bounded left panes and natural right document | `src/styles/desktop.css`, static `tide-app--columns` body modifier and authored workspace templates |
| Saved desktop tracks | `desktop.css`: results in column 1, detail in column 2; scoped browse overrides keep their three-column placement |
| Canonical component typography | Tide recipes; `test_presentation.py` rejects private aliases that override shared type across rendered routes |
| Permanent summary and native scrolling feed | `event-list.html`, `lineup-summary.html`, `lineup.css`; private context wrapper beside canonical Results; summary outside `.tide-app__feed-scroll`, isolated complete feed inside |
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
