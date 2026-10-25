# Lineup · Sliding Filters

Open <http://127.0.0.1:4187/lineup-sliding-filters/index.html>.

Two desktop variants start with a wide event list and the individual event. The list header's filter icon reveals the original Lineup controls as a third column:

- **Between:** event list / search and filters / individual event.
- **Left:** search and filters / event list / individual event.

The browsing half changes from one wide pane into two equal columns. The expanded widths match approved Half Split/Lineup. The individual event keeps the same width and horizontal position during the reveal; its content remains natural document scrolling. The header stays sticky and both browsing columns end 48px above the viewport bottom. Apply remains in the original pinned action dock.

The composition animates grid tracks and their gutter over 440ms with one shared easing curve. The original filter content also translates by one existing 24px spacing step and fades. Rapid toggles reverse the CSS transition. Reduced motion switches without animation. Hidden filter controls are inert and removed from the accessibility tree; the launcher exposes expanded state, an accessible name and an applied-filter count. A visible Close action and Escape return focus to that launcher. The real page H1 remains accessible in the list when filters are closed and moves back to its original visible position when open.

No input or form is cloned. The original query, inclusive dates, category checkboxes, native disclosure and Apply/Clear controls retain IDs, listeners and explicit form association. Opening/closing preserves unapplied drafts and filter scroll position. Per-variant session storage retains the panel choice across real event/search navigation; unavailable storage simply limits that preference to the current page. Default fresh sessions start closed. Native validation reveals a hidden panel immediately before focusing an invalid date.

The list heading and filter action remain visible while browsing. Month jumps account for the heading's measured height. Below 1200px the adapter restores the original Lineup node order, disclosure, component geometry and controls. All earlier studies and the maintained app/kit remain unchanged. This is an isolated app composition, not a kit addition.

The implementation references [CSS grid tracks](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/grid-template-columns), [inert](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert) and [reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion). No framework, View Transition prototype, modal overlay, wheel interception or publication is involved.

Build/check this sibling only with Python `-B`:

```text
python -B tools/build.py
python -B tools/check.py
node --check sliding-filters.js
```

Use the existing port4187 server and its read-only `/base/` mount. `tools/slide_context.py` guards the preceding preservation chain, including Filter Spaces 1.0.0. Do not run parent/app/kit writers.

## Verification · 2026-10-23

All 107 generated HTML documents pass source/reference checks (8,245 local references). After removing only the declared private composition additions, 106 product documents match the preserved Lineup generator. JavaScript syntax passes. The full preservation chain remains unchanged: 980 app files, 180 kit files, 185 original desktop-study files, 177 width-study files, 177 earlier refinement files, 182 Lineup files, 176 Control Bars files and 178 Filter Spaces files. No kit component or primitive changed.

In-app Chromium checks cover 1200 × 600, 1440 × 900 and 1920 × 1080, expanded and collapsed. Both browsing columns start at y=117 and end 48px above the viewport bottom. Apply's dock bottom matches the list bottom. No horizontal page overflow occurs. At 1440px the expanded columns are approximately 322 / 322 / 668px, matching Half Split; collapsed browsing and event panes are both approximately 668px. The event's width and x position remain identical during and after the transition. Mid-transition geometry confirms interpolation in both directions; rapid keyboard reversal closes cleanly.

Each variant returns one workshop for November 1, zero results for a nonmatching query and all 48 events after clearing. The panel remains expanded through real search navigation. Reversed dates preserve the original inline error and native invalid focus. Close and Escape return focus to the launcher; reopening retains draft dates and the focused field. Collapsed controls have inert and aria-hidden attributes, and the original H1 returns to its accessible position in the list. The category scroll point also survives closing/reopening.

November's month header settles at y=249 and its first event title remains visible at y=361. The helper runs after the shared month handler, retaining its pending-navigation cancellation. At the bottom of the event document the header remains at y=0, and both list and Apply dock retain y=852 bottoms in a 900px viewport. Selecting First Sunday Print Exchange smoothly returns the document to the top and retains the expanded panel; browser Back restores the previous document reading position.

At 1024 × 768 and 390 × 844, both variants restore the preserved Lineup's header, introduction, summary, list and first-card geometry exactly in document coordinates. Six original inputs remain, query/date drafts survive and the private desktop filter badge is hidden. No horizontal overflow occurs.

`qa/` contains raw observations and four inspected open/closed screenshots. Reduced-motion source rules and the preference-change handler are included; the operating-system preference was not changed during this pass. Firefox and Safari were not physically run. This is not a complete accessibility certification.

The saved source release is `dist/lineup-sliding-filters-1.0.0.zip`, with an internal file manifest and adjacent SHA-256 checksum. It depends on the preserved sibling studies and adjacent app rather than packaging a second maintained kit.
