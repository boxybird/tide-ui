# Date Line — Continuity: design QA

final result: passed

## Scope and evidence

Visual authority: Quiet Assembly 01 Date Line, the user's favorite overall. Reference copies: reference/baseline-list.html and reference/baseline-event.html. Original collections and practical studies were not edited.

Fresh source captures: qa/source-list.png, qa/source-event.png.
Final implementation captures: qa/implementation-list.png, qa/implementation-event.png.
Combined comparison inspected: qa/source-comparison.png.

Source and implementation viewport: 390 × 844 CSS px. Both PNGs are 390 × 844 pixels, density 1. No resampling or device-frame normalization. Comparison covers the app content itself.

The final unfocused resting list and opened Ink After Dark event both have **zero changed pixels** against their references. Keyboard return intentionally shows a focus outline on the card; that is a separate interaction state.

Focused text/layout checks were made in the combined image at readable scale. Date-row differences were isolated to their bounds and corrected. Intermediate evidence: qa/open-25.png, qa/open-65.png, qa/close-25.png. These are actual native animations paused by the QA checkpoint parameter, not fabricated frames.

## Required fidelity surfaces

- Fonts/typography: Manrope, original weights, sizes, line heights, tracking and wrapping remain. Inline date fragments preserve original glyph positions. A content-sized, single incoming title snapshot avoids double text during resizing.
- Spacing/layout: original tokens, 24 px inset, touching cards, date stamp, title/facts/action positions and full-screen hero remain. At 390 × 844 the article starts below the hero. Short screens retain the source's content-driven minimum height.
- Colors/tokens: shared palette, texture opacity and functional photo scrims unchanged. Motion opacity does not affect resting colors.
- Images/assets: workshop and texture unchanged. Concert/comedy and rough organizer photos reused from earlier prototypes. Existing Radix SVGs and licensed self-hosted fonts remain.
- Copy/content: Ink After Dark content retained. Other cards open coherent fictional details. Lab settings remain outside the app viewport. The prototype does not make reservations.

## Findings and resolution history

1. **P2 resolved — Date-row kerning.** Initial inline-block fragments changed glyph positions. Inline spans preserve snapshot names and source rendering. Post-fix full-event pixel comparison: zero differences.
2. **P2 resolved — Double title.** Old/new snapshots overlapped at different font sizes. One incoming snapshot keeps the title crisp. Inspected final opening/return checkpoints.
3. **P2 resolved — Covered controls.** Expanding photo covered unnamed incoming UI. Independent content/toolbar reveal layers now sit above it. Final 65% capture shows subtitle, fact icons, admission and actions arriving during movement.
4. **P2 resolved — Crossing date/venue.** Released changing abbreviations early and staggered incoming date labels/venue visibility. Final return checkpoint has no overlapping visible text.
5. **P2 resolved — Forward URL.** Base-list history rewriting removed the forward event hash. Restricted that rewrite to explicit navigation. Back/Forward now preserve matching route and rendered view.
6. **P2 resolved — Cropped preview.** Fixed 844 px preview did not fit a short desktop viewport. Preview now fits available height and stays visible as controls scroll. Tested 1280 × 720, with a fully visible 390 × 608 app frame.

No actionable P0/P1/P2 findings remain.

## Interaction and responsive checks

Evidence: qa/journeys.json, qa/responsive.json, qa/lab-controls.json.

- All three cards open matching event/photo.
- Native groups verified: linked elements; only title/root in Title only; only root in Soft dissolve.
- Both opening and return shared movements captured.
- Back, Forward, Escape, close links and the comparison return control work.
- Enter opens a card; return focuses its link.
- Short-phone list scroll restored to the measured 118 px.
- Details scroll below the opening. Off-screen-title return uses dissolve.
- Direct event links load; closing an initial deep link stays in the prototype.
- Saving updates without navigation; saved filtering and empty state work. Test save was removed again.
- Controls reach the iframe; slow mode reports 2400 ms, normal linked 480 ms. Organizer selection changes the Ink photo.
- Forced direct-navigation fallback tested with ?native=off.
- No horizontal overflow at 320 × 740, 390 × 844 or 430 × 932. A 390 × 667 check preserves source content height without clipping.

Automation waits for native movement to settle before the next ordinary tap. Physical rapid-tap/gesture behavior remains a device-testing follow-up.

## Console and accessibility limits

Standalone app warning/error log is empty. The browser tool reports an invalid-Node MutationObserver error on the iframe workbench. Neither supplied script uses MutationObserver, the early page-error listener records no page error, and controls/preview pass. This appears to be an iframe/tooling diagnostic; exposed log fields do not identify its source. It is recorded in qa/final-console.json and is not suppressed or described as a clean workbench console.

Reduced-motion handling is implemented and code-reviewed. Forced direct navigation was tested; the browser tool does not expose OS media-preference emulation. This run does not establish WCAG conformance or physical-phone/cross-browser certification. Keyboard controls retain visible focus. The noninteractive heading receives reading focus without a decorative outline. No swipe-only or motion-dependent navigation.

## Implementation checklist

- [x] Preserve original/practical studies.
- [x] Match resting source at reference viewport.
- [x] Use native API and unique snapshot names.
- [x] Inspect intermediate frames; resolve collisions/layering.
- [x] Verify history, keyboard, scroll/focus and fallback.
- [x] Keep local; run without package installation.

P3 follow-up: tune timing/easing and number of travelling details after user feedback; test actual phones/additional browsers; investigate browser-tool iframe observer diagnostics if they affect later automation.
