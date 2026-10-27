# Form controls · Tide 1.7.1

The kit owns control geometry, typography and visual states. Native HTML owns typing, selection, disclosure toggling, required validation and form reset. A consumer renders reviewed errors and owns any application validation, summary focus or announcements. These specimens ship no browser JavaScript.

CSS lives in `css/components.css` (fields, choices, chips and upload), `css/patterns.css` (disclosures), and `css/page-patterns.css` (error summary). `templates/controls.html` is the shared source for the component library and `frames/form-states.html` in every theme/mode. Registry entries declare those owners and the contract. Documentation layout/context tests live only in `site/css/docs.css`.

## Geometry and typography

| Element | Default geometry | Manrope typography |
| --- | --- | --- |
| Single-line input/select/date/time | 48px height; 11px block / 16px inline padding; 1px border | 16px / 24px, weight 400 |
| Textarea | 120px minimum height; same padding/border; vertical resize | Same field values |
| Field label | 8px field stack gap | 14px / 20px, weight 500 |
| Hint or error | Same stack; both may remain visible | 12px / 20px, weight 400 |
| Fieldset legend | 12px gap below legend | 16px / 24px, weight 550 |
| Checkbox/radio choice label | 44px minimum target; 12px gap; 18px native input | 14px / 24px, weight 400 |
| Chip | 44px minimum height; 10px / 16px padding; 8px gap; 18px input | 14px / 22px, weight 550 |
| Disclosure summary | 48px regular height; 11px / 16px padding; 18px chevron | 14px / 24px, weight 550 |
| Native file-selector button | Same compact geometry; 12px filename gap | 14px / 22px, weight 550 |
| Upload shell | 16px padding; 12px gap; 1px dashed border | Filename 14px / 22px, weight 400 |

All dimensions use named rem inputs and the existing 2px control radius. These are defaults at a 16px root, not fixed physical pixels at zoom. Choices, chips and summaries grow when labels wrap. Fields and disclosure summaries share regular geometry and a 24px line box. Chips and the file selector share compact action aliases. No viewport or surrounding heading changes control density. Family, style, size, weight, leading, tracking and case are explicit, including labels and helper text.

## Select and disclosure alignment

Both controls remain native HTML. A select chooses a value using its browser menu; `details`/`summary` reveals content. Kit 1.7.1 replaces only the collapsed single-select chrome with the same distributed chevron used by disclosures. It adds no menu, simulated roles, browser JavaScript or application layout.

`--tide-control-inset-inline` sets the shared 16px inset. `--tide-control-chevron` references the source SVG; both controls center its 18px box. Selects reserve 46px on the trailing side: 16px inset + 18px glyph + 12px text gap. This reservation is space for the icon, not extra label padding. The field grid places its decorative, pointer-transparent pseudo-element over row two, so keep the labelled select directly inside `tide-field`. Existing canonical markup already follows this recipe. The reserved border is accounted for in the marker inset. Logical properties mirror the chevron and text reservation in right-to-left layouts.

Only collapsed single-selects (omitted `size` or `size="1"`, without `multiple`) receive the kit arrow. Native list boxes retain their appearance, intrinsic height and no dropdown indicator. Disabled chevrons use muted text; system colors are provided for forced-colors mode. The native popup, option selection, type-ahead, keyboard, required and disabled semantics remain with the browser. Its open menu can still differ between platforms. Explicit CSS leading remains recorded separately from any native select line-height reported by an engine.

## Fields and reviewed errors

```html
<div class="tide-field">
  <label class="tide-field__label" for="email">Contact email</label>
  <input class="tide-field__control" type="email" id="email" value="hello@"
    aria-invalid="true" aria-describedby="email-hint email-error">
  <small class="tide-field__hint" id="email-hint">Used for event questions.</small>
  <small class="tide-field__error" id="email-error">Enter a complete email address.</small>
</div>
```

Enabled editable fields strengthen their border on hover and use the accent while active. Invalid fields keep their danger border through those transient states. Read-only controls remain focusable/selectable and use the surface background. Disabled controls use muted text/raised background and the neutral border, including when an earlier reviewed error remains in the markup. No state changes padding, border thickness or size. Shared keyboard focus remains a 2px outline separated by a 3px gap.

Do not set `aria-invalid` on untouched required controls. `:user-invalid` adds the danger boundary after native interaction, according to the browser's timing; unsupported engines retain native constraint-validation messages and explicit authored `aria-invalid` styling. Avoid `:invalid` styling that paints empty required controls immediately. Error words and a useful correction accompany authored invalid states, linked through `aria-describedby`; color alone is insufficient. Native browser messages and authored error summaries are separate demonstrations.

Reset restores native values, checked defaults, file selection and interaction-based validation state. It does not clear authored `aria-invalid`, error text or a summary. A consumer must render those consistently with its actual reviewed state. The static matrix explicitly labels that limitation.

## Choices and chips

Keep visible native checkbox/radio inputs inside labels, with a fieldset/legend for a related group. Radio arrows, Space, checked state, required constraints and disabled semantics come from the browser. Label targets remain at least 44px. Checked ordinary choices use primary text; native inputs retain their accent and platform feedback. Hover strengthens unselected choice text. Native focus stays on the input.

Chips use the compact action rhythm. Hover uses the raised surface; held active and checked states use the audited selected text/surface/border pair. Checked hover and active use 1px and 2px inset feedback without changing geometry. Invalid checked chips use the field/danger pairing while the native check still conveys selection. Disabled styling wins over checked, invalid, hover and active, including inputs disabled by a parent fieldset. A prior error can remain readable below the unavailable control.

`tide-chip--selected` remains an authored appearance for compatibility. It does not set native state. Use native checked inputs for choices, a real href for navigation, and appropriate current-page semantics only for the actual current destination. An unavailable anchor omits href and can expose `aria-disabled="true"`; CSS cannot disable a live link. Do not put interactive descendants inside an interactive chip.

## Disclosures

Use `details.tide-expandable` and its first `summary.tide-expandable__summary`, followed by `tide-expandable__body`. The summary is keyboard focusable; Enter/Space toggles its native open state and Tab reaches revealed controls. Do not duplicate the browser's role or add manually synchronized `aria-expanded`.

Every summary has an indicator. When `tide-expandable__icon` is present, that decorative source SVG rotates on open. Otherwise a CSS mask uses the shared `--tide-control-chevron` asset. The fallback disappears when an explicit icon is supplied, so there is one chevron. Both are 18px and reserve their space. The summary uses regular field geometry; hover/active retain the audited neutral/selected roles. Details has no native disabled state: omit an unavailable disclosure or present static information; `aria-disabled` alone would not prevent toggling.

## Upload and error summary

Keep a visible file label, native file input, filename and linked guidance in `tide-upload`. `accept` is a chooser hint; the kit does not inspect files, enforce size/content limits, upload, generate previews or implement removal. A native Reset button in the same form clears the selection. The selector uses the compact button typography/geometry and enabled hover/active feedback. The input keeps real keyboard focus.

An authored `aria-invalid` or native `:user-invalid` switches the shell to a solid danger border, matching text fields while reserving the same 1px. Disabled shells and selector buttons remain neutral and muted even with an earlier error. The all-theme matrix includes normal, required, reviewed invalid, disabled and invalid-plus-disabled examples. File-content validation and the rendered error message belong to the consumer.

Compose `tide-error-summary` with the neutral `tide-notice` boundary, a heading with `tide-error-summary__title`, and an ordinary linked `tide-error-summary__list`. Each error link targets its actual control ID. Keep values, labels, hints and inline errors available. `tabindex="-1"` permits deliberate consumer focus; the static kit does not move focus, compute/clear messages or announce an alert. Do not add an alert role to every pre-rendered summary. Native fragment links and focus are exercised in the matrix; dynamic announcements need separate consumer and assistive-technology testing.

## Verification

Run root `npm run build` and `npm run check`. Portable contracts check explicit type/geometry ownership, state precedence selectors, disabled-fieldset coverage, native markup, unique labels/IDs, hint/error associations, valid summary destinations, shared all-theme rendering and the zero-script boundary. Existing contrast gates cover the selected pairing and danger text against field/canvas/surface/raised backgrounds without changing the palette.

The development-only read-only `tools/form-browser-probe.js` measures the rendered matrix, context isolation, disabled precedence, indicator count and overflow. It is never served. [Form verification](FORM-VERIFICATION.md) records actual browser coverage and limits. Application CSS/templates and their layout ownership are untouched; consumers receive updated kit presentation through the shared stylesheet.
