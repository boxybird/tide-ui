# UI page coverage · 2026-10-26

Tide 1.5.0 and events example 1.1.6 add the five agreed areas: venue composition, form validation, event conditions, website navigation and control states. Theme work in 1.4.0 remains intact. These are kit and local example deliverables.

## Sources and ownership

- Four registered reusable blocks: Venue profile, Venue card, Site header and Form error summary. Composition styles live in `packages/tide/css/page-patterns.css`; additive states remain with the existing controls in `css/components.css`.
- Seven shared HTML specimens render in Tide, Bumble, Slate, Grove and Iris, each in light and dark. The reference site's Screens section links every recipe.
- The events example consumes shared venue padding and header/section rhythm; the three duplicated app rules were removed. Private viewport geometry, fragment clearance and all nine runtime scripts remain owned by the example.
- Form, toggle and file demonstrations live in the reference site. The generated CSS distribution contains no JavaScript. Native controls remain available without the demonstrations.

## Checks and observed behavior

`npm run build` and `npm run check` passed: 904 generated HTML documents, local references/associations, registry/ownership, theme parity and contrast gates; 16 kit tests, 24 app template tests, 16 search assertions, 18 runtime contracts and the registered documentation script's syntax check.

Installed Chrome (Chromium on Windows), using local generated files:

| Coverage | Result |
| --- | --- |
| All seven recipes in all ten theme/modes | 70 page variants checked; no browser script errors. |
| 320px, 390px and 1440px widths; 390px at 200% root text size | 280 layout observations; no horizontal document overflow. Root text enlargement is not a claim of browser zoom testing. |
| Invalid form | No untouched invalid state; two errors on submit, containing disclosure revealed, summary focused, error link focuses its field. |
| Form correction/reset | Modified title retained, hints retained alongside errors, invalid semantics cleared after correction, success status shown and initial values restored by reset. |
| Native fallback | Required-date validation and accessible expanded contact fields remain when JavaScript is disabled. |
| Control states | Native read-only/disabled semantics, radio keyboard selection, pressed toggle semantics and matching selected paint, including while hovered. |
| File selection | Actual local selection/replacement, unsupported type and oversized-file rejection, error association/treatment, removal and focus returned to chooser. |
| Navigation | Skip link focuses main; one accurate current-page link; long labels wrap without a menu script. |

The browser pass exercised 292 interaction assertions. Reviewed phone captures cover venue, form error, navigation, event-condition and control-state specimens. Routine screenshots and detailed local reports remain ignored under `.cache/ui-coverage/`.

All 60 rendered app routes were compared with a pre-change snapshot. They match exactly after normalizing only the two adopted venue classes. The existing venue profile retains 24px padding and 12px header spacing. Venue facts, sample data, native IDs/URLs, theme inputs and runtime sources are unchanged.

## Limits

The browser evidence is Chromium on Windows. Firefox, Safari, physical devices, browser zoom and screen-reader announcement checks remain deferred. Structural associations and focus observations do not establish assistive-technology behavior. File feedback checks browser-provided MIME/size metadata only; it does not validate image contents or upload files.
