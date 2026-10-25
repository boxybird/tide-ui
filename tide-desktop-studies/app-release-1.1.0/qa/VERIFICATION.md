# App 1.1.0 verification

Verified on October 25, 2026 in Chromium on Windows. [Source checks](checks.json) pass for 421 HTML documents, 34,499 local references, BEM/component ownership, unique IDs, labels/form associations, valid times, one H1/main, consistent generated output and sixteen search/scope assertions. The baseline host CSS is byte-identical. The archived package additionally checks that every generated app/review HTML reference exists inside the package.

[Browser results](browser-checks.json) contain 34 passing observations. New screenshots in this folder are from the successor, not reused study evidence.

| Coverage | Observed result |
| --- | --- |
| 1440 × 900 desktop | 54 global / 6 venue samples; independent bounded left panes, natural right document. Native gutter 10px, bottom clearance 34px, list and Show events bottom both 866px. |
| 1440 × 640 short desktop | List/Show bottom both 606px, left list scrollable, no horizontal overflow. |
| Sticky handoff, both directions | October partially pushes off at list scroll 459.333px: outgoing header spans y158.333–218.333 beneath summary y117–249. Kicker/count/filter hit tests all resolve to summary. Reverse sample also passes. |
| Month jumps and wrapping | Native November jump settles at y249, exactly the summary bottom. At 1240 × 700 a long search query expands the summary to 180px; measured CSS offset is 180px and the visible month begins at y297, equal to summary bottom. |
| All six theme/modes | Tide, Summer, Bumble × light/dark: global list, event→venue→event, correct scope, usable guide, aligned footer, loaded images, no horizontal overflow. All six venue screenshots visually inspected. |
| Scoped filters | Draft live count changes before feed; one result, no results with guide retained, date+category combination, Reset/apply back to six, refresh, scoped event/return URLs, native Back, explicit exit to all 54. A query matching other venues cannot escape venue scope. |
| 1024 × 768 tablet | Bounded list beside guide; flyout opens, updates draft, first Escape cancels nonempty search and returns focus, apply and scoped event/return work. Desktop gutter input removed. |
| 390 × 844 / 320 × 740 phone | Natural list document, venue identity/address, no horizontal overflow. Venue details focuses its target at y121 below 97px header. Full-screen event hero is 844px tall; header/list hidden and return URL retains venue/query. |
| Open modal → desktop resize | Draft cancelled, dialog closed, one original search field restored, footer/list aligned. |
| Document reading / event selection | Scrolling right document keeps header y0 and left list y117–866. Selecting another event smoothly returns document to top before native navigation. Direct visible-card click then browser Back restores observed reading point exactly (252.667px). |
| Console | No warnings or errors in checked journey. |

Preservation checks pass: all 283 approved baseline files (including the full kit), all 92 venue-study files, all eleven accepted sticky-fix files, and prior locked releases/foundation match their recorded hashes. No writers ran in frozen trees. No UI kit component or primitive changed.

Limits: Firefox/Safari remain deferred at the user's request. No physical-device or screen-reader check is claimed. Browser zoom is unavailable through the connected in-app browser; responsive resizing and actual title/query wrapping are verified instead. Venue facts retain the original October 24 source date. Everything scheduled is sample data. This release adds no CMS, network data, accounts or PWA services.
