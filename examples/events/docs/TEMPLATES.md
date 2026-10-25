# Shared app HTML

This example uses build-time partials, not browser rendering. The UI kit's canonical component recipes and CSS remain unchanged. App partials compose those existing components for this product; they do not become a competing kit implementation.

## Source ownership

| Source | Owns |
| --- | --- |
| `src/pages/*.html` | Three unique content fragments: venue information, help and submission; no document or workspace copies |
| `src/templates/header.html` | Brand and navigation, including existing secondary-link and current-page variants |
| `filter-rail.html`, `filters.html`, `filter-dialog.html` | One original GET form/control set, desktop rail and responsive dialog shell |
| `results-intro.html`, `lineup-summary.html`, `summary-*.html` | Existing heading levels, counts, applied badge and filter toggle |
| `event-list.html`, `month-group.html`, `month-nav.html`, `month-jump.html` | Complete-feed isolation, stable calendar IDs, grouping and jumps |
| `event-card.html` | One card recipe, selected modifier/status, authored dataset and date/time/admission markup |
| `empty-results.html`, `results-footer.html` | Existing recovery and list footer variants |
| `data/events.json` | Canonical 54 authored events, including card fields and structured detail content; shared by rendering and search tests |
| `data/pages.json` | Six non-event route contexts: collection, selection, navigation, document title, layout and optional unique source |
| `document.html`, `workspace.html`, `skip-link.html`, `site-footer.html`, `preview-state.html`, `venue-script.html` | Shared document/workspace with explicit native route variants |
| `event-detail.html`, `detail-*.html` | One detail composition, structured sections and existing inline icons |
| `data/detail-presentations.json` | Existing full/concise structural defaults and common labels |
| `form-*.html`, `data/submission-fields.json`, `tools/form_fields.py` | Eleven existing native submission fields, labels, optional states and hints |
| `tools/html_templates.py` | Explicit list/route/document composition and generation of all native documents |
| `tools/template_engine.py` | Escaped value substitution and registered includes |
| `tools/event_details.py` | Structured detail rendering, heading levels and supported content blocks |

All template names and list-data homes are registered in `consumer-manifest.json`. The build fails for missing/unregistered partial files, unknown values/routes, malformed syntax and cyclic includes. Normal checks reject pasted document wrappers/scripts, header, workspace, filter, rail, dialog, card, standard field wrapper, footer or preview-state markup in unique content fragments.

## Authoring

Insert a named partial with `{{> header}}`, `{{> filters}}` or `{{> event-list}}`. Includes accept only registered flat names. There is no arbitrary expression evaluation, filesystem traversal, browser fetch or client router.

Use `{{UPPERCASE_VALUE}}` for a value. Plain strings are HTML-escaped in text and quoted attributes. Never pre-escape sample text. The renderer's `Html` type is reserved for controlled attributes and composed partial output; never wrap organizer text in it. Values are substituted once, so text that resembles an include is not executed. `{{KIT_CSS}}`, `{{APP_CSS}}` and `{{KIT_ASSETS}}` remain reserved build-path placeholders.

The renderer explicitly composes repeated cards and calendar groups. The template syntax deliberately has no loops or conditionals. Optional fragments, current-link attributes and selected status are supplied by the typed composition functions. Keep new reusable app markup in a registered partial and add its context in the renderer rather than building HTML strings inside browser scripts.

The app builder composes all 60 native documents from `document.html`. Fifty-eight routes share `workspace.html`; only the three registered unique content fragments are read from `src/pages/`. Event details and submission fields use their respective sample data. It then emits the default app and all six theme/mode examples. Do not edit generated pages in `build/`. Run `npm run build` and `npm run check` from the repository root.

## Preserved state and content

Canonical sample IDs determine native event filenames and select their corresponding card. Index/search retain High Desert Signal as their unfiltered preview. Sunshine Theater shows six exact-ID matches and initially selects no event. Saved reuses Ink After Dark, retaining its original shortlist dataset and heading/footer variants. Heading levels and navigation active states retain their existing per-route differences.

Calendar labels use fixed English month/day names and local ISO dates, independent of the build machine's locale. Authored start timestamps are retained; display-only ranges retain their existing span markup. The original 48-event and six-Sunshine JSON files remain provenance records. Event-detail prose now lives in structured sample data. The [detail contract](DETAILS.md) documents supported blocks and existing presentation variants. The [page contract](PAGES.md) documents document profiles, utility content and submission fields. This remains a sample app rather than a content-management or ingestion system.

The runtime still moves one original control set between rail and dialog. Native form association, live draft counts, Show events/Enter, Reset, Escape/focus restoration, URL state, venue scope, sticky offsets, scroll restoration and reduced-motion behavior retain their current contracts. App styles/scripts/assets remain byte-identical to the approved baseline.
