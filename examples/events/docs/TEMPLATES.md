# Shared app HTML

This example uses build-time partials, not browser rendering. The UI kit's canonical component recipes and CSS remain unchanged. App partials compose those existing components for this product; they do not become a competing kit implementation.

## Source ownership

| Source | Owns |
| --- | --- |
| `src/pages/*.html` | Native route documents and individual event details, venue guide, help or submission content |
| `src/templates/header.html` | Brand and navigation, including existing secondary-link and current-page variants |
| `filter-rail.html`, `filters.html`, `filter-dialog.html` | One original GET form/control set, desktop rail and responsive dialog shell |
| `results-intro.html`, `lineup-summary.html`, `summary-*.html` | Existing heading levels, counts, applied badge and filter toggle |
| `event-list.html`, `month-group.html`, `month-nav.html`, `month-jump.html` | Complete-feed isolation, stable calendar IDs, grouping and jumps |
| `event-card.html` | One card recipe, selected modifier/status, authored dataset and date/time/admission markup |
| `empty-results.html`, `results-footer.html` | Existing recovery and list footer variants |
| `data/event-list.json` | Canonical 54 authored cards, in approved order; shared by rendering and search tests |
| `data/pages.json` | Six non-event route contexts: collection, selection and navigation state |
| `tools/html_templates.py` | Escaped value substitution and explicit collection/route composition |

All template names and list-data homes are registered in `consumer-manifest.json`. The build fails for missing/unregistered partial files, unknown values/routes, malformed syntax and cyclic includes. Normal checks reject pasted header, filter, rail, dialog or card markup in route sources.

## Authoring

Insert a named partial with `{{> header}}`, `{{> filters}}` or `{{> event-list}}`. Includes accept only registered flat names. There is no arbitrary expression evaluation, filesystem traversal, browser fetch or client router.

Use `{{UPPERCASE_VALUE}}` for a value. Plain strings are HTML-escaped in text and quoted attributes. Never pre-escape sample text. The renderer's `Html` type is reserved for controlled attributes and composed partial output; never wrap organizer text in it. Values are substituted once, so text that resembles an include is not executed. `{{KIT_CSS}}`, `{{APP_CSS}}` and `{{KIT_ASSETS}}` remain reserved build-path placeholders.

The renderer explicitly composes repeated cards and calendar groups. The template syntax deliberately has no loops or conditionals. Optional fragments, current-link attributes and selected status are supplied by the typed composition functions. Keep new reusable app markup in a registered partial and add its context in the renderer rather than building HTML strings inside browser scripts.

The app builder expands every source route once, then emits the default app and all six theme/mode examples. Do not edit generated pages in `build/`. Run `npm run build` and `npm run check` from the repository root.

## Preserved state and content

Event route filenames select the corresponding card ID. Index/search retain High Desert Signal as their unfiltered preview. Sunshine Theater shows six exact-ID matches and initially selects no event. Saved reuses Ink After Dark, retaining its original shortlist dataset and heading/footer variants. Heading levels and navigation active states retain their existing per-route differences.

Calendar labels use fixed English month/day names and local ISO dates, independent of the build machine's locale. Authored start timestamps are retained; display-only ranges retain their existing span markup. The original 48-event and six-Sunshine JSON files remain provenance records. Event-detail prose stays in the route files; this extraction is not a new content-management or ingestion system.

The runtime still moves one original control set between rail and dialog. Native form association, live draft counts, Show events/Enter, Reset, Escape/focus restoration, URL state, venue scope, sticky offsets, scroll restoration and reduced-motion behavior retain their current contracts. App styles/scripts/assets are byte-identical to 1.1.1.
