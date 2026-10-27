# Kit closeout in 1.10.0

All public blocks now have required [ownership contracts](OWNERSHIP.md). Remaining component/page-pattern [typography and spacing](KIT-CLOSEOUT.md) have an all-theme normal/context/hidden matrix in `kit-closeout.html`. See [verification](KIT-CLOSEOUT-VERIFICATION.md) and [completion status](NORMALIZATION-STATUS.md). Application layout sources remain unchanged.

# Listings normalized in 1.9.0

Cards, dates, calendar groups and result summaries have a [listing contract](LISTINGS.md), canonical card/date recipes and all-theme `listing-states.html`. Type, spacing, visible separators and native preview/navigation states are covered by [verification](LISTING-VERIFICATION.md). Application viewport/layout ownership remains separate.

# Feedback normalized in 1.8.0

Badges, notices, toast specimens and empty states now share explicit typography and spacing/state contracts. See [feedback components](FEEDBACK.md), canonical `templates/feedback.html`, the all-theme `feedback-states.html` matrix and [verification](FEEDBACK-VERIFICATION.md). Notice borders remain neutral; native links remain native; static messages do not imply a feedback engine.

# Select/disclosure alignment in 1.7.1

Closed native selects and disclosures share a source chevron, logical 16px horizontal insets and 48px regular geometry. The all-theme form matrix includes paired, right-to-left, size-one and native listbox comparisons. See [the form contract](FORMS.md#select-and-disclosure-alignment).

# Forms normalized in 1.7.0

Fields, choices, chips, disclosures and upload/error states now declare their own typography and geometry, with disabled precedence over checked/invalid states, native validation/reset and consistent disclosure indicators. See [form contracts](FORMS.md), the shared `templates/controls.html`, all-theme `frames/form-states.html` and [verification](FORM-VERIFICATION.md). Application layout sources remain untouched.

# Buttons normalized in 1.6.0

Button, Icon button and Photo control now have an explicit [geometry, typography and state contract](BUTTONS.md), canonical `templates/buttons.html` and an all-theme `button-states.html` specimen. Primary/secondary/quiet and trailing-arrow layout share one regular geometry. Compact size is explicit; no viewport changes button padding. Existing plan/icon/photo classes remain compatible. See [verification and limits](BUTTON-VERIFICATION.md).

# Additions in 1.5.0

Venue profile and Venue card, Site header and Form error summary have shared CSS/HTML/state contracts in [page recipes](PAGE-PATTERNS.md). Seven all-theme specimens cover venue/schedule conditions, form validation, event conditions, navigation and control states. The events example consumes shared venue rhythm. Specimens use native validation/file controls and clearly authored states; the entire browser deliverable stays script-free.

# Additions in 1.3.0

Filter panel (`tide-filter-panel`) owns header/body/footer/status/count layout. Source: css/filter-panel.css. Canonical HTML: templates/filter-panel.html. Fixture: frames/filter-panel.html in all ten modes. Reuse existing Field, Choice, Button, Badge, Result summary, Field error and Empty. See [contract](SEARCH-FILTERS.md).

# Component inventory and HTML contract

The rendered component list is the library's Components section. Its source is `templates/library.html`; screen compositions live in `templates/frames/`. Every rendered theme uses the same BEM markup and CSS. `component-manifest.json` provides a machine-readable index.

## Inventory

| Component / composition | BEM block | Included states or variants | Source specimen |
| --- | --- | --- | --- |
| Venue profile / card | `tide-venue-profile`, `tide-venue-card` | Practical facts, unknown access, schedule populated/empty, native directory link | Venue, venue-empty and venues |
| Site header | `tide-site-header` | Native navigation, current page, focus, narrow and long-label wrapping | Navigation; venues |
| Form error summary | `tide-error-summary` | Authored linked errors, preserved hints/values, neutral Notice boundary; native fragments | Form states; form validation |
| Filter panel | `tide-filter-panel` | Optional header, scrolling body, pinned footer, status/count, flush rail; reused reset/submit controls | All ten filter-panel fixtures; shared shell template |
| Text action | `tide-button` | Primary, secondary, quiet, full/spread, explicit compact, icon-only, hover/active/focus, authored pressed, disabled and combined states | Button states; library |
| Icon action | `tide-icon-button` | Legacy compact, explicit regular, native focus, authored pressed, hover/active and disabled | Button states; library |
| Photo action | `tide-photo-control` | Compact/regular photographic action, authored pressed, hover/active/focus, disabled; decorative save preview | Button states; full-screen event |
| Brand and saved navigation | `tide-brand`, `tide-saved-link` | List/app-bar placements, focus | List; search |
| Text/select/textarea field | `tide-field` | Explicit type, hover/active/focus, required/native invalid, reviewed invalid, read-only, disabled precedence | Form states; submit |
| Native checkbox/radio | `tide-choice` | Unchecked, checked, keyboard, reset | Library; filters |
| Filter chip | `tide-chip` | Compact action rhythm; checked, hover/active, invalid and disabled precedence; native input or link | Form states; filters |
| Status badge | `tide-badge` | Neutral/success/warning/danger; static words, optional glyph, wrapping and hidden | Feedback states; adopted patterns |
| Callout | `tide-notice` | Explicit title/body/actions; information/recovery/success; neutral uniform edges; hidden and error-summary composition | Feedback states; states |
| Toast specimen | `tide-toast` | Message-only/native action; long content; unavailable action; hover/active/focus and hidden | Feedback states |
| Organizer | `tide-organizer` | Organizer details + contact | Library |
| Sponsored placement | `tide-partner` | Explicit sponsored label | Library |
| Event card and date | `tide-event-card`, `tide-date` | Explicit category/title/metadata and date columns; native cover/action layers, preview/status/unknown/unavailable/hidden states | Listing states; list; adopted patterns |
| Native disclosure | `tide-expandable` | Regular 48px summary, closed/open, hover/active/focus; explicit or fallback chevron | Form states; adopted patterns |
| Calendar group | `tide-event-group` | Explicit heading/count type; native jumps, sticky/static/hidden states, offset input and visible separators | Listing states; adopted patterns |
| Result summary | `tide-results` | Fixed type/insets; zero/one/many, long count/order, hidden and context states | Listing states; adopted patterns |
| Empty result/saved state | `tide-empty` | First use/no matches/empty schedule/unavailable; heading-independent title; regular/explicit compact; native recovery links | Feedback states; empty specimens |
| Missing-photo surface | `tide-fallback` | Event heading + no-photo label | Review; states |
| File field | `tide-upload` | Compact native selector, selection/replacement/reset, required/invalid, disabled precedence | Form states; submit |
| Event photo opening | `tide-event-hero` | Full viewport, photo scrim, facts and action, short viewport | Event |
| Scrolling event details | `tide-event-details` | Inclusions, schedule, practical details, disclosure | Event |
| App compositions | `tide-appbar`, `tide-page-intro`, `tide-page-body`, `tide-form-section`, `tide-summary`, `tide-results`, `tide-screen-footer` | Shared screen/state compositions | Frames |
| Spacing compositions | `tide-stack`, `tide-row`, `tide-split` | Fixed shared gaps, row wrap, narrow split gap | Across fixtures |
| Prose | `tide-prose` | Ordinary rich HTML, heading/list rhythm, link states, quotations, definitions, figures, tables, code, overflow, embedded component exclusion | `frames/prose.html`, all modes |
| Content page | `tide-content-page` | Title, metadata, optional contents rail, reading body, footer; narrow/short/wide layouts and native fragment focus | `templates/content/help.html`, `frames/help.html`, all modes |
| Additive panel example | `tide-panel` | New block consuming the existing contract | `extensions/index.html` |

## HTML examples

See [Form controls](FORMS.md) for explicit field/label typography, regular field/disclosure geometry, compact chip/file-selector geometry, invalid/disabled precedence and native behavior boundaries. `templates/controls.html` supplies both the library and `frames/form-states.html` in all ten theme/modes. The earlier submission/control specimens remain usage examples.

For ordinary rich text and informational pages, see [Prose and content-page contracts](CONTENT.md). `css/content.css` owns both additions; the application consumes the same implementation. The wrapper styles native descendants only within its scope, with an explicit exclusion for embedded components. It needs no Tailwind or editor-specific classes.

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

Event lists, result containers and single-event compositions have no decorative outer border or rounded clipping shell at any breakpoint. Keep this unframed treatment when composing desktop or tablet layouts. Card separators, selected-preview state and keyboard focus have their own component contracts; an outer panel frame is not part of the kit. App 1.3.1 removes the desktop-only framing that had been added by its composition stylesheet. Kit 1.2.1 records this clarification; shared component CSS is unchanged.

Use a unique heading ID and `aria-labelledby` on each article. The stretched link is a sibling of the card content and must have a meaningful label. Any future save button goes above the link using the `tide-event-card__save` layer, has its own 44px target, and must not be nested inside the anchor. Current bookmark marks are explicitly static/decorative where the source treats them as visual examples.

For a paired preview, add `tide-event-card--in-view` and put the existing neutral `tide-badge` in the optional `tide-event-card__status` slot. The host updates modifier/visibility together. This is not a toggle badge or selected tab. `aria-current="page"` on a link means the actual current event document, rather than merely an event previewed on the search page. See [adoption contracts](ADOPTION.md) for markup, behavior ownership and the promotion checklist.

`css/patterns.css` owns the adopted disclosure, calendar group, card preview outline and result-summary elements. `templates/adopted-patterns.html` is the shared source for their library specimens and the `app-patterns.html` frame in all ten theme/modes. A component's public class and its CSS source belong in the registry; supporting blocks and compositions are recorded there too. The app's ownership check rejects new shared blocks with no registered home.

## Semantic heading levels (reviewed copy 1.0.1)

Use `.tide-event-hero__title`, `.tide-event-details__title`, `.tide-event-details__section-title` and `.tide-page-intro__title` on headings independently of their HTML level. An event title can be H1 on a standalone page or H2 in a browse preview. Typography is unchanged. Legacy level-specific selectors remain compatibility aliases. Choose one primary H1 per document and avoid skipped levels within each content outline.

The prominent date is a `time` with a valid datetime value and a full accessible date label; visible day/month fragments are hidden from assistive technology to avoid repetition. Time, venue and price are real text. Unknown information should not be fabricated to fill a layout.

## Behavior boundaries

The kit provides HTML/CSS recipes, native controls and documented authored states. Consumers own application state changes and routing; the current example uses native/static result specimens. A visual specimen does not establish an operational service. Coverage records UI examples, not pending product decisions. Extend a component or example interaction only for a concrete UI need, with a behavior contract and relevant keyboard/announcement checks. Service implementation is outside project scope.

All screen/specimen compositions are included in every named theme and both modes. The selected list and the full-screen event are available directly; the library also shows search, filters, saved, empty, submission, review, confirmation, recovery, adopted app patterns, help and rich HTML.
