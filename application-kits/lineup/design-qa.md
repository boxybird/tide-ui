# Lineup design QA · compact headers and header navigation

The earlier sections retain the workspace, navigation, event-return and filter-panel records. The current 2.2.0 real-menu/directory verification is recorded last.

## Findings

No actionable P0/P1/P2 visual differences remain in the selected header treatment. The two compact labels share 20px/28px Manrope at weight 580, their baselines and lower dividers align, and the first filter body and month feed begin at the same height. The right event document retains the original composition.

An earlier P1 implementation defect made the new count inherit 14px from the later component layer. Moving the variant's count declarations into Tide's canonical patterns module corrected the cascade. The final rendered count is 20px; the default Results count remains 14px.

## Target and evidence

- Source visual truth: [selected option three](docs/design/compact-headers-target.png), 1586 × 992 pixels.
- Implementation: `http://127.0.0.1:4187/events/app/index.html`, Bumble Dark, initial collection, closed drawer, document scroll at zero.
- CSS viewport: 1440 × 900. Reported devicePixelRatio: approximately 1. The browser screenshot service produced 1425 × 891 raster pixels; its output is JPEG despite the capture filename suffix.
- Final implementation capture: `build/qa/lineup-compact-headers/implementation-desktop.png` from the repository root.
- Equal-size full-view comparison: `build/qa/lineup-compact-headers/comparison.html` and `full-comparison.png`. Both original rasters are displayed together at 720 × 450, corresponding to the same 1440 × 900 CSS frame at half scale. The source's negligible aspect-ratio discrepancy is normalized to that frame.
- Focused comparison: `build/qa/lineup-compact-headers/headers.html` and `header-comparison.png`. Both images are displayed together at 1440 × 900, inside matching 780 × 230 crops starting at CSS y=85. This makes the title, divider, first field and month row readable at the same scale.
- Expanded measurements: `build/qa/lineup-compact-headers/measurements.json`. Routine browser captures and comparison pages are ignored development evidence; the selected source image is retained in the application kit.

## Comparison history

1. The first rendered implementation had 14px utility headings because the later Results count reset won the cascade. Evidence: `iteration-1-desktop.png` and computed font size. This was a P1 defect in the selected compact-title hierarchy.
2. The canonical variant count rule was placed after the default count rule in Tide's patterns module. Evidence: `iteration-2-desktop.png`, computed 20px/28px and equal filter/feed top positions. The final capture includes the subsequent CSS fallback geometry correction.
3. The final source/implementation pair was opened together for the full view and the focused header view. Both implementation title boxes begin at y=133 and are 28px high. The filter body and first month feed begin at y=193.667. No visual fix was required after this comparison.

## Fidelity surfaces

| Surface | Assessment |
| --- | --- |
| Fonts and typography | Manrope is loaded locally. Both utility labels use the authorized named 20px/28px recipe, weight 580 and normal tracking. Order remains 14px. Existing calendar/card typography remains canonical. The generated target's incidental heavier/larger month text is outside the selected header change. |
| Spacing and layout rhythm | Compact rows align at the top of the two left columns, with a lower divider and 16px external gap. The 20/35/45 tracks, 92rem bound, natural right document, native gutters and 24px pane clearance remain. The target's incidental left-track width and tighter choice spacing are normalized to these explicit repository contracts. |
| Colors and tokens | Existing Bumble Dark tokens supply foreground, canvas, surfaces, divider and yellow links/actions. No palette, primitive token, radius or shadow changes. The generated image's stronger separator contrast is treated as an image-generation artifact. |
| Image quality and assets | The original supplied event photograph, crop, gradient treatment, icons and font asset are retained. No generated repaint replaces an existing asset. The retained target is a layout reference, not a replacement photograph. |
| Copy and content | Search & filters, 54 events and Soonest first match the selected direction. Coming up, its tagline and The lineup kicker are absent from the browse interface. Authored route counts, useful venue information, accessible location context and native event titles remain. |

The generated mock packs all category choices above the footer. The application deliberately preserves Tide's 44px native choice targets and scrolling filter body; lower choices remain available by native scrolling. Existing cards and calendar rows retain their public recipe. These are intentional ownership/accessibility constraints, not unresolved attempts to copy the mock's incidental redraws.

## Browser and interaction verification

In-app Chromium on Windows using viewport emulation:

- 51 route/viewport cases: index, venue and Saved at 320, 390, 768, 959, 960, 1024, 1199, 1200, 1440 and 1920 by 900, plus seven other route families at 390, 1024 and 1440. One visible h1, no horizontal document overflow, zero browser scripts and one original query field where applicable.
- 30 theme cases: all five themes in light/dark at 390, 1024 and 1440. Nine short-window cases: index/venue/Saved at 1024, 1200 and 1440 by 500. Pane bottoms preserve at least 24px clearance.
- 20 Tide fixture cases: all ten theme/mode pairs at 390 and 1440. Utility counts and foreign-context counts are 20px/28px; default count/order text remains 14px; hidden cases have no box. Lower hairlines match the default hairline's device-pixel-snapped thickness.
- Entered a query, two native dates and Comedy, then activated Reset: all four fields returned to their authored defaults. Close and Escape dismiss the native popover and return focus to Filters. Clicking the visible strip outside the drawer dismisses it. The native Date and category disclosure collapses and expands.
- A query survives resizing an open drawer from 390 to 1440. CSS anchors fit its rectangle exactly to the reserved desktop filter column. An ignored QA fixture removes the named anchor to exercise the declared CSS fallback; index and venue differ from the reserved top by only the expected 0.333px border snapping and retain the same left edge, width and bottom.
- Native November fragments at 1440 and 1024 keep the summary exposed and the month at the feed top. Venue fragments reserve the information jump; About this venue reaches the useful information section. No custom history or browser scripting is involved.
- At 320 × 500 the drawer body scrolls while its footer stays pinned and visible. There is one query control and no horizontal document overflow.
- Console warnings/errors checked after the app interactions: none recorded.

Firefox/Safari, physical devices, screen readers and changed system motion preferences remain unverified. The fallback fixture verifies Chromium's fallback expressions, not another browser engine.

## Review and completion

The user reviewed and accepted the Tide 1.11.0 recipe and Lineup 2.1.5 integration on 2026-10-27, then requested preservation on main. No deployment or service work is part of this change.

Implementation checklist: visual comparisons complete; native interactions complete; responsive/theme checks complete; repository build and contract checks passed.

`npm run build` and `npm run check` passed. The check covered 1,031 generated HTML files, 55,763 local references, 578 Markdown references, performance budgets, browser-JavaScript prohibition and 115 tests (7 preview HTTP, 67 Tide palette/contracts and 41 application template contracts). Tide CSS is 99,988 bytes and Lineup CSS is 18,508 bytes, within the unchanged budgets. Git diff whitespace checks pass; `main` is the only branch. The implementation starts from `8239327`.

The first repository check rejected an application wrapper selector that referenced the shared Results variant. External spacing now uses the explicit private `tide-lineup__summary--utility` class; no ownership exemption or shared-check relaxation was added. The application builder includes this review record, and package documentation avoids source-file links that are unavailable in the built reference site. The complete check passed after these corrections.

## Header navigation · Lineup 2.1.6 / Tide 1.12.0

The current integration implements the third displayed navigation option using the separately reviewed Tide treatment. Source target: [centered navigation mock](docs/design/centered-navigation-target.png), 2128 × 739 pixels representing a 1440 × 500 CSS crop. The stronger implementation reference is the accepted native Tide header in `build/qa/tide-navigation-review/after-header.png` (1377 × 93 pixels).

Implementation: `http://127.0.0.1:4187/events/app/index.html`, Bumble Dark, 1440 × 900 CSS viewport, initial scroll, closed drawer and no pointer/keyboard state. Capture: `build/qa/lineup-header-navigation/desktop.png` (JPEG 1425 × 891 despite the suffix). Exact header capture: `header.png` (JPEG 1361 × 93), measuring 1360.667 × 92.667 CSS pixels. DevicePixelRatio is approximately 1.

Combined evidence: `build/qa/lineup-header-navigation/comparison.html` and `comparison.png`, rendered at 1504 × 960. The selected mock and actual application are shown together at equal 720px width, normalized to the same 1440px CSS context. The actual application is cropped to the mock's upper 500px. Reviewed Tide and Lineup header captures appear together at their native CSS dimensions; focused primary-link and Saved crops align their centers/trailing edges to account for the 16px component-width difference. Both full composition and readable focused controls were inspected from this combined input.

Fonts: navigation uses the reviewed Manrope 14px/22px weight 550 and normal tracking. Geometry: 44px minimum, 10px/16px padding, 2px radius, reserved hairline and 18px source icon. Colors: current-page selected surface/text and native hover/active/focus roles match Tide. Assets: the original supplied icon, wordmark and application photograph are retained. Copy: destinations remain Find events, route-appropriate Sunshine Theater/Add an event, and Saved. The generated image's incidental photo/type/spacing differences below the header are intentionally excluded; the existing application composition is preserved.

An initial P1 inspection found a missing current-page fill because a nested extension layer could not override Button's unlayered owner inputs. The stylesheet now joins `tide.components`, matching its canonical owner. A regression guard protects that layer. The final app and reviewed-Tide comparison show the selected fill/text correctly. No actionable P0/P1/P2 mismatch remains after this fix; the post-fix combined comparison required no further visual change.

Verification completed:

- Thirty before/after geometry cases cover index, venue, Saved, Help, submission and a native event at 390, 768, 1024, 1200 and 1440 by 900. Desktop and split-tablet pane rectangles are identical. Narrow headers wrap naturally; content retains the same widths/heights and moves only with the header's normal-flow height. Native event header omission is unchanged.
- Ninety theme cases cover index/venue/Saved in all ten theme/mode combinations at 390, 1024 and 1440. Native navigation targets, type, padding and radius match the kit; no overlapping controls, horizontal overflow or scripts. Desktop primary links are centered.
- Ten promoted Tide state cases verify actual hover/current/selected feedback and keyboard focus across every theme/mode. In Lineup, native Tab exposes the shared 2px outline with nominal 3px offset, and held pointer feedback shows the 2px inset keyline at unchanged 44px height. Current-page fill remains independent of focus and hover.
- Native venue and Saved links, exact current-page semantics and browser Back pass. A query survives widening an open drawer from 390 to 1440; the same single control set fits its reserved column exactly. Native Reset clears it; Escape dismisses and returns focus to Filters. The desktop November fragment retains the permanent summary and aligns at y=193.667 with document scroll zero.
- SHA-256 parity: all five application stylesheets, data and non-header templates are unchanged. All 738 generated main-content sections are identical. Tide's default CSS modules, palette inputs and assets are unchanged; navigation is a separately loaded canonical extension.
- Browser console warnings/errors: none recorded. Expanded measurements and parity reports are in the ignored QA folder. The user accepted the header integration and requested its commit and push on main.

A further 60 narrow-theme cases at 320/390 verify the final header spacing, with no overlaps, horizontal overflow or scripts. The final root build/check passes: 1,041 HTML documents, 56,891 local references, 607 Markdown references and 121 tests (7 HTTP, 72 Tide, 42 application), including unchanged performance budgets and ownership guards. Firefox/Safari, physical devices, screen readers, actual text zoom and changed OS forced-color/motion preferences remain unverified.

## Header placement · Lineup 2.1.7 / Tide unchanged

The user requested primary navigation beside Saved instead of centered, plus Filters at the far right of the second row when the header collapses. Lineup now owns a private inner grid in `header.html` / `base.css`; the public centered modifier is removed from application markup. The existing Site header shell and navigation actions retain their Tide appearance. A named 24px external gap distinguishes Saved from the primary links. Below 60rem, Burque/Saved occupy row one and primary navigation/Filters occupy row two. Links can wrap in their own cell. This is native CSS Grid with no absolute placement, duplicated controls or browser JavaScript.

Evidence from in-app Chromium on Windows, 2026-10-28, is in ignored `build/qa/lineup-header-placement/`: `desktop-before.png`, `desktop.png`, `phone.png`, `before.json`, `after.json`, `themes.json` and `breakpoints.json`. Desktop comparison uses 1440 × 900; phone uses 390 × 900. Appearance inputs remain Manrope, canonical compact 44px actions, 48px Filters, original padding/radius/focus/state colors, source icon, event photo and all copy. The private brand wrapper prevents the wordmark link's focus area from stretching across the flexible leading track.

- Thirty before/after cases cover six route families at 390, 768, 1024, 1200 and 1440px. From 960px upwards every measured header/main/pane rectangle is identical. Narrow content keeps its dimensions and follows the new header height in normal flow.
- All ten theme/mode pairs pass at 320, 390, 768 and 1440px for index, venue and Saved: 120 cases with no overlapping controls, horizontal overflow or scripts. Eight edge cases around 480/704/960/1200px also fit. Split/desktop panes retain 24px bottom clearance at 700px height.
- Native pointer and Enter open the same popover; Close and Escape dismiss it and return focus to Filters. An entered query survives a 390-to-1440px open-drawer resize; the panel exactly matches its reserved column and still has one query field. Reset clears it. Venue/Saved links and browser Back preserve document-accurate current states. Keyboard focus remains a 2px outline with nominal 3px offset. Browser warnings/errors: none.
- SHA-256 comparison confirms all 122 Tide/site source files unchanged and all 737 generated route main sections unchanged. Only application-owned canonical files are edited; Tide remains 1.12.0.

Firefox/Safari, physical devices, screen readers, actual text zoom and changed system motion/forced-color preferences remain unverified.

Root build/check passed with 1,041 HTML documents, 56,891 local references, 611 Markdown references and all 121 tests (7 HTTP, 72 Tide, 42 application). Performance and strict component-ownership checks pass. Canonical changes are confined to Lineup; `main` remains the only branch. The user reviewed and accepted this placement change and requested that it be committed and saved on 2026-10-28.

## Event return availability · Lineup 2.1.8 / Tide unchanged

The user requested removal of the event photo's top-left back arrow when the list is already visible beside the event. The control is a native `index.html` link, not browser history. Application `base.css` hides its private host from the existing 60rem split breakpoint. Below 60rem the same link remains available on full-screen event documents. A private flex host preserves its original 44px geometry; retaining the hidden leading slot keeps the optional Saved control on the right. When Saved is absent, an outer private host omits the empty toolbar. No shared component style, token, event data, browser script or positive tabindex is added.

In-app Chromium on Windows, 2026-10-28:

- Twenty-five before/after cases cover index, venue, Saved, a full event and a concise event at 390, 959, 960, 1024 and 1440px. Hero/title/results/optional Saved rectangles are identical. The arrow is available only below 960px on a visible event, with no horizontal overflow.
- Twenty cases cover all ten theme/mode pairs at 390 and 960px on a full event. Visibility, remaining controls and zero browser scripts pass.
- Shift+Tab from the photo Saved control skips the hidden arrow in split view and reaches it on phone. Enter on the phone arrow returns to the visible all-events list; browser Back restores the event route. Concise split views omit the empty Event navigation from the accessibility tree. Browser warnings/errors: none.

Ignored evidence is in `build/qa/lineup-event-back/`: `before.json`, `after.json`, `themes.json`, `desktop-before.png`, `desktop.png`, `phone.png` and the dependency fingerprint record. All 122 Tide/documentation-site source fingerprints remain unchanged. Coverage does not include Firefox/Safari, physical devices, screen readers or changed system preferences. The user accepted this application checkpoint and requested preservation on 2026-10-28. The starter notes also record the consuming-site upgrade expectation; no additional application behavior or component reorganization was introduced.

Root build/check passes: 1,041 HTML documents, 56,891 local references, 615 Markdown references and all 121 tests (7 HTTP, 72 Tide, 42 application), including strict ownership, zero browser JavaScript and unchanged performance budgets. All canonical edits are within Lineup; `main` is the only branch.

final result: passed

## Filter-panel spacing · Lineup 2.1.9 / Tide unchanged

The visible headings read Search & Filters. A private content wrapper adds Tide's named 24px top clearance only in the mobile/tablet drawer. Category adopts the compact plain-fieldset/choice composition from Tide's existing filter-disclosure specimen: 44px choice rows with no extra Stack gap. Date fields retain Stack, and no shared component internals are overridden.

The [spacing contract](docs/FILTER-PANEL-SPACING.md) records the 30 all-theme phone/tablet/desktop spacing cases, four boundary/short-screen cases, venue scope, native Reset/dismissal/focus and open-drawer resizing. Desktop search form/label/input rectangles at 1440×900 match the settled baseline exactly. All 121 repository checks pass (7 HTTP, 72 Tide, 42 application). Expanded evidence remains ignored under `build/qa/lineup-filter-panel/`; current browser coverage is Chromium on Windows, with the limits recorded in the contract.

## Real menu and venue directory · Lineup 2.2.0 / Tide unchanged

The primary menu consistently offers Find Events, Venues and Add an Event, with Saved separate and Help in the shared footer. The native directory adopts existing Content page and Venue card recipes and links to Sunshine Theater's profile, schedule and information. This retains the current wrapping as the baseline for the next responsiveness review; phone wrapping is not presented as a finished redesign.

The [navigation/directory contract](docs/VENUES-NAVIGATION.md) records forty all-theme phone/desktop cases, six small/tablet cases, native journeys, filter preservation, consumer migration and browser limits. All 122 repository checks pass (7 HTTP, 72 Tide, 43 application). The four filter source files remain byte-identical to the 2.1.9 working checkpoint; protected Tide/reference-site/shared-tooling sources remain unchanged. Raw measurements and screenshots stay ignored under `build/qa/lineup-real-navigation/`.

## Native mobile Menu · Lineup 2.2.1 / Tide unchanged

Below 34rem, a native Menu popover replaces the inline primary presentation. Brand/Saved retain row one; Menu/Filters share row two. A registered partial authors the real links once for both presentations. Private CSS controls responsive mounting and anchored placement; existing Tide navigation buttons, Icon and unchanged Panel provide appearance. All 68 routes and the original filter control set remain.

The [mobile navigation contract](docs/MOBILE-NAVIGATION.md) records ten phone theme/mode cases, twenty exact desktop header comparisons, 320×500 and breakpoint/tablet checks, keyboard/outside dismissal, native link journeys, Filters interaction and resizing. All 124 repository checks pass (7 HTTP, 72 Tide, 45 application). Protected sources and the four filter-panel files are unchanged. Expanded evidence stays ignored under `build/qa/lineup-mobile-menu/`; browser and fallback testing limits are explicit in the contract.

## Desktop first-label alignment · Lineup 2.2.2 / Tide unchanged

From 75rem, the private utility-summary gap is 8px instead of 16px. Together with Tide's unchanged 8px calendar-header padding, October 2026 starts 16px below its utility divider, level with Search Events. Native month-fragment reservation shares the gap input. Mobile/tablet keep the 16px external gap and 24px divider-to-month-title spacing. Saved continues to use its separate default Results composition.

In-app Chromium on Windows, 2026-10-28:

- Eighteen before/after cases cover index, Sunshine Theater and Saved at 390, 1024, 1199, 1200, 1440 and 1920×900. Index/venue labels align exactly at desktop widths. Their feed starts 8px earlier and retains its bottom edge; search controls, utility headers, filter rail and right event document rectangles are unchanged. Every measured rectangle below 75rem and on Saved is identical.
- Twenty theme cases cover all ten theme/mode pairs at 390 and 1440×900. Phone measurements match the baseline exactly; desktop labels align. No horizontal overflow or browser scripts were found.
- The opened 390px filter drawer retains exactly the same measured geometry, including 24px heading-to-search clearance. November links on desktop index/venue and split-tablet index align the target header to the feed top with outer document scroll zero. The permanent summary stays exposed and desktop pane bottoms retain 24px clearance.

Expanded evidence remains ignored under `build/qa/lineup-desktop-label-spacing/`. Firefox/Safari, physical devices, screen readers and changed system preferences were not exercised for this spacing patch.

`npm run build` and `npm run check` pass, including all 124 tests (7 HTTP, 72 Tide and 45 application), ownership guards, documentation links, performance budgets and the browser-JavaScript prohibition. All 135 protected Tide/reference-site/shared-tooling files match the starting fingerprints. Canonical edits are confined to Lineup, with `main` as the only branch.

## Consistent utility-summary spacing · Lineup 2.2.3 / Tide unchanged

The accepted desktop fix was committed and pushed as `67f4b16` before extending its private 8px summary gap to every width. The first month title on unscoped browse pages now starts 16px below its divider on mobile, tablet and desktop. Shared Results/calendar padding and typography remain canonical; the application breakpoint override is removed.

In-app Chromium on Windows, 2026-10-28:

- Eighteen before/after cases cover index, Sunshine Theater and Saved at 320×500 and 390, 768, 1024, 1200 and 1440×900. Below 75rem, utility feeds start 8px earlier. Headers, utility rows and filter geometry are unchanged. Single-column venue information follows the shorter list by 8px in ordinary flow with identical dimensions; the split right document stays in place. All measured desktop and Saved rectangles match 2.2.2 exactly. No horizontal document overflow or scripts were found.
- Twenty cases cover all ten theme/mode pairs at 390 and 1440×900. Phone browse clearance is 16px; every desktop measurement matches 2.2.2. Venue pages retain their existing information-jump allowance above the month feed.
- The 390px drawer's heading, title, content and search label retain identical geometry and 24px heading-to-search clearance. Native November links on split-tablet index and venue align the target header to the feed top with outer document scroll zero. The permanent summary stays visible and bounded feed bottoms retain 24px clearance. Console warnings/errors: none recorded.

Evidence remains ignored under `build/qa/lineup-summary-spacing/`. Firefox/Safari, physical devices, screen readers and changed system preferences were not exercised for this spacing patch.

`npm run build` and `npm run check` pass, including all 124 tests (7 HTTP, 72 Tide and 45 application), ownership guards, performance budgets, documentation links and the browser-JavaScript prohibition. All 135 protected Tide/reference-site/shared-tooling files match their starting fingerprints. Canonical edits remain within Lineup, with `main` as the only branch.
