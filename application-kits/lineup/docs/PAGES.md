# Native document composition · App 2.0.0

Every one of the 68 native routes uses `document.html`. Sixty-five event/list/search/saved/venue/result-state routes share `workspace.html`; Help, submission and the Venues directory retain their own main layouts. There are four unique fragments in `src/pages/`. Browser script inventories are empty.

| Source | Contract |
| --- | --- |
| `document.html` | Doctype, language/theme/mode, metadata, escaped title, stylesheets and header; no scripts |
| `workspace.html` | Complete browse/detail slots and preview placeholder |
| `workspace-browse.html`, `workspace-results.html` | Authored browse grouping and results region; saved omits the filter column |
| `filter-rail.html`, `filter-status.html`, `filter-actions.html` | Initial panel/body/footer, one native form and native reset |
| `event-list.html` | Fixed summary followed by a separate native feed scroller containing month groups, empty state and footer |
| `preview-state.html` | Visible for the authored empty result state, hidden for populated previews |
| `form-field.html`, `form-input.html`, `form-textarea.html`, `form-select.html` | Native submission field markup from the eleven registered definitions |
| `form-hint.html`, `form-optional.html`, `form-option.html` | Associated hints, optional labels and native choices |

`data/pages.json` owns fourteen non-event routes. Three category specimens and an empty-result specimen use a restricted `sampleFilter` object; the build rejects unknown categories/keys. Event titles and facts come from the 54 canonical records. Context values are escaped and script/HTML injection is not accepted in sample data.

`header.html` consumes Tide's Site header/navigation list recipe; `skip-link.html` consumes its native Skip link helper. Only an exact route/destination match receives `aria-current="page"`. The utility-page titles name Saved events, Help & guidance and Add an event, followed by Burque; 48 event metadata titles also drop the same retired prefix. Retired study names remain only in historical provenance/evidence.

Native skip links retain event/detail/results/main targets and focusable destinations. Empty results target the actual preview placeholder. Exact venue identity and authored facts remain; no runtime venue rewriting or query-state recovery is supplied. Saved remains a fixed sample shortlist. The native submission specimen still has no operational submit service, upload endpoint or account behavior.

`data/submission-fields.json` retains IDs/names, required/optional markers, hint associations, native types, maxlength and autocomplete. File chooser, permission markup and unique prose remain authored HTML. Native reset restores source defaults; browser validation supplies native required/type checks. There is no JavaScript validation summary controller.

See [template grammar](TEMPLATES.md), [event content](DETAILS.md), [runtime boundary](RUNTIME.md) and [desktop composition](DESKTOP-LAYOUT.md). Build/check generate and inspect all ten modes; browser evidence is Chromium on Windows, with other browsers/devices/screen readers deferred.
