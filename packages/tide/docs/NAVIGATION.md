# Optional navigation · Tide 1.12.0

Load `css/tide.css`, then `extensions/navigation.css` to consume the reviewed centered navigation. The extension joins the existing `tide.components` layer so its explicit modifiers can supply action inputs after the default Button recipe. It is not bundled into the core entry point. Existing header, link and button defaults are unchanged.

Canonical HTML: `templates/navigation.html`. The all-theme `frames/navigation-review.html` sheet retains the default header alongside the centered recipe and native state comparisons. Site header and Button register the extension as a supporting source. No palette, primitive, asset or existing component CSS module is replaced.

## Composition

Use `tide-site-header tide-site-header--centered` with a `__leading` group, `__primary` navigation and `__utility` navigation. The primary list adds `tide-site-header__links--actions` to `__links`. Equal available side tracks center the primary group; minimum content sizes protect the side groups. Below 44rem the primary navigation moves to a second row. Leading/utility groups and the link list wrap naturally. Header height can grow; the consumer owns viewport placement and pane allowances.

Primary destinations use `tide-button tide-button--quiet tide-button--compact tide-button--navigation`. Utilities can use secondary emphasis with the same compact geometry. An optional native leading action, such as Filters, keeps its original semantics. Consumers supply labels, routes and document-accurate aria-current. Destinations remain real anchors; they do not receive menu roles or toggle semantics.

## Appearance and states

Navigation adds no font, padding, radius or target-size declaration. It reuses the 44px compact minimum, 10px/16px padding, Manrope 14px/22px weight 550, reserved 1px border and 2px radius. Bookmark uses the supplied 18px icon. Shared focus remains a 2px outline with a nominal 3px offset.

`tide-button--navigation[aria-current="page"]` maps the existing selected surface/text pair to location emphasis. A quiet link's reserved border stays transparent at rest; a secondary utility retains its neutral border. Current hover/held feedback uses the reviewed 1px/2px inset keyline without geometry movement. Other links inherit existing action states. Disabled appearance wins; unavailable anchors omit href. Current page never uses aria-pressed.

The system-color fallback uses Highlight/HighlightText without replacing focus. No animation, JavaScript, controller, history or storage is introduced. The [original review](NAVIGATION-REVIEW.md) records the acceptance checkpoint; Lineup's current header-navigation contract records integration and pane parity. Browser evidence is Chromium on Windows; other engines, physical devices and screen readers remain deferred unless explicitly recorded.
