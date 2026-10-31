# Build-time templates · Lineup 2.4.10

The browser receives complete native HTML/CSS. There is no browser template engine or router. Only the venue directory loads the registered map runtime. Every partial is registered in `consumer-manifest.json` and rendered by `tools/html_templates.py`.

Only `{{UPPERCASE_VALUE}}` and `{{> registered-partial}}` are supported. Plain values are HTML-escaped. `Html` is reserved for markup assembled by trusted build-time composition, never raw HTML in sample JSON. Missing values/partials, invalid paths, unknown routes and cyclic includes fail the build.

| Home | Ownership |
| --- | --- |
| `header.html`, `skip-link.html` | Canonical Tide Site header/list/link and Skip link recipes; native destinations, exact current page and route-appropriate focusable fragments |
| `document.html`, `workspace.html` | Native document and main browse/detail slots; stylesheets and the directory-only registered map runtime |
| `workspace-browse.html`, `workspace-results.html`, `browse-search.html` | Static filter/list grouping, results region and the single search form above the list on Find Events |
| `filter-trigger.html`, `filter-rail.html`, `filter-search.html`, `filters.html`, `filter-navigation.html`, `filter-status.html`, `filter-actions.html` | Native popover trigger/close and one responsive panel/form/control set, visible fieldsets, reset and venue-only navigation; no tutorial result-state menu |
| `results-intro.html`, `lineup-summary.html`, `month-group.html` | Canonical Page intro, Results and calendar slots; canonical utility headers with a screen-reader context prefix, plain month/year text; no DOM rewriting or private type aliases |
| `event-list.html`, `month-nav.html`, `month-jump.html` | Summary outside the native feed scroller, stable fragment destinations and complete-feed isolation |
| `event-card.html`, `event-detail.html`, `detail-*.html` | Cards and all 54 native event details, with authored preview heading levels |
| `venue-hero-open.html`, `venue-hero-close.html` | Tide photo-hero composition around Sunshine's authored venue information; owner-selected private host keeps its height aligned with Sunshine event heroes |
| `data/events.json`, `data/detail-presentations.json` | The canonical 54 sample events and full/concise presentation defaults |
| `data/pages.json` | Nineteen non-event routes, including the directory, global result fixtures, three venue-owned empty views and the homepage/search `workspacePresentation` setting; the homepage-only `filterPresentation: push` requires a split workspace |
| `form-*.html`, `data/submission-fields.json` | Eleven native submission fields with original IDs, hints and constraints |
| `src/pages/` | Four unique fragments: venue information, venue directory, Help and submission content |

The builder emits 73 documents in the default app and all ten theme/mode combinations. The original native paths remain. Authored category specimens select their category at build time; arbitrary URL query strings do not filter, mutate previews or invoke browser behavior. The global empty specimen retains recovery links and a preview placeholder; venue empty views retain their venue information instead. All six venue profiles share the workspace and profile shell; the directory retains its map/list composition. See [venue context](VENUE-CONTEXT.md).

Source/markup contracts verify event selection, one original form, labels/IDs, route contexts, category counts, escaping and the directory-only script boundary. See [native runtime boundary](RUNTIME.md) and [document composition](PAGES.md).

`lineup-summary.html` now owns the visible count heading outside the popover. `filter-heading.html` supplies its aligned desktop utility label; see the [compact-header contract](COMPACT-HEADERS.md). `scope-link.html` composes native context/exit links; `filter-reset.html` chooses a global native reset button or scoped venue navigation link. Venue owner/result destinations and empty recovery are documented in [heading and venue contracts](HEADINGS-VENUE-SCOPE.md).
