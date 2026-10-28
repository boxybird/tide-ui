# Compact headers · design QA

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

final result: passed
