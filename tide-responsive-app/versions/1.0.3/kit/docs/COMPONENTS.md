# Component inventory and HTML contract

The rendered component list is the library's Components section. Its source is `templates/library.html`; screen compositions live in `templates/frames/`. Every rendered theme uses the same BEM markup and CSS. `component-manifest.json` provides a machine-readable index.

## Inventory

| Component / composition | BEM block | Included states or variants | Source specimen |
| --- | --- | --- | --- |
| Text action | `tide-button` | Primary, secondary, quiet, full width, icon-only, disabled, focus, hover/pressed | Library; search; submit |
| Icon action | `tide-icon-button` | Rest, selected, focus specimen | Library |
| Photo action | `tide-photo-control` | Back link; save visual specimen | Full-screen event |
| Brand and saved navigation | `tide-brand`, `tide-saved-link` | List/app-bar placements, focus | List; search |
| Text/select/textarea field | `tide-field` | Default/value, placeholder, invalid + description, disabled, required | Library; submit |
| Native checkbox/radio | `tide-choice` | Unchecked, checked, keyboard, reset | Library; filters |
| Filter chip | `tide-chip` | Static selected specimen; native checked choice; filter link | Library; filters |
| Status badge | `tide-badge` | Neutral, success, warning, danger, explicit status text | Library; states |
| Callout | `tide-notice` | Recovery, success, cancellation and informational wording; same neutral border | Library; states; received |
| Toast specimen | `tide-toast` | Message + follow-up link | Library |
| Organizer | `tide-organizer` | Organizer details + contact | Library |
| Sponsored placement | `tide-partner` | Explicit sponsored label | Library |
| Event card and date | `tide-event-card`, `tide-date` | Default, link focus, hover; long title wraps; no image dependency | List; search; saved |
| Empty result/saved state | `tide-empty` | Explanation + next action | No results; saved empty |
| Missing-photo surface | `tide-fallback` | Event heading + no-photo label | Review; states |
| File field | `tide-upload` | Optional native file selector + guidance | Submit |
| Event photo opening | `tide-event-hero` | Full viewport, photo scrim, facts and action, short viewport | Event |
| Scrolling event details | `tide-event-details` | Inclusions, schedule, practical details, disclosure | Event |
| App compositions | `tide-appbar`, `tide-page-intro`, `tide-page-body`, `tide-form-section`, `tide-summary`, `tide-results`, `tide-screen-footer` | Eleven complete screen/state fixtures | Frames |
| Spacing compositions | `tide-stack`, `tide-row`, `tide-split` | Fixed shared gaps, row wrap, narrow split gap | Across fixtures |
| Additive panel example | `tide-panel` | New block consuming the existing contract | `extensions/index.html` |

## HTML examples

An action that navigates is an anchor. An action that changes local state or submits a form is a button. Give icon-only buttons a meaningful accessible name. Use native disabled semantics rather than only a dimmed class.

```html
<a class="tide-button" href="event.html">View event</a>
<button class="tide-button tide-button--secondary" type="button">Save event</button>
<button class="tide-button" type="button" disabled>Unavailable</button>
<button class="tide-icon-button" type="button" aria-pressed="true" aria-label="Save event">
  <svg class="tide-icon" viewBox="0 0 15 15" aria-hidden="true" focusable="false">…</svg>
</button>
```

The real application must update aria-pressed and the visible save state together. The isolated selected/focus examples in the library demonstrate appearance only. A stateful control still needs its actual application behavior.

```html
<div class="tide-field">
  <label class="tide-field__label" for="venue">Venue</label>
  <input class="tide-field__control" id="venue" type="text"
    aria-invalid="true" aria-describedby="venue-error" required>
  <small class="tide-field__error" id="venue-error">
    Enter the venue name so people know where to go.
  </small>
</div>
```

Do not mark an untouched required field invalid on initial load. When application validation fails, preserve the entered values, connect the error to its field, and provide a useful next step. Native required-field validation works in the static form; asynchronous validation is outside this kit.

```html
<label class="tide-choice">
  <input type="checkbox" name="free-only">Free events only
</label>
<fieldset class="tide-fieldset">
  <legend class="tide-fieldset__legend">When</legend>
  <div class="tide-chip-list">
    <label class="tide-chip"><input type="radio" name="when" value="today">Today</label>
    <label class="tide-chip"><input type="radio" name="when" value="weekend" checked>This weekend</label>
  </div>
</fieldset>
```

Checked appearance follows the native input using `:has(input:checked)`. Radio-group keyboard behavior is supplied by the browser. The chip is a label, not a div with simulated button semantics.

```html
<span class="tide-badge tide-badge--warning">Pending review</span>
<div class="tide-notice">
  <strong>We couldn’t save that change.</strong>
  <p>Your event details are still here. Try again when your connection returns.</p>
</div>
```

Static callouts do not all need `role="alert"`. If an application inserts urgent errors dynamically, choose the appropriate live-region behavior and avoid duplicate announcements. The toast specimen is not presented as a complete live toast system.

## Event-card details

Use a unique heading ID and `aria-labelledby` on each article. The stretched link is a sibling of the card content and must have a meaningful label. Any future save button goes above the link using the `tide-event-card__save` layer, has its own 44px target, and must not be nested inside the anchor. Current bookmark marks are explicitly static/decorative where the source treats them as visual examples.

## Semantic heading levels (reviewed copy 1.0.1)

Use `.tide-event-hero__title`, `.tide-event-details__title`, `.tide-event-details__section-title` and `.tide-page-intro__title` on headings independently of their HTML level. An event title can be H1 on a standalone page or H2 in a browse preview. Typography is unchanged. Legacy level-specific selectors remain compatibility aliases. Choose one primary H1 per document and avoid skipped levels within each content outline.

The prominent date is a `time` with a valid datetime value and a full accessible date label; visible day/month fragments are hidden from assistive technology to avoid repetition. Time, venue and price are real text. Unknown information should not be fabricated to fill a layout.

## States not yet implemented

The kit does not claim production behavior for asynchronous loading, live save/unsave, toasts, file-size validation, search/filter logic, booking, sharing, dialogs, menus, authentication or organizer editing. The Coverage section retains those product decisions. Add a behavior contract and keyboard/announcement tests when implementing them.

All eleven existing screen/state compositions are included in every named theme and both modes. The selected list and the full-screen event are available directly; the library also shows search, filters, saved, empty, submission, review, confirmation and recovery patterns.
