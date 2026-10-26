# Search and filters — kit 1.3.0

The Filter panel is the only new block. Field, Fieldset, Choice, Button, Badge, Result summary, Empty state, Notice and native Expandable keep their existing definitions. No primitive, palette seed, type size, radius or target size changes.

## Ownership

`css/filter-panel.css` ships in `tide.components.extensions`. `templates/filter-panel.html` and `tools/filter_panel.py` supply the same shell to the kit specimens and consumer app. `component-manifest.json` registers the block, states and reused patterns. `templates/frames/filter-panel.html` generates identical HTML in every registered theme, each light and dark.

The host owns the native aside/dialog, placement, available height, breakpoint, matching, validation, URL routing, pluralization, opening snapshot, focus restoration and viewport handling. The kit adds no browser runtime. The consumer's scripts are an integration example, not a kit service.

## Filter panel

Use `.tide-filter-panel` on an aside, section or native dialog. Give the region a meaningful accessible name. Use an optional `__header` with `__title` and `__description`, followed by `__body` and `__footer`. The body scrolls; the footer stays outside that scroll region. The host must supply a bounded available block size. Never introduce a second nested scrolling body.

`__status-row` contains an existing quiet Button for Reset all and `__count`. The count uses secondary text, caption size and inherited body leading. Only the dynamic count is a polite atomic live status; do not announce every button-label change separately. Use `.tide-button--full` for Show events. Do not create panel-specific button variants.

The `--rail` modifier removes the body inset and gives the footer a flush start, 24px end inset, 16px top inset and zero bottom inset. This supports existing rail sections that already own their end padding. Header-gutter alignment, column gaps and list/footer bottom alignment remain host geometry. No negative-margin correction or per-control padding reset is required.

Default body spacing is 32px, padding 24px. Footer gap is 16px with 20px top and 24px side/bottom padding (safe-area-aware). The optional header uses the existing page type and a neutral separator. There is no decorative panel frame or colored left border. Native scrollbars remain available; thin is the existing panel preference, not a guaranteed pixel width. The app measures occupied list gutter space separately.

## Combined form

One GET form owns query, From, Through and category checkboxes. If moved outside the form, controls and Show events retain `form="event-search-form"`. Move the original controls between presentations; do not clone controls, duplicate IDs or maintain independent drafts. A standalone Field is sufficient for a query with no adjacent submit; keep Search line's existing two-column contract for other uses.

Enter and Show events submit the same combined form. Dates are inclusive and interpreted in the event's local time zone. Category selections combine with OR; query, dates and categories combine with AND. Keep accessible labels, fieldset legends and validation descriptions. Invalid dates block submission through native validity; zero matches must remain submittable.

## State and action contract

| State/action | Required behavior |
| --- | --- |
| Clean draft | 48 matching events, Reset all disabled, Show 48 events. |
| Edit query/date/category | Update draft count and submit wording without moving focus. Applied feed stays unchanged. |
| One match | “1 matching event” and “Show 1 event.” |
| No matches | “0 matching events”; Show remains enabled; apply reveals existing Empty state. |
| Invalid range | Describe the error on Through; count says “Check the date range”; native validity prevents applying. |
| Reset all | Clear query, dates and categories to empty choices. Do not use native reset-to-initial-values for a URL-prefilled form. Do not navigate. |
| Modal Cancel/Escape/backdrop | Restore opening values, dismiss and return focus to launcher. |
| Desktop Close | Hide rail, retain draft and restore launcher focus. |
| Show events / Enter | Apply all controls via GET. Feed count and month groups reflect applied matches. |
| Clear all | Navigate to the unapplied URL. Reuse Link, not a new removable-chip component. |
| Resize | Keep exactly one set of controls. Roll back an open modal before moving into desktop. Clean up modal and scrollbar observers/inputs below their owning breakpoint. |
| Refresh / Back | Restore applied criteria from URL; keep existing navigation/reading-position enhancement. |

## Modal and progressive enhancement

Use native `dialog.showModal()` with a labelled title, explicit Cancel, Escape handling, backdrop dismissal and focus return. A modal draft must be recoverable. Keep the title programmatically focusable, not in the ordinary Tab order. Keyboard focus stays within the modal. The app can adjust available height using VisualViewport while preserving pinch zoom; physical software-keyboard testing remains a separate check.

Without scripts, expose the real query form, native disclosure, date/category controls and combined submit in the document. The closed dialog is hidden even though the block normally uses grid. The launcher reuses Button and Icon; its name and dialog relationship remain available when its text label is hidden.

## Applied context and coverage

Reuse Badge for descriptive applied categories and In view, Result summary for applied counts, Field error for invalid dates, and Empty state for zero results. A live draft count is not an applied result count. Sorting text must not look like an interactive control if sorting is unavailable.

Static all-mode fixtures cover clean/disabled reset, native focus, checked controls, one/zero wording, invalid fields and applied context. The independent app copy exercises live count, reset, rollback, GET apply, resize and native gutter alignment. The approved Unified Search 1.0.2 prototype and frozen kit 1.2.1 remain byte-identical. Browser evidence is Chromium only; Firefox/Safari and assistive-technology/physical-device checks are deferred, not passed.
