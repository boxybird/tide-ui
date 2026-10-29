# Compact venue heading and search · accepted foundation · 2026-10-29

final result: passed

Scope: tidy the top of the directory while preserving the user-approved photo-free rows and Venues / Albuquerque utility heading. Removed the filler tagline and separate venue-count line. The native labelled search remains; private `space-4` padding supplies 16px from heading divider to label and 16px between the search area and list surface. No Tide component appearance changes.

At 1488x1058 the intro is 60px shorter (228.67px to 168.67px). Its utility heading coordinates are unchanged, and the measured divider-to-label gap exactly matches Search events on the home page. The five responsive cases from 320 through 1488px have no horizontal document overflow and retain all six rows; all ten desktop theme/mode combinations have the same 16px spacing. Phone List/Map switching retains a 228.67px header and a usable 48px search input in both views.

Root build/check passes all 130 tests. The approved row template, individual venue documents, map image/points/popovers, shared header and Tide sources remain unchanged. Removed the unused directory-count template value and obsolete context-hiding rule. The previously recorded tall-tablet map clipping issue is outside this header refinement and remains open.

Evidence: ignored `build/qa/lineup-venues/compact-intro/` contains before/after desktop images, a phone image, responsive/theme measurements, native view-switch results and boundary fingerprints. Retained desktop evidence is [the current directory](docs/verification/venue-directory-desktop.jpg). Browser coverage is Chromium on Windows; Firefox/Safari, physical devices, screen readers and text zoom remain untested.

The user approved the current list/map as the foundation for continued work on 2026-10-29. Tag `lineup-v2.3.0` preserves this Lineup 2.3.0 checkpoint with Tide 1.12.0 unchanged. Individual venue pages and the recorded map issue remain open for refinement. Historical pending-review/uncommitted notes below describe earlier measurement-time states and are superseded by this checkpoint.

---

## Photo-free venue list · accepted by user · 2026-10-29

final result: passed

Scope: adopt the home-page event-list appearance for the venue sidebar without changing Tide, map interactions or individual venue documents. This supersedes the photo-row direction for the directory list only. User approval of the overall venue experience remains pending; nothing is committed or pushed.

- Reused unchanged Event list/card slots for venue type, a level-two name, Albuquerque scope, fixture-derived listed-event count and Show on map. Canonical 24px card padding, 24px/32px titles, category/support/metadata type, surface, texture and separators match Find Events. No list photos, fake dates/prices, private component restyling or browser JavaScript is added.
- Desktop list width follows Find Events' 35% middle-track calculation and uses the same thin native scrollbar. At 1488px the pane and card widths differ by less than 0.02px of CSS track rounding. Search/heading/card text share their canonical 24px inset. The wider list reduces the map's available width; map templates, point coordinates, callouts and image bytes are unchanged.
- Twenty direct card-role comparisons cover all five light/dark themes at 390 and 1488px: no computed differences for card, category, title, support, metadata or accent roles. Seven responsive cases span 320–1920px, retain six rows and have zero horizontal document overflow and zero list images.
- Native keyboard card navigation opens Sunshine Theater, Show on map targets its visible native point on phone, and Escape returns focus to the marker. The listing's independent action layer keeps the map link above the covering venue link. Native focus outlines/title color come from Tide.
- Root build/check passes 72 Tide, 51 application and seven HTTP tests. Existing event-card structure/adoption checks cover the new usages; the directory destination test now expects six listing cards. No additional mirrored implementation test is introduced for this composition change.

Evidence: ignored `build/qa/lineup-venues/list-refactor/{before,event-reference,after-desktop,after-mobile}.jpg`, `responsive.json`, `theme-parity.json`, `interactions.json` and `boundary.json`. Current retained desktop image: [venue directory](docs/verification/venue-directory-desktop.jpg). The event feed is the style authority for this pass; the earlier photo-row mockup is historical direction, not a pixel-match target for the new list. Browser coverage is Chromium on Windows; other engines, physical devices, screen readers and text zoom remain untested.

Separate map observation for the upcoming map review: an additional tall-tablet check at 1024x1058 exposes partial Warehouse Room marker clipping in the existing cover fit. This viewport's map/grid rules are unchanged by the list refactor. The 1200/1488/1920px desktop checks have no clipped markers, no map scrollbars and 24px bottom clearance. Recorded in `map-regression.json`; this scoped list result does not close that map issue.

---

## Previous frame/search/map refinement (historical)

final result: passed

Scope: the three issues reported by the user—application frame width/insets, the missing left-column search field, and map X/Y scrollbars. This result covers those corrections and their regression checks. The complete venue experience remains under user review; nothing is committed or pushed. The prior native acceptance below was superseded by the user's rejection.

## Findings and fixes

- **P1 · Application frame mismatch, resolved.** The independent 92rem wrapper and added header insets did not match Find Events. The directory now consumes Lineup's existing desktop content width/insets and native scrollbar gutter; tablet/phone consume its existing maximum widths. A directory-only viewport wrapper gives the natural header and main Grid rows and puts the footer below the initial frame. Seven direct comparisons (390, 768, 1024, 1200, 1488, 1920, 2560) have exactly zero delta for header left/width, brand left and main left/width. Evidence: `build/qa/lineup-venues/refinement-widths.json` and `refinement-frame.png`.
- **P1 · Search field omitted, resolved.** The canonical Tide Field is back above the venue rows, with visible Search venues label and 48px input. Its native GET/q contract matches the event-search pattern. Removed redundant application spacing beneath it; the Venue card supplies its own 24px block spacing. Enter submits `venues.html?q=Sunshine`; the static preview retains all six fixtures because matching belongs to the consumer. Evidence: `refinement-search.json`, `refinement-focus.png`; new source test protects the form/label/control contract.
- **P1 · Two-axis map scrolling, resolved.** The old oversized illustration was made scrollable. It is now centered in a non-scrolling image frame, with desktop cover fit and complete-image fit in the single-column view. Container queries separate the two close labels on smaller illustrations without moving their points. No internal X/Y scrollbar dimensions, clipped 44px point controls or horizontal document overflow in 19 responsive states. At least 24px bottom clearance remains. Evidence: `refinement-responsive.json`, `refinement-labels.json`, `refinement-desktop.png`, `refinement-phone-map.png`.

## Comparison target and normalization

Source visual truth: the approved standalone direction retained at `docs/design/venue-directory-approved.jpg`, plus the actual native Find Events route as the frame/layout authority. Implementation: `http://127.0.0.1:4187/events/app/venues.html`, retained `docs/verification/venue-directory-desktop.jpg` and ignored `build/qa/lineup-venues/refinement-desktop.png`.

The approved image, Find Events screenshot and implementation screenshot are each 1488x1058 raster pixels at a 1488x1058 CSS target, effective density 1. State: Bumble Dark, six venue entries and Sunshine's callout open on the venue page. Find Events uses its standard default state. Native scrollbar gutters are intentionally present on both application documents. No browser chrome/device frame is compared.

Full source/native comparison is saved together in `refinement-comparison.png`, with each image at equal 592x420.925 display size. Actual application frame comparison is saved together in `refinement-frame.png`. Focused native-scale paired crops of source and implementation search/rows are in `refinement-focus.png`. The source uses an experimental compact row and inset search icon; canonical Tide Field/Venue card interiors remain the implementation authority rather than adding private overrides.

## Required fidelity surfaces

- **Typography:** local Manrope, canonical 20px/28px utility/title roles, Field label/input and plain underlined link roles. No font/type override or new arrow treatment. Checked visible search and row hierarchy in the focused comparison.
- **Spacing/layout:** exact native frame parity at seven widths, search restored before the isolated list, no doubled search-to-card host gap, 24px minimum pane clearance, footer below the initial frame. Card interiors retain Tide's 24px padding; the reference's 12px experimental card density is not silently restored.
- **Colors/tokens:** unchanged Bumble palette and all ten theme/mode pairs. Existing photo-accent, Photo control and Panel roles remain. No new component colors/borders/padding/focus recipe.
- **Image quality:** same approved generated photos and map, unchanged optimized asset bytes and crop direction. The illustration fills the desktop frame without scrollbar artifacts; the complete image is fitted on narrow views so point controls remain visible. Label placement is app composition; locations and source art are unchanged.
- **Copy/content:** Search venues label and native q hook restored; six names/counts and 54 event fixtures unchanged. The caption identifies illustrative photos/locations. No live-map or matching service is implied by the static preview.

## Verification and limits

Chromium on Windows: 19 responsive states with verified actual viewport dimensions, seven direct application-frame comparisons, 30 fresh theme/state cases and nine narrow/map-label checks. Search native GET and marker popover Escape/focus return pass; console warning/error capture is empty. Root build/check passes: 72 Tide + 51 application + seven HTTP tests. All 67 non-directory original documents remain byte-identical; 133 Tide/reference-site/shared-tool source hashes and the Tide distribution remain unchanged. Main is the only branch; all canonical edits remain inside Lineup.

The map is still a generated illustration. A live provider, live text matching and enhanced consumer navigation are separate integration decisions. This pass does not claim Firefox/Safari, physical-device, screen-reader, forced-colors or text-zoom verification, or final user approval of the full venue experience.

## Implementation checklist

- [x] Match the actual application frame, with measured parity.
- [x] Restore the existing Tide search field and document its consumer contract.
- [x] Remove map scrollbars without hiding its native point controls.
- [x] Compare source/native full and focused views, update evidence and retain boundaries.
- [x] Keep Tide unchanged and all work uncommitted/unpushed.

---

## Superseded native translation review (historical)

# Lineup native venue directory · 2.3.0

final result: passed

The reviewed standalone photo-list/map direction is implemented with unchanged Tide 1.12.0 components and Lineup-owned native composition. No actionable P0/P1/P2 findings remain against that direction and the explicit zero-browser-JavaScript / existing-components boundary.

## Source, state and comparison evidence

- Visual source: `docs/design/venue-directory-approved.jpg`, the user-approved standalone prototype capture. It is review evidence only; no prototype code/runtime is copied.
- Rendered implementation: `http://127.0.0.1:4187/events/app/venues.html`, screenshot `docs/verification/venue-directory-desktop.jpg` (also `build/qa/lineup-venues/desktop.png`).
- Source and implementation are both 1488x1058 raster pixels; the native CSS viewport is 1488x1058, effective density 1. Both show Bumble Dark, all six entries and Sunshine Theater's map information. The native map has browser-owned scroll position and the existing Sunshine information link.
- Full combined comparison: `build/qa/lineup-venues/comparison.png`; source/native together at equal 592x420.925 display size, no browser chrome or device frame.
- Focused combined comparison: `build/qa/lineup-venues/focus.png`; native-scale paired venue-row and Panel crops. Component origins are normalized independently (source row y325/native y270, source Panel crop y440/native y530) because native card rhythm, footer and omitted runtime search deliberately change vertical placement.

## Required fidelity surfaces

- **Typography:** unchanged local Manrope; the utility h1 computes to 20px/28px/580, matching Lineup's filter/results headings. Venue card and Panel titles use canonical 20px roles. Metadata uses canonical Caption, links retain 14px regular underlined text with no added arrows. Font weight, hierarchy, wrapping and focused crops were checked; no private type adjustments.
- **Spacing/layout:** centered 92rem directory, 428px list/20px gap/976px map at the comparison viewport. Native header/footer size the workspace through Grid. Canonical Venue card 24px block padding replaces the prototype's 12px experiment; no selected-card appearance is invented for a component without that variant. Both bounded panes end 24px above the footer. Short-height windows use natural page scrolling. The optional consumer search/zoom UI is omitted instead of shipped as inactive chrome.
- **Colors/tokens:** unchanged theme pairs, neutral rules, square kit controls and existing Panel surface. Native map squares paint the standard SVG glyph with the existing photo-accent token, preserving its intended contrast over the map in light and dark modes; 44px Photo controls keep the kit's photographic backing and interaction states. Both mobile Menu and map callout have identical computed Panel background, text, border, radius, 24px padding, 12px gap, shadow and body type. No custom marker/callout colors, type or border override.
- **Images/assets:** all seven approved generated image concepts are placed. Served WebP derivatives preserve the art direction/crop with explicit lossy encoding and intrinsic dimensions; each is below 200KB. Photos/points are illustrative rather than documentary/geographic facts. The standard filled Square icon comes from Phosphor with its license retained; no substitute CSS drawing or generated screenshot-as-page implementation. Thumbnail sharpness, map raster scale and focused crops were inspected.
- **Copy/content:** six exact fixture venue IDs/names and derived counts total 54 events. Five additional native venue documents expose their existing event lists; Sunshine retains attributed visitor information. All 67 non-directory original documents are byte-identical. No new address/accessibility/facilities claim is invented. A discreet illustration caption communicates the map's limits.

## Iterations and resolved findings

- P2: the directory's new body Grid initially allowed its auto-margin header to shrink to content width. Added external inline-size on the existing private header host; final screenshot shows normal brand-left/navigation-right placement.
- P2: a phone row's initial Map popover trigger hid its own containing list when the map opened, losing native focus return. Replaced it with a native fragment link to that venue's exact map point. The marker then opens the native popover, with persistent fragment/focus visibility. Post-fix phone interaction evidence verifies Escape returns to the visible 44px marker.
- P2: first-pass callout placement declarations touched two shared aliases not allowed by the strict application contract. Moved placement/heading clearance onto ordinary private wrappers; the shared Panel/title/close Button interiors remain unchanged. The strict presentation check passes without extending its allowlist.
- The first restricted HTTP test run could not connect to its loopback port; the approved loopback-enabled check passed. A CSS rule-parity test initially compared formatting strings across colon-whitespace compaction; it now compares ordered selectors and exact property/value pairs, while separate fixtures retain string, URL, escaped-newline, license and calc-value checks. These are tooling/verification fixes, not visual iterations.
- Final full/focused comparisons show the approved hierarchy retained. The explicit canonical normalization of row spacing, photo controls, footer, native map scrolling and runtime-only search is acceptable under the requested adoption boundary.

## Actual verification and limits

Chromium in-app browser on Windows: 30 theme/state cases across all ten theme/mode combinations (phone list, phone map/callout and desktop/callout); 16 responsive cases from 320x500 through 1920x1080. One visible h1, zero scripts, no document horizontal overflow and viewport-contained long-name callouts in every recorded case. Five new venue documents have correct counts and no phone overflow. Verified directory → Sister → Desert Frequencies → native browser Back, fragment focus, native popover Escape/focus return and mobile Menu Panel parity. Console warning/error capture is empty.

Root build/check: 803 application documents; 72 Tide tests, 50 application tests and seven HTTP tests. Application CSS remains below 22KB raw/5KB gzip, with all declarations protected by parity tests; the seven new served venue images remain below 200KB. All 133 protected Tide/site/shared-tool source fingerprints and the vendored Tide distribution remain identical. Main is the only branch and all canonical edits are in Lineup.

Detailed evidence: `build/qa/lineup-venues/{themes,responsive,profiles,interactions,console,boundary}.json`, with phone/map/short-phone screenshots. The [directory contract](docs/VENUE-DIRECTORY.md) documents sources, integration boundaries and migration. Firefox/Safari, physical devices, screen readers, changed system forced-colors/reduced-motion settings and text zoom remain untested. Native anchor-positioning fallback is authored but not cross-browser validated. No real map provider, search service or enhanced consumer runtime is claimed.

## Implementation checklist

- [x] Adopt existing Tide recipes without public component/interior overrides.
- [x] Preserve original events, venue facts, paths and unaffected application documents.
- [x] Verify native journeys, focus, responsive layouts, theme pairs and performance budgets.
- [x] Update Lineup's independent version, ownership, runtime, route/asset docs and checks.
- [x] Keep the standalone prototype and HTMX project separate; Tide remains read-only.

---

## Prior completed spacing review (historical)

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
