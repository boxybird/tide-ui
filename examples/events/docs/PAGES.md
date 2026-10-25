# Document, venue and utility-page composition

The remaining pages were reviewed for actual repetition. Every one of the 60 native routes uses `document.html`. The 58 event/list/search/saved/venue routes also share `workspace.html`; help and submission retain their distinct main layouts. Only three unique fragments remain in `src/pages/`, explicitly registered through `data/pages.json`. No new browser renderer, router, CSS component or kit release is involved.

## Shared pieces

| Home | Contract |
| --- | --- |
| `document.html` | One doctype, HTML language/theme/mode, metadata, escaped title, stylesheet order, deferred script order, body attributes and shared header |
| `skip-link.html` | Native route-specific targets, text and existing detail-link modifier |
| `site-footer.html` | Existing sample disclaimer; help retains its own content footer instead |
| `workspace.html` | Existing results container and detail slot; saved omits rail and filter controls |
| `preview-state.html` | Existing hidden preview placeholder, IDs, heading level and focus target |
| `venue-script.html` | Existing venue-context enhancement, inserted after search-core only on routes that already loaded it |
| `form-field.html`, `form-input.html`, `form-textarea.html`, `form-select.html` | Existing kit field/label/control markup composed for eleven submission fields |
| `form-hint.html`, `form-optional.html`, `form-option.html` | Associated hints, optional label suffix and native select choices |

`data/pages.json` owns the six non-event routes, document titles, workspace/content layout choice, optional unique source and existing navigation/collection context. Event titles continue to come from `data/events.json`. `tools/html_templates.py` composes the document profiles explicitly rather than accepting arbitrary HTML attributes or script paths from data. All templates and data homes remain registered in `consumer-manifest.json`.

## Preserved route differences

| Routes | Session key before the existing theme suffix | Scripts | Skip targets | Filter rail/dialog |
| --- | --- | --- | --- | --- |
| Individual events | `app-release-1.1.0` | Nine, including app-runtime and venue-context | Event detail | Yes |
| Index/search | `app-release-1.1.0` | Nine, including app-runtime and venue-context | Results and event preview | Yes |
| Sunshine Theater | `app-release-1.1.0` | Nine, including app-runtime and venue-context | Results and venue information | Yes |
| Saved | `margin-aligned` | Eight, without venue-context | Results and event preview | No |
| Help/submission | `margin-aligned` | Eight, without venue-context | Main content | No |

Body classes, exact venue identity, active navigation, focused targets, script execution order, native URLs, sticky hierarchy, bounded scroll panes and responsive filter placement retain their prior behavior. The app stylesheet is unchanged; JavaScript retains these contracts through the shared services documented in [runtime ownership](RUNTIME.md).

## Submission fields

`data/submission-fields.json` supplies the eleven existing fields: ID, native name, plain label, input/textarea/select kind, supported input type, required/optional state, optional hint, maxlength/autocomplete and select choices. `tools/form_fields.py` composes registered partials. Each field has exactly one slot in the authored submission fragment; duplicate, missing or orphan slots fail the build.

Text and quoted values are escaped using the existing template engine. Control kinds/input types and data keys are restricted; IDs/names must be plain identifiers. No raw HTML, arbitrary attribute names, event handlers, upload service or submission endpoint is accepted. A hint derives its ID from the control and retains `aria-describedby`. Required/optional states, native date/time/email behavior, the empty first category option, maxlength, autocomplete and native reset remain unchanged. The form still has no submit button.

The photo upload, permission checkbox, paired field rows and form-section composition occur once and stay in `src/pages/submit.html`. Its back icon reuses the existing registered SVG partial. This is app composition of established kit recipes; the kit itself is not modified.

## Deliberately unique HTML

Sunshine Theater's information, attributed facts, contact/directions links and visit guidance remain in `src/pages/sunshine-theater.html`. Help's content-page layout, contents navigation, prose, table and footer remain in `src/pages/help.html`. These are trusted authored content, not duplicated app shells. Neither needs a generic data-driven content system for this cleanup. All copy remains verbatim, including existing preview limitations.

Source checks reject document wrappers/scripts/shared header, workspace, standard field wrappers, site footer and preview-state copies inside these fragments. All native pages still generate in the default app and the six theme/mode examples. Run the root build/check commands; never edit generated theme copies.
