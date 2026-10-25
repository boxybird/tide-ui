# Quiet Assembly — design QA

final result: passed

## Findings

No actionable P0/P1/P2 findings in the final comparison. The intentional list changes implement the latest feedback: zero gaps, clearer dates, and sans serif type. The event openings preserve the first collection exactly at the reference size.

## Sources and normalized comparison

- Primary source: `../refinements/qa/01-list.png`, `01-event.png`; corresponding 04 and 06 captures for DM Sans and Instrument Sans.
- Implementation: `qa/01-list.png`, `01-event.png`, and matching 02/03 captures.
- Viewport and screenshot: 390×844 CSS px / 390×844 image pixels, scale 1. No density resizing before comparison.
- State: list at its start, opened Ink After Dark at its start, same photograph and fictional event content.
- Full comparison: `qa/source-comparison.png` combines each old pair with its new pair, at the same native size.
- Focused typography/photo/facts comparison: `qa/type-comparison.png` uses identical 390×300 crops. Native 320px list captures and the short event capture were also inspected.
- Gallery evidence: `qa/01-pair-desktop.png`; three-pair overview: `qa/three-pairs.png`.

## Required fidelity surfaces

**Fonts and typography:** Manrope, DM Sans and Instrument Sans are the original local variable font files. All three use 24px/32px card titles and 36px/40px opened titles; no serif or editorial face is loaded. Date numerals use 26px/32px or 32px/36px with smaller supporting weekday/month labels. Names wrap naturally at 320px, including the reserved date corner. No truncation or synthetic bolding.

**Spacing and layout:** The compact header, category/title/venue order, 24px or 28px edges and 4px spacing scale come from Quiet Studies. Cards have zero separation, verified from actual adjacent bounding rectangles. The narrow date rail and date-corner reservation are intentional variants. Brand link hit area expands without shifting the original wordmark. All measured phone anchors are at least 44px in both dimensions; the main action is 48px high.

**Colors and tokens:** The three palettes match Quiet Studies 01, 04 and 06. The same dark dot surface and warm accent remain. Eight targeted contrast combinations per variant pass 4.5:1; minimum 6.10:1. This includes conservative first-photo-text checks using a white underlying pixel. Short-height event openings add a content-anchored reading scrim. These are targeted checks, not a full accessibility certification.

**Image and asset fidelity:** The workshop photograph, object positioning, normal-height overlay, icon SVGs and dot texture are unchanged assets. The original full-screen event opening screenshots and new screenshots are pixel equal for all three corresponding variants, recorded in `qa/event-fidelity.json`. No new generated images or approximate asset drawings were needed.

**Copy and content:** The exact three events and their useful card facts remain. Every opened listing includes the original description, materials, schedule, practical guidance and arrival details below its opening viewport. At 390×844, the long-form article starts at y=844 in every variant. Event facts remain fictional design content, disclosed in the longer listing.

## Browser checks

- Six native frames at 390×844: no horizontal overflow, clipping or browser scripts. All event heroes are 844px high.
- The same six frames at 320px and 430px: twelve additional checks, no overflow or clipped text. Long names wrap without colliding with dates.
- Three event openings at 390×667: no horizontal overflow or clipped text. Their hero grows to approximately 683–695px so content can scroll naturally. A minimum 86% content scrim protects the first line independently of the global image gradient.
- Gallery at requested widths 1440, 960, 768, 436 and 320: no page or caption overflow. Actual client widths are recorded; artboards remain 390px where space allows and stack on narrower canvases.
- Ink After Dark opens from the card. The close/return links return to its matching list. The detail link scrolls to the fuller listing, observed near y=20 after scrolling. Keyboard Enter also opens the card link.
- Browser warning/error logs checked. The server is bound to loopback only.
- Reduced-motion and higher-contrast CSS branches retained. OS preference simulation and a screen-reader session were not part of this pass.

## Comparison history and implementation checklist

The first final native comparison found no substantive mismatch. All three event openings match the selected first-family counterparts pixel for pixel. Date placement, contiguous cards and date scale are expected list differences requested by the user.

- Complete: three pairs and six standalone HTML frames.
- Complete: normal-height full-screen photo opening, with richer details below the fold.
- Complete: zero-gap cards, three prominent-date arrangements, sans serif typography.
- Complete: native, narrow, wide, short-height and gallery review.
- Complete: local assets/fonts/licenses, readable source and portable archive.

## Follow-up polish / scope limits

No additional polish is required for this static comparison. Bookmark marks, Saved and the first two events are visual references; the workshop path and detail anchors work. Booking and persistence are outside this requested HTML study. Earlier collections remain unchanged. The next design choice is which of the three date placements to refine.
