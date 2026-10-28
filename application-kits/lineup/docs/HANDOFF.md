# Lineup interface and handoff · 2.1.4

Lineup's application interface uses ordinary product language. It contains no tutorial result-state menu, forced “No results” link, control-example labels or design-study notices. Search, dates and categories remain a single native form. Reference layouts remain available to kit reviewers outside the application journey; their paths and event/venue IDs are preserved.

## Native HTML and modern CSS

The delivered application has no JavaScript files, script elements, inline handlers or JavaScript URLs. Node and Python only build, serve and check the kit.

The mobile/tablet drawer already used the browser's `popover="auto"` and `popovertarget` controls. CSS owns its left placement, `100dvh` sizing, scrolling body, pinned footer and background scroll restraint. `@starting-style` with discrete `display`/`overlay` transitions animates entry and exit; `prefers-reduced-motion` removes that motion. At 75rem the original control set becomes the permanent desktop column. CSS anchor positioning, with a grid-geometry fallback, fits a still-open top-layer drawer when the viewport widens. No script migration or replacement drawer is necessary.

Links, browser history, month fragments, details/summary, form reset, required/type validation and local file selection remain native. Grid/subgrid, sticky positioning and scrollbar gutters handle layout. Tide's component recipes and appearance are unchanged.

## Integration contract

This is an HTML/CSS application kit, not an operating events service. Removing tutorial presentation does not add search matching, persistence, booking or submission services.

For optional enhanced navigation, replacement regions, search/collection state, pagination, loading/motion, return context and upgrade verification, use the [consumer integration guide](CONSUMER-INTEGRATION.md). Complete native documents remain the foundation; an independent consumer chooses its runtime and response protocol. The guide adds no application scripts, framework requirement or public selector API.

- The search form sends a native GET request with `q`, `from`, `to`, repeated `category` values and `venue`. Its global action is `search.html`; venue actions remain at `sunshine-theater.html`. The local static preview serves those documents without evaluating query parameters, so changed input values do not change the result set or count. The recipient can connect this form contract to its own server. CSS is not a text/date search engine.
- Saved contains an authored shortlist. Links open that page; they do not store a selection.
- The submission layout preserves labels, required/type constraints, hints, permission and local file selection. It has Reset and Back actions, with no operational submission/upload endpoint or submit control.
- Category and empty documents are reference layouts generated at build time. `/events/index.html` is the kit review entry; the website's filter panel and Help do not link to those reference states. Native recovery links retain venue scope.

These boundaries describe the delivered kit; services, hosting and deployment are outside this task's completion criteria.

## Content provenance

All 54 events are fictional authored fixtures, including the six Sunshine Theater events. Their names, dates, prices and admission conditions are not real listings. Event photography is illustrative; the concert photograph does not depict Sunshine Theater. Replace the fixture catalog and photography for a real service. Original source fixture files retain their historical provenance. The venue profile retains its separately attributed facts, source links and checked date.

Developer explanations and fixture provenance belong in these kit documents and the review entry, outside the customer interface.

## Verification

In-app Chromium on Windows, 2026-10-27:

- 39 layout/content cases: index, venue and Saved at 320, 390, 768, 1024, 1199, 1200 and 1440 pixels; venue-empty, global-empty, concise/full event details, Help and submission at 390, 1024 and 1440 pixels. Heights were 900 pixels. Each had one visible h1, no horizontal document overflow, zero browser scripts and no tutorial copy or reference-state links.
- 20 theme cases: the index in all five themes/light-dark modes at 390 and 1440 pixels. Each phone drawer opened; each desktop panel remained in its original column with 24px bottom clearance. No tutorial copy, reference links, script elements or horizontal document overflow appeared.
- At 390×844, native Reset cleared query, dates and category choices; Close and Escape dismissed the drawer and returned focus to Filters. Outside-click dismissal passed at 768×900. At 320×500, selecting the last category scrolled the body while the footer remained inside the viewport.
- Widening an open phone drawer to 1440×900 retained the entered query and exactly one search input. Its top-layer rectangle matched the reserved desktop column. Native dismissal retained the permanent desktop panel; narrowing hid the closed drawer.
- At 1024×900, venue Reset returned from the empty Comedy reference to six exact venue cards. The global native form submitted `q` and a category to `search.html`; the static result count stayed at 54, confirming the documented integration boundary.

`npm run build` and `npm run check` passed: 737 application documents, the kit review entry, 41 application tests, 66 Tide tests, HTTP regressions and all document/reference/script-boundary checks. The initial HTTP run hit sandbox loopback `EACCES`; the final run with local-network access passed. Routine screenshots and expanded measurements live under ignored `build/qa/lineup-handoff/`.

Earlier [Tide alignment evidence](TIDE-ALIGNMENT.md) remains the appearance baseline; it predates this copy cleanup. The native drawer CSS is unchanged, including reduced motion. Current-run evidence does not cover Firefox/Safari, physical devices, screen readers or changing the reduced-motion system preference. Shared-source review confirms all canonical edits are inside Lineup; Tide, the reference site, sibling kits and shared tooling are unchanged.
