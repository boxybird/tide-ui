# Native mobile navigation · Lineup 2.2.1

Below 34rem, Menu replaces the inline primary presentation. Brand and Saved stay on the first header row; Menu and the original Filters button occupy the second. Tablet and desktop retain the accepted inline header. The breakpoint is content-based: the full three-link row plus Filters needs about 526 CSS pixels with the existing insets and gutter; 34rem supplies a small allowance at the default root size.

## Native behavior and composition

The Menu button uses `popovertarget="lineup-menu"`. Its target is an ordinary `nav` with `popover="auto"`, not an ARIA menu widget. Tab follows real links. The button toggles the popover; Escape and outside clicks dismiss it, and native keyboard dismissal restores invoker focus. Opening the separate Filters auto popover dismisses Menu. No focus trap, controller, script, storage or custom history is added.

`navigation-items.html` authors Find Events, Venues and Add an Event once. It renders inside the inline list and the mobile popup list; CSS removes inactive presentations from layout and accessibility. Closed mobile navigation remains a Menu button, and only one Main navigation is exposed when open or inline. Both renditions carry exact current-page states. The original filter form/control set is not duplicated.

Private wrapper classes own mounting and spacing between controls. A private `:has(> :popover-open)` host mounts the unchanged Panel only while open. This keeps its canonical grid, padding, border, surface, radius and type intact. CSS anchor functions place it below the button with a named 8px gap. The native centered placement remains the fallback when anchor functions are unsupported. Popup dimensions are viewport-bounded and its contents can scroll; background scrolling is restrained only while the phone menu is open.

At or above 34rem the mobile wrappers are hidden and inline navigation is exposed. An open popover's native state is retained across resizing; it can reappear when returning to phone width unless dismissed. The hidden wide-screen popup is neither rendered nor exposed as another navigation. The browser owns this state; no static `aria-expanded` value tries to replace it.

The responsive switch is gated by `@supports selector(:popover-open)`. Without that support, the original inline links remain available. Menu adds no animation; the filter drawer retains its own reduced-motion behavior. Native event documents keep their existing phone header omission.

## Dependencies and ownership

Tide 1.12.0 is unchanged. Button/navigation/Icon recipes supply the trigger and links. The existing `packages/tide/extensions/panel.css` supplies the popup surface. The application builder emits it byte-for-byte as `events/runtime/css/tide-panel.css`; this is generated dependency output, not a maintained fork. `KIT_PANEL_CSS` resolves its path for every mode. The five application style modules still own only private composition.

Template consumers adopt the registered link-item partial, `HEADER_MENU_ICON` and `KIT_PANEL_CSS`. Consumer adapters should distinguish the active presentation instead of assuming every header anchor has a single DOM copy. Existing routes, current-page semantics, field names and the separate external consumer experiment remain unchanged.

## Verification and limits

In-app Chromium on Windows, 2026-10-28:

- All ten theme/mode pairs at 390×900 expose Menu when closed and exactly one Main navigation when open. Popup links retain canonical 44px targets and Panel's 24px padding. There is no horizontal document overflow or browser script.
- Twenty 1440×900 comparisons cover index and Venues in every theme/mode. Header, inline navigation and Saved rectangles match the 2.2.0 baseline exactly.
- The popup fits at 320×500. Checks immediately below/at the 34rem boundary (543/544 CSS pixels at the default root size) expose only the appropriate navigation. Tablet at 768×900 retains inline links and its original Filters behavior.
- Tab enters the ordinary links; Escape closes Menu and returns focus to its button. Outside clicks dismiss it. Opening Filters dismisses Menu. Native journeys reach Venues, Add an Event, Saved and Find Events with document-accurate current states. An open Menu remains hidden when resized to 768/1440 and can be toggled after returning to 390.
- Console warnings/errors: none recorded. `npm run build` and `npm run check` pass, including 124 tests (7 HTTP, 72 Tide and 45 application), strict style ownership and zero-browser-JavaScript checks. Tide, reference-site and shared-tooling sources remain unchanged; the four filter-panel source files retain their 2.1.9 bytes.

Measurements and screenshots remain ignored under `build/qa/lineup-mobile-menu/`. Firefox/Safari, physical devices, screen readers, actual text zoom, changed system preferences and unsupported-popover/anchor fallbacks have not been exercised. The CSS fallbacks are implementation paths, not cross-browser verification claims.
