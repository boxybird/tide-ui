# Public block ownership · Tide 1.12.0

The registry covers 26 components, 26 supporting blocks and 13 compositions. Every entry requires a canonical CSS source, HTML recipe, rendered fixture, behavior description, contract and explicit kit style ownership. Composition names require matching composition contracts. Missing fields, duplicate owners, invalid source paths, absent fixtures and fixtures omitting their registered block fail the normal check.

The registry is an index into maintained recipes, not a second implementation. Extension Panel is owned by `extensions/panel.css` and loaded explicitly; it does not silently enter the core distribution. Theme copies are generated. All named theme/modes share markup. See [normalization status](NORMALIZATION-STATUS.md) and the all-theme `frames/kit-closeout.html` specimen.

## Supporting blocks

| Blocks | Contract and behavior |
| --- | --- |
| Brand, Saved link, Back link | Native navigation with an authored name and destination. Brand retains named optical wordmark proportions; Saved and Back have explicit caption/small type and 44px minimum targets. |
| Caption, Eyebrow | Explicit Manrope type: caption 12px/20px regular; eyebrow 11px/16px medium with tracked uppercase. Card categories and sponsorship have their separately documented 12px/20px role. These labels do not implement interaction. |
| Icon | Decorative dimensions only; author `aria-hidden` on decorative SVGs and name the enclosing native control. An icon's dimensions do not define its hit target. The existing compact navigation glyph is an explicit consumer exception. |
| Inclusions, Schedule, Place, Disclosure | Semantic event-detail content. Schedule pairs labels/descriptions; unknown times remain text. Place labels are authored. `tide-disclosure` is small disclosure copy, separate from interactive `tide-expandable`. |
| Fieldset, Chip list, Search line | Native grouping and layout around the existing [form controls](FORMS.md). Fieldset needs a legend; radio name/value and label associations remain native. The consumer may compose the documented fieldset grid. |
| Event list, List, State | Static card stack, list-page scaffold and adjacent state separators. Native scrolling and semantic child content; no filtering, live counts or state controller. |
| Frame | Generated specimen-document wrapper. Hides that specimen's scrollbar without replacing native scrolling. The site builder supplies the wrapper around the named recipe. |
| Skip link, Screen-reader-only text | Native fragment link with a focusable main destination; visually hidden text remains available to accessibility APIs. Neither helper supplies an accessible name automatically. |
| `tide-u-start`, `tide-u-muted`, `tide-u-mb-8`, `tide-u-mt-7`, `tide-u-mt-8` | Explicit alignment, color and external spacing utilities. They inherit reading typography by design and add no semantics or behavior. |
| Photo control | [Button contract](BUTTONS.md#icon-and-photo-controls). Native photographic action; consumers own any state changes. |

## Compositions

Screen, Stack, Row and Split are layout helpers. They intentionally inherit reading typography and do not turn semantic children into widgets. Appbar, Page intro/body, Screen footer and Summary declare default Manrope body type; their title/label roles are explicit. Form section/actions and Search line compose existing controls. Content page and Results retain their [content](CONTENT.md) and [listing](LISTINGS.md) contracts. Consumers author heading levels, IDs, routes and truthful content. Use private consumer blocks for viewport geometry.

Generic layout helpers must not reset a nested component's type, padding or states. Standalone venue profiles retain 24px insets. A profile inside an already padded page opts into `tide-venue-profile--flush-inline`; it removes only inline padding, retaining block padding and section rhythm. See [page recipes](PAGE-PATTERNS.md#venues).

The [Results utility variant](RESULTS-UTILITY.md) is a kit-owned additive recipe. Consumers opt in through markup; no private count/type/divider overrides are authorized.

The [optional navigation recipe](NAVIGATION.md) owns the centered header slots and navigation current-page modifier. It reuses existing action internals and is loaded explicitly.

## Consumer exceptions

`consumerStyleExceptions` lists target selectors, exact property/value choices and reasons. The ownership check examines each selector in a grouped rule, including selector functions, so one permitted target cannot conceal another target or an extra declaration. A negative reference such as `p:not(.tide-eyebrow)` does not restyle Eyebrow. These focused checks are not a general CSS parser.

Existing accepted exceptions cover card preview visibility/outline; safe-area/viewport/print placement and crop protection for the event opening; detail reading measure/fragment clearance; the compact navigation glyph; fieldset grid; native compact filter-footer links; and external form-caption spacing. Their exact values live in the registry. They do not authorize arbitrary font, padding or color overrides. New consumer needs require a documented variant/input or a reviewed exception. The app keeps its current CSS; no private layout is promoted into the kit.
