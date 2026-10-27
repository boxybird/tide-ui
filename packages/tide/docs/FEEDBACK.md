# Feedback components · Tide 1.8.0

The kit owns typography, spacing, colors and native link states for badges, notices, toast specimens and empty states. The consumer renders the actual status/result and owns any insertion, live announcements, focus, queue, timeout or dismissal behavior. The kit and its specimens ship no browser JavaScript.

CSS: `css/components.css`. Canonical HTML: `templates/feedback.html`, rendered as the full `frames/feedback-states.html` matrix in all ten theme/mode combinations. The main library extracts seven overview cases from that same HTML and links to the complete matrix, keeping its existing document budget. There are no copied preview recipes. Registry entries declare CSS/HTML, state, behavior and contract ownership. Documentation presentation/context tests live in `site/css/docs.css`. The check/bookmark glyphs reuse the maintained Radix SVGs, with the existing MIT license in `licenses/radix-icons-MIT.txt`.

## Type and spacing

| Element | Typography at the default root | Geometry |
| --- | --- | --- |
| Badge | Manrope 12px / 20px, weight 550 | 24px minimum height; 1px / 8px padding; 8px gap; optional 16px glyph |
| Notice title | 14px / 24px, weight 550 | 16px on every edge; 8px gap between title, body and actions |
| Notice body | 14px / 24px, weight 400 | Same shell; multiple body paragraphs use an 8px gap |
| Toast message | 14px / 24px, weight 400 | 16px on every edge; 16px message/action gap; 78px minimum shell reserves a 44px action row |
| Feedback action link | 14px / 24px, weight 550 | 44px minimum target height; underline; action rows wrap with 8px row / 16px column gaps |
| Empty-state title | 24px / 32px, weight 580 | Regular 48px / 24px padding; explicit compact 24px / 16px; 16px content gap |
| Empty-state body | 14px / 24px, weight 400 | Reading measure up to 65ch; optional 28px decorative glyph |

All values use named rem inputs, the reserved 1px border and existing 2px control radius where a border exists. Labels, text and actions wrap and grow rather than truncate useful status/error text. Badge padding is calculated from its named height/leading/border inputs. Badge dimensions are not interactive targets. Notice/toast shells remain neutral; empty states remain unframed.

Font family, style, size, weight, leading, tracking and case are explicit on each block. A surrounding reading header, large italic serif style or uppercase label cannot change feedback typography. Empty-state titles use the existing title tracking; other feedback tracking is normal. Real inline emphasis can still use `strong` or `em`. Semantic heading level and component type are independent.

## Badge

Use ordinary status text, usually a `span.tide-badge`. Neutral, `--success`, `--warning` and `--danger` use the same geometry. The status roles change only foreground, background and border color; visible words carry the meaning. Optional icons are decorative and do not replace those words. A neutral badge has no filled selected/toggle appearance.

Badges have no hover, active, pressed, focus or disabled interaction. Do not make a badge a button, removable filter chip or live region just to match its appearance. If an action is needed, use the Button, Chip or native link recipe. Hidden badges follow the native `hidden` attribute.

## Notice

```html
<section class="tide-notice tide-notice--error" aria-labelledby="change-title">
  <h2 class="tide-notice__title" id="change-title">We couldn’t save that change</h2>
  <div class="tide-notice__body"><p>Your entered details are still here.</p></div>
  <div class="tide-notice__actions">
    <a class="tide-notice__action" href="review.html">Review details</a>
  </div>
</section>
```

Use a heading and labelled section when the message deserves its own region. A short ordinary message can be a `div` with a direct `strong` title and `p` body; that legacy markup remains supported. Body wrappers contain paragraphs, so inline emphasis keeps its ordinary inline layout. `--error` and `--success` remain compatible content labels with the same shell as information, warnings and recovery messages. They do not introduce a colored stripe or status border. State must be explicit in the words.

The former extra left inset is removed: every edge has 16px padding. Keep values, hints and useful context when reporting errors. Compose `tide-error-summary` with Notice for a linked field review; its explicit title/list contract remains intact. See [form controls](FORMS.md). Static messages do not need automatic focus or an alert role. Only a consumer with a real dynamic update should choose a live-region strategy and verify announcements.

## Toast specimen

```html
<div class="tide-toast">
  <span class="tide-toast__message">Saved-page example is ready.</span>
  <a class="tide-toast__action" href="saved.html">View saved examples</a>
</div>
```

`__message`, optional `__actions` and `__action` provide explicit slots. A legacy direct `span` and bare `a` remain supported. A Button may be composed instead; toast link styling excludes Button anchors and does not change their geometry or hover state. Multiple messages or long actions wrap within the shell. Message-only feedback keeps the same minimum shell size as a short message with an action; long content can increase height.

The action is a real navigation link. Hover uses audited `accent-hover` and a thicker underline; held active returns to audited `accent` with a double underline; focus uses the shared 2px outline / 3px gap. No state changes typography or padding. An unavailable action omits href, exposes `aria-disabled="true"`, uses muted text and has no hover/active treatment. System GrayText is provided in forced colors. CSS cannot disable a live href.

The same action-link recipe is available as `tide-notice__action` and `tide-empty__action`. Normal inline prose links need not be turned into 44px action rows. Buttons continue to use [their own size/emphasis contract](BUTTONS.md).

These are static feedback specimens. There is no toast manager, save operation, queue, auto-dismiss timer or automatic announcement. No inert close button is drawn. If a consumer needs changing feedback, it owns the actual update, appropriate announcement, focus preservation, dismissal and enough time to read/use any action. Keep consequential recovery information available in a persistent Notice as appropriate. The static kit does not claim those interactions are implemented.

## Empty state

Use `tide-empty__title`, `__body`, `__actions` and `__action` with document-appropriate headings. Legacy `h2`/`p` markup retains the same type. The base uses regular spacing at every viewport; choose `tide-empty tide-empty--compact` explicitly for an inline specimen. Neither a small screen nor an enclosing heading silently changes its density. Icons and actions share the same 16px flow gap; there are no extra hidden icon/action margins.

Explain the actual reason for absence. First use can invite browsing. No matches can offer changed criteria. A venue with no listed schedule still has useful location/access information. An unavailable listing is different from a successful search with zero matches; a load failure needs recovery wording rather than an empty-data claim. Completion messages may reuse the layout for compatibility, but they are not evidence of an operational submission service. The matrix links to authored UI examples; it does not perform filtering or saving.

## Checks and evidence

Run root `npm run build` and `npm run check`. Portable regression guards cover type/context isolation, status geometry, neutral Notice boundaries, explicit empty density, native action semantics, hidden states, Button composition, registered ownership and shared all-theme rendering. The existing 600 contrast pairs cover status labels on their surfaces and feedback text/actions on neutral surfaces. Theme inputs and resolved palettes are unchanged.

The development-only read-only `tools/feedback-browser-probe.js` measures type, padding, gaps, wrapping, hidden states, targets and context equality in the generated matrix. It is never served. [Feedback verification](FEEDBACK-VERIFICATION.md) records actual rendering/keyboard coverage and remaining limits.

To stay inside the existing distribution budgets, the compiler omits ordinary source comments from the generated combined CSS. Strings, URLs, rules, declaration values, layer order and license/preserve comments remain intact. Canonical source comments remain readable in the repository. This is not value minification; portable parity checks cover the transformation. See the [loading contract](../../../docs/LOADING-PERFORMANCE.md).
