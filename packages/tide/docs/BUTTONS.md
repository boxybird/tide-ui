# Buttons · Tide 1.6.0

Tide 1.12.0 adds an opt-in [navigation modifier](NAVIGATION.md). It reuses compact quiet/secondary geometry and action states while mapping aria-current to location emphasis. Existing defaults and toggle semantics are unchanged.

The kit owns action geometry, typography, native semantics and visual states. A consuming page owns placement, routing and actual state changes. No browser JavaScript is shipped or required by these specimens.

CSS: `css/components.css`. Named inputs: `css/tokens.css`. Canonical HTML: `templates/buttons.html`, rendered in the library and `frames/button-states.html` in all ten theme/mode combinations. The registry declares the CSS/HTML/contract owners for Button, Icon button and Photo control. Documentation layout stays in `site/css/docs.css`.

## Geometry and typography

| Size | Minimum height | Text | Padding, block / inline | Border | Glyph |
| --- | --- | --- | --- | --- | --- |
| Regular | 48px | Manrope 14px / 22px, weight 550 | 12px / 20px | 1px reserved | 18px |
| Explicit compact | 44px | Same type | 10px / 16px | 1px reserved | 18px |
| Icon only | 48px regular; 44px compact | Accessible name required | Centered glyph, zero padding | 1px reserved | 18px |

These are rem-based defaults. Buttons have a minimum height; longer labels may wrap and grow vertically. Square icon controls have a fixed target. The existing 2px control radius remains. User zoom and root-font preferences scale the inputs together.

Primary, secondary and quiet are emphasis choices. They keep the same geometry for a given size, including the transparent border reservation. A quiet button is no longer a shorter-padded text action. Use a native text link for inline reading/navigation when button geometry is inappropriate.

There is no breakpoint-dependent button density. Choose `--compact` explicitly; the surrounding composition wraps or stacks actions at narrow widths. The component declares its own font size, family, style, weight, line height, tracking and text case, so reading/header or emphasized uppercase contexts cannot alter a regular button accidentally.

## Independent options

```html
<button class="tide-button" type="submit">Apply choices</button>
<button class="tide-button tide-button--secondary" type="reset">Reset</button>
<button class="tide-button tide-button--quiet" type="button">Cancel</button>
<button class="tide-button tide-button--compact" type="button">Compact action</button>

<a class="tide-button tide-button--full tide-button--spread" href="event.html">
  <span>View event</span>
  <svg class="tide-icon" aria-hidden="true" focusable="false" viewBox="0 0 15 15">…</svg>
</a>
```

`--full` selects width. `--spread` puts the label and trailing icon at opposite ends and aligns wrapping labels to the start; it does not change padding or type. Use real source icons. Document-level heading/reading styles must not redefine button internals. Component inputs alias the named type and spacing tokens; themes continue to change colors only.

The old `--plan` class remains a compatibility alias for spread layout with regular geometry and retains its historical block display. Within Event hero, its action gap is supplied by the event composition. New canonical event markup uses `tide-event-hero__action` for that gap alongside `--full --spread`. No application template/layout migration is needed for this release.

## Icon and photo controls

Use `tide-button tide-button--icon` for a regular icon action and add `tide-button--compact` for 44px. Combine the ordinary emphasis modifiers as needed. Label every interactive icon with meaningful text or `aria-label`; the SVG remains decorative.

Legacy `tide-icon-button` and `tide-photo-control` keep their 44px footprint for compatibility. Their `--regular` modifiers explicitly select 48px. All action families use the same 18px glyph. Photo control retains its dark photographic reading treatment; a decorative save-preview span is not made interactive by its appearance.

The native file-selector button belongs to Upload's field recipe. Kit 1.7.0 aligns it with compact action geometry and 14px/22px weight-550 typography. See [form controls](FORMS.md) for its native selection, reset and reviewed-error contract.

`tide-icon-button--selected` remains a compatibility appearance for authored examples; real toggle semantics use `aria-pressed`. The display-only `--focus-sample` alias is deprecated but retained for compatibility. New specimens exercise actual keyboard focus instead of drawing a permanent demonstration ring.

## State contract

| State | Presentation and behavior |
| --- | --- |
| Rest | The chosen emphasis and size. Native link/button semantics remain intact. |
| Hover | Primary uses the audited accent-hover role. Secondary, quiet and icon actions use a raised surface. Photo controls use the opaque photo canvas. Only enabled native buttons and links with href receive hover styling. |
| Active, while held | Primary uses a separate audited accent-active role. Secondary, quiet and icons use the selected surface/text pair; photo actions use the photo accent. No movement or geometry change. |
| Keyboard focus | Shared 2px outline with a 3px offset. Photo controls use photographic foreground contrast. Focus is independent of hover and selection. |
| Pressed / selected | `aria-pressed="true"` uses the selected surface, text and border. Hover adds a 1px inset keyline; active adds a 2px inset keyline without changing the outer border or layout. |
| Disabled | Native `disabled` prevents activation and skips Tab. Muted foreground/background takes precedence over selected/hover/active styling. Photo controls retain their reading context. |
| Forced colors | Reserved system-colored borders, an equivalent selected fallback for all three families, and GrayText for disabled controls. Actual engine/assistive-technology coverage is recorded separately. |

Pressed examples in the canonical matrix are fixed, labelled visual states. CSS does not toggle `aria-pressed`; the consumer supplies actual state changes or renders the current state. The kit does not implement saving, persistence, dialogs or business actions.

A navigation action is an anchor with a real href. CSS cannot disable a live link: if navigation is unavailable, omit href and expose an appropriate disabled semantic, or omit the action. `[aria-disabled="true"]` supplies appearance only. Do not use pointer-events as a substitute for native/semantic behavior.

## Checks and browser evidence

Run root `npm run build` and `npm run check`. Portable regression guards reject viewport-, emphasis- and reading-context geometry overrides, missing explicit type, unregistered action ownership, missing authored state combinations, and inaccessible/identical hover-active color roles. The existing ownership check now covers the Photo control supporting block as well as Button and Icon button.

The development-only read-only function in `tools/button-browser-probe.js` can be evaluated through Browser Use on each generated `button-states.html`. It measures actual geometry, inherited context equality, regular/compact target sizes, glyphs and disabled-state precedence. It is never served as browser code. The root check needs no new dependencies; source checks do not substitute for these rendered measurements.

See [normalization verification](BUTTON-VERIFICATION.md) for actual browser coverage and remaining limits. This pass changes kit action presentation and documentation only; application layout/template sources stay untouched.
