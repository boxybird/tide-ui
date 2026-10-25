# Browser verification — 24 October 2026

Actual engine: the connected in-app Chromium browser. Tests used an agent-created tab; the user's approved-prototype tab and its draft were not operated. All original files and dependencies are independently hash checked. Final results and measured rectangles are in `browser.json` (23 passing checks plus six theme/mode specimens).

## Geometry and preservation

- At 1440 × 900, rail, list, event, query, footer, Reset and Show events rectangles match the approved prototype exactly. Rail starts at x32; list x328; event x724.333. Footer/Show and list end at y866. Native occupied list gutter is 10px, so bottom clearance is 24 + 10 = 34px. Footer padding is 16px at the top, with a 16px gap between the status row and submit.
- One-result and zero-result lists occupy no native scrollbar width: the measured input becomes 0px and bottom clearance returns to 24px. One result ends at y876 in the same 900px viewport.
- 1280 × 720 and 1920 × 1080 keep both panel bottoms aligned with Show events and use the measured gap. Natural right-document scrolling retains the left panels and footer bounds.
- At 1024 × 768, the tablet modal, header, scrolling body, query, footer and submit match the prototype. Drawer width384px; submit bottom744px. At 390 × 844 the same geometry matches: drawer width342.667px; submit bottom820px. The browse-first feed also matches at both widths. Desktop gutter measurement is removed below75rem.
- All six new component specimens were opened: Tide, Summer and Bumble, each light/dark. Identical 576px-high panel geometry, scrolling body, pinned footer, disabled clean Reset and no horizontal overflow. Screenshots use the theme/mode filename.

## Behavior exercised in the copied app

Live draft changes leave the feed unchanged; desktop Close retains the draft. Enter applies one result through GET. Reset clears URL-prefilled query/date/category values without altering applied results. November1–29 with Music yields11 events. An inverted range is described and blocks navigation. Zero results remain submittable and use the existing empty recovery; Clear recovers48 events. Refresh restores URL criteria.

Modal Cancel, Escape and backdrop restore the opening draft and return focus. Shift+Tab wraps from the programmatically focused title to Show events; Tab wraps from the last control to Cancel. Enter applies and focuses the result count on the next page. Resizing an open modal rolls back before desktop mounting and retains one input set. Event navigation waits for the existing smooth return, opens Desert Frequencies with its local image, and Back restores Ink After Dark and the earlier reading position. No captured console errors or warnings remained in the final consumer navigation check.

Testing found one host integration edge: a native search input consumed the first Escape to clear its value. The copied host now intercepts Escape inside its modal and performs Cancel on the first press. This is not a kit runtime addition and does not modify the approved prototype.

## Limits

Firefox and Safari were explicitly deferred by the user. No claims of physical-device/software-keyboard or assistive-technology testing are made. Native no-script fallback is checked in source; it was not exercised with browser scripting disabled. Native scrollbar width remains platform-dependent; the copy measures actual occupied space instead of assigning a fixed width.
