# Build-time templates · App 2.0.0

The browser receives complete native HTML/CSS. There is no browser template engine, router or script. Every partial is registered in `consumer-manifest.json` and rendered by `tools/html_templates.py`.

Only `{{UPPERCASE_VALUE}}` and `{{> registered-partial}}` are supported. Plain values are HTML-escaped. `Html` is reserved for markup assembled by trusted build-time composition, never raw HTML in sample JSON. Missing values/partials, invalid paths, unknown routes and cyclic includes fail the build.

| Home | Ownership |
| --- | --- |
| `document.html`, `workspace.html` | Native document and main browse/detail slots; stylesheets only |
| `workspace-browse.html`, `workspace-results.html` | Static filter/list grouping and results region |
| `filter-trigger.html`, `filter-rail.html`, `filters.html`, `filter-status.html`, `filter-actions.html` | Native popover trigger/close and one responsive panel/form/control set, disclosures, reset and static result-state links |
| `results-intro.html`, `lineup-summary.html`, `month-group.html` | Canonical Page intro, Results and calendar slots; private context wrapper beside Results, plain month/year text; no DOM rewriting or private type aliases |
| `event-list.html`, `month-nav.html`, `month-jump.html` | Summary outside the native feed scroller, stable fragment destinations and complete-feed isolation |
| `event-card.html`, `event-detail.html`, `detail-*.html` | Cards and all 54 native event details, with authored preview heading levels |
| `data/events.json`, `data/detail-presentations.json` | The canonical 54 sample events and full/concise presentation defaults |
| `data/pages.json` | Thirteen non-event routes, including global result fixtures and three venue-owned empty views |
| `form-*.html`, `data/submission-fields.json` | Eleven native submission fields with original IDs, hints and constraints |
| `src/pages/` | Only unique venue information, help and submission content |

The builder emits 67 documents in the default app and all ten theme/mode combinations. The original native paths remain. Authored category specimens select their category at build time; arbitrary URL query strings do not filter, mutate previews or invoke browser behavior. The global empty specimen retains recovery links and a preview placeholder; venue empty views retain their venue information instead.

Source/markup contracts verify event selection, one original form, labels/IDs, route contexts, category counts, escaping and zero script dependencies. See [native runtime boundary](RUNTIME.md) and [document composition](PAGES.md).

`workspace-browse.html` now owns the single ordinary-document heading outside the popover. `scope-link.html` composes native context/exit links; `filter-reset.html` chooses a global native reset button or scoped venue navigation link. Venue owner/result destinations and empty recovery are documented in [heading and venue contracts](HEADINGS-VENUE-SCOPE.md).
