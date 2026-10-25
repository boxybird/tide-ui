# Margin Reveal · Browse first

[Live review](http://127.0.0.1:4187/margin-reveal-browse-first/index.html) · [Open prototype](http://127.0.0.1:4187/margin-reveal-browse-first/demo/index.html) · [Previous proposal](http://127.0.0.1:4187/margin-reveal-responsive-filters/index.html)

This is a browse-first hypothesis for an events discovery feed. The experiment prioritizes seeing events on arrival and keeps deliberate search/refinement one action away. It does not assume every visitor has the same intent; the visible header action gives goal-directed visitors a direct route to search. The earlier proposal and the approved desktop remain preserved.

## What changes below 75rem

The feed opens at The lineup, its count and month groups. The existing introductory H1 stays available to assistive technology but is visually hidden. The original search form moves into the flyout with the original date/category inputs. There is one query input and one set of filters. The single Show events action submits the whole original GET form; the separate search-arrow submit is hidden while this composition owns the form.

The header search action is a 48px icon button on phones and a labelled Search & filters button on tablets, reusing Button's quiet/icon modifiers. The header remains sticky so the action is still reachable farther down the feed. On split-view tablets, the existing bounded results pane accounts for that header height; the right event keeps natural document scroll. Header geometry comes from existing space/control/border tokens through one private composition variable. Desktop is excluded from these rules.

Search and filters open in a left modal sidebar, capped at 24rem and leaving at least 32px of the underlying phone page visible. Tablet uses the same capped width. The drawer overlays the app; it does not compress its columns. Entry takes 240ms and Cancel/backdrop/Escape dismissal takes 180ms. Reduced motion removes these effects. Resize restoration and GET submission close immediately.

The central body scrolls, with the existing Show events action pinned below it. Typing, dates and category choices preview the matching count with the existing search rules. Enter in search also submits the form. Reset all clears the draft query and filters; it stays in the panel until applied. Cancel, Escape and backdrop dismissal restore both query and filters to their opening values and return focus to the header action. The applied URL and feed do not change while drafting.

The dialog follows the visible viewport height/offset when the Visual Viewport API is available, so its footer can follow a software keyboard's visible area. CSS dynamic viewport height remains the fallback; pinch zoom is left native. See [MDN: visual and layout viewports](https://developer.mozilla.org/en-US/docs/Web/API/VisualViewport). The fixed-size review frames compare layouts; use the direct prototype link for physical-device keyboard testing, which remains part of adoption verification.

After applying, the existing count includes the query, the existing Badge names the selected categories (or says Dates set), and the original date-context/Clear all row is visible below the feed heading. That row is hidden only for an unfiltered feed. Clear all still returns all 48 events. Existing invalid-range explanation, empty state, real event links and Back behavior are reused. Sticky calendar labels stay below the persistent header; their stacking context is confined to the results pane.

## Component ownership and preservation

`tide-browse-flyout` is private app composition. `browse-flyout.css` extends the previous modal shell; `browse-flyout.js` owns temporary node placement, draft state and focus. The HTML hooks and candidate are registered in `component-candidates.json`. No component internals, raw palette values or maintained-kit files are changed. The existing Field, Choice, Button, Badge, type and spacing tokens remain their source of truth.

This is a candidate for later kit adoption after selection, all-theme specimens and device/assistive-technology testing. It does not create another maintained kit. The original native disclosure/search placement remains usable if the enhancement cannot mount. Every breakpoint transition restores the same nodes before the frozen desktop adapter mounts.

Native modal behavior and focus handling follow [W3C's dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) and [H102: native dialog](https://www.w3.org/WAI/WCAG22/Techniques/html/H102). No popularity claim is used to justify the browse-first choice; the two preserved proposals are testable alternatives.

Use Python `-B tools/build.py`, `-B tools/check.py`, then `-B tools/package.py`. All 73 files of the previous responsive-filter release, the aligned desktop release and the entire earlier dependency chain are hash-verified. New QA and release output belong here, with local previews on4187.
