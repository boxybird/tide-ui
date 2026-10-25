# Extraction map — Tide 1.3.0

The approved prototype is the immutable build input, not the migration target. New consumer pages live in `app/`; its styles and scripts no longer load the previous panel CSS or kit bundle.

| Accepted pattern | Implementation home | Reuse / host boundary |
| --- | --- | --- |
| Combined form | Canonical shared shell; one existing GET form in consumer | Field, Fieldset, Choice, Button. One input set is moved, never cloned. |
| Scroll body / pinned footer | `kit/css/filter-panel.css`, `.tide-filter-panel` | Optional header, body, footer, status-row and count. Rail modifier preserves flush alignment. |
| Live draft count / Show N | Panel count + existing full-width Button | Host `filters.js` calculates, pluralizes and updates one polite atomic status. Feed changes only on apply. |
| Reset / Cancel / Clear | Existing Button / Link | Host clears draft, rolls back modal snapshot, or navigates to clear applied URL. |
| Launcher | Existing quiet/icon Button | Host places it in header and manages dialog relationship/focus. |
| Applied context | Existing Badge, Result summary and Link | Host supplies wording and applied criteria. |
| Validation / zero | Existing Field error and Empty | Invalid date range blocks apply; zero is valid and recoverable. |
| Native modal | Host `filters.js` + native dialog | Header/body/footer use shared kit. Focus, Escape/backdrop, snapshot and VisualViewport remain integration behavior. |
| Margin Reveal / gutter | Host `rail.js`, `host.css`, ResizeObserver | Kit has no viewport breakpoint or 24px-plus-gutter product rule. |

## Removed duplicated styles

The consumer does not include `responsive-filters.css` or `unified-search.css`. Its generated host stylesheet omits the legacy `.tide-shell__rail`, `__filter-scroll`, `__action-dock`, `.tide-slide-study__scroller` and `.tide-browse-flyout__body` rules. Status-row/count/apply private styles are absent. The rail/footer and native dialog use the new block and existing `.tide-button--full`.

Only host dimensions, column placement, breakpoint, disclosure animation, query/group placement and viewport inputs remain. The modal shell is generated with `kit/tools/filter_panel.py`, exactly like the static kit specimens. The desktop adapter creates the two BEM body/footer elements around the same original form nodes. Source checks reject a reintroduction of old panel classes or any host CSS selector styling the shared block.

The new CSS is additive in `tide.components.extensions`. The existing component, primitive, palette and content CSS sources are byte-identical to 1.2.1. All theme/mode example bodies are generated from one template. The kit still ships zero browser scripts or inline styling.
