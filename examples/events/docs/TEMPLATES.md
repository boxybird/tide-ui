# Build-time templates · App 2.0.0

The browser receives complete native HTML/CSS. There is no browser template engine, router or script. Every partial is registered in `consumer-manifest.json` and rendered by `tools/html_templates.py`.

Only `{{UPPERCASE_VALUE}}` and `{{> registered-partial}}` are supported. Plain values are HTML-escaped. `Html` is reserved for markup assembled by trusted build-time composition, never raw HTML in sample JSON. Missing values/partials, invalid paths, unknown routes and cyclic includes fail the build.

| Home | Ownership |
| --- | --- |
| `document.html`, `workspace.html` | Native document and main browse/detail slots; stylesheets only |
| `workspace-browse.html`, `workspace-results.html` | Static filter/list grouping and results region |
| `filter-rail.html`, `filters.html`, `filter-status.html`, `filter-actions.html` | One native form/control set, disclosures, reset and static result-state links |
| `results-intro.html`, `lineup-summary.html`, `month-group.html` | Authored headings/counts and month-name/year spans; no DOM rewriting |
| `event-list.html`, `month-nav.html`, `month-jump.html` | Summary outside the native feed scroller, stable fragment destinations and complete-feed isolation |
| `event-card.html`, `event-detail.html`, `detail-*.html` | Cards and all 54 native event details, with authored preview heading levels |
| `data/events.json`, `data/detail-presentations.json` | The canonical 54 sample events and full/concise presentation defaults |
| `data/pages.json` | Ten non-event routes, including four typed category/empty result states |
| `form-*.html`, `data/submission-fields.json` | Eleven native submission fields with original IDs, hints and constraints |
| `src/pages/` | Only unique venue information, help and submission content |

The builder emits 64 documents in the default app and all ten theme/mode combinations. The original native paths remain. Authored category specimens select their category at build time; arbitrary URL query strings do not filter, mutate previews or invoke browser behavior. The empty specimen retains useful recovery links and a visible preview placeholder.

Source/markup contracts verify event selection, one original form, labels/IDs, route contexts, category counts, escaping and zero script dependencies. See [native runtime boundary](RUNTIME.md) and [document composition](PAGES.md).
