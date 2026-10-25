# Kit adoption verification · app 1.2.1 / kit 1.1.0

## Scope

Reusable native disclosure and calendar groups moved from app CSS to the maintained kit. The existing neutral badge now has an explicit In view usage specimen, paired with an optional event-card modifier/status slot. Result-summary elements, behavior ownership and the promotion process are documented. The app consumes the shared definitions; viewport composition and data/navigation remain app-owned. No event, palette, space, type, radius, target or font primitive changed.

## Checks

- 40 tests pass: 14 kit contract/palette cases (including orphan-class and duplicate-style guards), 5 event-data cases and 21 search/navigation cases.
- 324 palette contrast pairs pass; all 93 generated kit outputs and 392 generated app documents are current.
- Kit markup check: 87 HTML documents, 1,386 local references, 12 fixture templates, 20 registered components, no browser scripts or inline styles.
- App check: 26,817 local references, all 34 shared block families registered, three approved deferred scripts, no ownership violations.
- Original 176-file kit and 263-file frozen three-event baseline verify unchanged. The complete 1.2.0 ZIP remains preserved.

## Browser evidence

Chromium in-app browser, using the real rendered app and native controls:

- `adoption-preservation.json` compares the desktop, open-filter and 320px app states before/after extraction. Measured component dimensions, type, colors, borders, outlines, padding, gaps and display values have **zero differences**.
- Adopted specimens render in all three themes and both modes, without horizontal overflow. Each has a working native disclosure, semantic card heading, neutral badge/outline and real month fragment targets. `adoption-theme-checks.json` records these checks.
- At 320px and 390px, date fields fit and disclosures retain 44px minimum summaries; no horizontal document overflow.
- A QA-only clone of the generated specimen uses a 32px root (200% text) and the actual shared CSS at the default 1280px viewport. It has no horizontal overflow; jump targets scale to 88px. `adoption-text-size.html`, `adoption-text-size.css` and `adoption-enlarged-text.png` record this check. This is not a browser zoom claim.
- Enter closed the disclosure; Space reopened it. Tab moved to the From date field with a visible focus outline. Native checkbox selection and Clear fields reset worked.
- App From/Through November 1 + Workshops returned one result and exactly one in-view card/badge. Adding unmatched text returned zero visible month groups and no in-view card. Clear restored all 48 events. The updated month jump focused `month-title-2026-11`, and selecting that event followed the real HTML route with the correct current link/state and document at the top.
- A fresh isolated kit/app tab reported no warnings/errors. An earlier rapid-navigation QA tab logged four unlocated MutationObserver errors; no authored app or kit source calls that API, and they did not recur in the isolated check. No attribution to application code is claimed.
- The user's original preview remains on Desert Frequencies, refreshed with the maintained kit and 48-event list.

The kit screenshot is `kit/qa/adopted-patterns.png`. The native Firefox/Safari, screen-reader, physical-device and operating-system forced-colors checks from earlier handoff notes remain outstanding. These checks are not a full accessibility certification.
