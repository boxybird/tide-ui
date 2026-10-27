# Burque events example · 2.0.2

A browser-JavaScript-free HTML/CSS consumer of Tide 1.5.2. All 54 events are authored samples. The original 60 routes remain, plus Music, Comedy, Workshop and empty-result specimens: 64 documents in the default app and each of ten theme/mode combinations.

Desktop keeps the centered 92rem maximum and 20/35/45 filters/list/detail proportions. CSS Grid/subgrid, native scrolling, sticky month headers and viewport units supply layout. The result summary sits outside the feed scroller, so no height observer is needed. Narrow layouts keep the one original control set in the document with native disclosures. There is no scripted drawer or duplicated form.

Native links, fragments, browser Back, input controls, reset, required/type validation and file selection remain. Free-text/date matching, live result counts, fetched previews, session state and photo/inspection message hooks are removed. Controls are explicitly labelled examples. Use the authored result-state links to review populated/category/empty layouts; URL query values are not evaluated. No backend or service is introduced.

Run `npm run build`, `npm run check`, `npm run dev` from the root. Open `/events/app/index.html`; `/events/index.html` links to all modes. Node/Python are development tools only. See [zero-browser-JavaScript policy](../../docs/NO-BROWSER-JAVASCRIPT.md).

Canonical sources are `src/templates/`, three unique fragments in `src/pages/`, the five `src/styles/` modules and structured `data/` fixtures. `data/events.json` owns events, `data/pages.json` owns ten non-event routes and typed authored result states, and `data/submission-fields.json` owns eleven submission fields. The renderer escapes text and rejects unknown/missing/cyclic includes. Never edit generated copies.

See [runtime boundary](docs/RUNTIME.md), [desktop composition](docs/DESKTOP-LAYOUT.md), [template ownership](docs/TEMPLATES.md), [document composition](docs/PAGES.md) and [performance observations](docs/PERFORMANCE.md). Browser evidence remains Chromium; other browser/device/assistive-technology checks are deferred.
