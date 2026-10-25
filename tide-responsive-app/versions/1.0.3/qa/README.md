# Verification record · 2026-10-22

**Current navigation behavior (1.0.3):** see `EVENT-SELECTION.md`. The user clarified that selecting another event from a scrolled detail page should smoothly return to the top. One optional deferred helper now sequences that motion before following the native HTML link and retains list/Back positions. Original script-free reports below describe earlier preserved versions. Seven new behavior tests and a real browser selection/Back/mobile sequence pass.

**Latest refinement:** see `VIEWPORT-FIT.md` and `viewport-fit-checks.json`. The original short-window release behavior described below has been superseded: desktop result panes now remain bounded at every tested height, leaving 24px below their closed container on arrival. The initial evidence is retained as a record of the first study.

**Smooth scrolling (1.0.2):** the document and result pane compute `scroll-behavior: smooth` under the browser's current no-reduced-motion preference. Activating “More about the music” reaches `#event-story` and focuses the destination. The initial pane still has a 24px bottom gap. Reduced-motion behavior follows the CSS guard and default `auto`; the operating-system setting was not changed for this check. User wheel/trackpad input is left native. See `smooth-scroll-check.json` and `smooth-scroll-details.png`. Source checks still pass, including the 176-file original-kit lock. [MDN behavior reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-behavior).

## Source and regression checks

- Reviewed kit: 12 unit tests passed, including palette validation and authored-name/BEM/tabindex contracts.
- 324 contrast pairs passed across Tide, Summer and Bumble in both modes.
- Reviewed kit markup check: 81 complete HTML documents, 1,270 local references, 11 screen templates and 18 registered components.
- App check: 77 generated HTML documents and 1,491 local references passed. No authored browser scripts, inline styles, undefined CSS tokens or raw palette colors in the application stylesheets.
- Original preservation: 176 file hashes verified; copied spacing/type/radius/control tokens, theme inputs and font match the original.
- `kit-geometry-check.json`: the reviewed list and event fixtures match the original at 390 × 844 for measured rectangles, type, colors and corners.

## Rendered browser checks

Chromium in the in-app browser. No native Firefox or Safari session is available here.

- `viewport-checks.json`: browse, event, search, saved and submission routes at widths 320, 834, 1024, 1440 and 1920. No horizontal document overflow; correct single/paired layout and one visible primary heading.
- Additional 390 × 844 phone checks: full-width touching cards; event hero exactly 844px tall; detail anchor navigation; hidden result list on standalone mobile event.
- `theme-checks.json`: all six theme/modes at 1440px. Identical 1120px workspace, 184px first card, 24px card title and 16px inputs. All images loaded; no horizontal overflow.
- At 320px the review gallery fits without horizontal scrolling.
- At 1024 × 600 the result pane releases sticky positioning and nested scrolling as intended.
- At 834px the form uses two columns where space allows. Date and start-time control tops both measured 894px after the field alignment refinement.
- Native keyboard Tab/Enter activated the visible phone skip link and focused `#results`. The second desktop skip link focused `#event-detail`, visible below the top edge.
- Native checkbox/radio changes and Reset filters restored their defaults. The submission sample's Reset form cleared the entered event name and category.
- Searching for printmaking navigated to the disclosed fixed search state. All three event links produced the matching H1 and exactly one current card link.
- A fresh review tab reported no console errors/warnings and contained no script elements. Two unlocated MutationObserver errors appeared during rapid navigation in the temporary QA tab; they did not recur in the fresh review tab. No authored runtime script exists to attribute them to.

## Evidence

`phone-browse.png`, `phone-event.png`, `tablet-browse.png`, `tablet-form.png`, `desktop-browse.png`, `bumble-light-desktop.png`, `review-gallery.png`.

## Remaining release checks

Screen-reader testing, native Safari/Firefox rendering, physical touch targets/safe areas, text-only enlargement, forced-colors operating-system rendering, actual organizer photo contrast and dynamic application states require testing in the implemented product. These source and smoke checks are not a full accessibility certification. No installable/offline PWA behavior is claimed.
