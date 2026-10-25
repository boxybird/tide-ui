# Tide responsive app study

- Original approved kit is `../tide-ui-kit/`. Preserve it. This directory consumes its independent reviewed copy in `kit/`, version 1.0.1.
- User still favors Tide and Date Line. No new palette or layout favorite has been selected in this iteration.
- Plain HTML/CSS foundation. No React or app services are needed. The user explicitly requested smooth return to the top when selecting another event after reading down the right side. The optional `js/event-navigation.js` enhancement lets CSS smooth scrolling finish before following the real event href, retains list position and respects reduced motion. Keep native link fallbacks and modified-click behavior. Build using `tools/build.py`; edit that source and `data/events.json`, not individual generated theme pages.
- Keep typography, touching cards, dates, square corners and semantic colors from the kit. Composition belongs in `css/app.css` (`tide.app` layer). Review presentation belongs in `css/review.css`.
- Three named themes, each with light/dark modes; adding a theme to the kit source generates the app variants too. No component selectors by theme name and no raw app palette values.
- Keep desktop contained at 70rem. Pair results/detail only when there is room. One column is the mobile and portrait-tablet default. Right detail scrolls in the document. Desktop results must fit on arrival with 24px below their closed container, including in short windows. Use shared header geometry and dynamic viewport units; do not forget the header/top gap when calculating available height.
- Use semantic heading levels with the kit's public heading classes. Native controls, labels, focus states and skip navigation must remain intact. No colored left callout stripes.
- Search/saved are disclosed fixed sample states; submission sends nothing. This is not an installable PWA. Preserve that distinction in handoff.
- Rebuild the kit and app, run checks/tests in README, and verify changed layouts in a real browser. Keep QA evidence separate from compatibility research. Preserve original hashes in `qa/original-kit-lock.json`.
- Keep local. Preview server binds 127.0.0.1:4186 only. Do not publish without user instruction.
