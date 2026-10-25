# Date Line — In Practice: design QA

final result: passed

## Findings

No actionable P0/P1/P2 findings remain. The approved Date Line is preserved. Advertising changes are confined to the inserted placements and their neighbouring raster edges; the poor-photo change is confined to the image and a below-fold credit.

## Source, state and normalized evidence

- Selected source: Quiet Assembly 01 Date Line, now the user's favorite layout overall.
- Approved visual truth: `qa/approved-list.png`, `qa/approved-event.png`, copied from the approved collection.
- Approved source documents: `source/approved-list.inc`, `source/approved-event.inc`.
- Rendered implementation: `qa/baseline-list.png`, `baseline-event.png`, `local-partner-list.png`, `local-partner-event.png`, `rough-upload-list.png`, `rough-upload-event.png`.
- Viewport: 390×844 CSS px; each screenshot 390×844 pixels, scale 1. No resizing before equality checks.
- State: list at the top; event at the top; same title, date, facts, controls and action. `local-partner-event-scrolled.png` shows the intentional below-fold ad.
- Combined full-view comparison: `qa/source-comparison.png` places approved and changed states in the same image. `qa/practical-elements.png` shows the list ad, scrolled event ad and bad-photo opening.
- Focused checks: isolated native card crops, foreground rectangles/type/color, and `qa/preservation-results.json`. Individual native screenshots were opened to inspect date labels, title rhythm, ad disclosure, control alignment and photo contrast.

## Preservation results

At 390×844, the following are pixel equal to the approved original:

- Preserved baseline list.
- Preserved baseline event opening.
- Rough Upload list.
- Local Partner event opening.

All three cards in the advertising list retain their original dimensions and pixel-identical content/surface interiors. The third card moves down exactly 144px for the inserted slot. The first card is fully pixel equal. Changing the neighbouring panel creates raster-compositing differences only in five bottom padding rows of card 2 and three top edge rows of card 3. These are recorded explicitly, rather than claiming whole-crop equality. No type, date, icon or content pixels change within those cards' interiors.

The Rough Upload foreground has exactly the same measured geometry, font family and text color as the baseline. Its photograph is intentionally different; its existing scrim remains.

All 21 locked approved source/copy hashes match, including the original two documents, five stylesheets, selected font, photograph, texture and icon files. The original project files have not been edited.

## Required fidelity surfaces

**Fonts and typography:** Date Line's Manrope, weights, 24px card names, 36px opened title, line heights, date hierarchy and tracking remain unchanged. Ad copy uses the same family at a smaller 16px headline, 11px disclosure and 12px link. No editorial face or synthetic font styling is introduced.

**Spacing and layout:** Original card insets, dimensions, zero gaps, metadata grouping and full-screen geometry remain. The ad slot reserves 144px and follows the second card. Its link is at least 44px high. The event ad is outside the first 844px viewport, after the workshop introduction. New content grows in document flow and does not overlay existing controls.

**Colors and tokens:** Original tokens and background texture are copied unchanged. The ad uses a quieter #14191c surface, existing neutrals, clear Advertisement labeling and no event date/bookmark treatment. Eleven targeted text combinations pass 4.5:1; minimum 6.62:1. The photographic stress calculation assumes a white pixel under the first small text. These are targeted checks, not a full accessibility certification.

**Image quality and assets:** The approved photograph remains unchanged in the baseline and advertising study. Rough Upload uses one newly generated 1024×1536 fixture with intentionally bad framing, flash and blur; this is expected input variation, not a visual-fidelity failure. It keeps the original object-fit/crop/overlay. The composition remains visibly poor; no upload enhancement or automatic subject selection is implied. Radix SVGs and the dot texture are the approved local assets. The exact built-in ImageGen prompt is in `assets/images/provenance.json`.

**Copy and content:** All existing event facts and rich details remain. Ads are explicitly labelled and name their fictional advertiser. They do not imitate organic events. Ad links lead to a clearly fictional local partner page. A photo credit is added in the Rough Upload's longer listing. No product copy refers to technical quality judgments about the organizer's image.

## Browser checks

- Six native frames: no horizontal overflow, clipped text or browser scripts. All three event openings are 844px high and their details begin at y=844.
- All six frames at 320px and 430px: twelve further checks, no clipping or horizontal overflow. Ad slots remain 144px at the tested narrow size.
- All three event openings at 390×667: no clipping or horizontal overflow. They grow to about 683px to retain the content and use the approved short-height reading surface.
- Gallery checked at 1440, 960, 768, 436 and 320 requested widths. Actual client widths are recorded. No gallery or caption overflow.
- The workshop link opens the matching scenario. The close link returns to its list. The detail link scrolls to the full listing. The partner ad link opens the fictional Morrow Coffee example; its return link leads to the advertising list.
- Warning/error logs checked before handoff. No ad network, remote embeds, tracking, checkout or API is connected.
- Reduced-motion, higher-contrast and focus rules are retained. OS preference simulation and a screen-reader session were not part of this review.

## Comparison history

Initial strict card-crop comparison found boundary-only differences beside the new advertising surface. Inspection isolated them to empty edge/padding rows. The review now records both raw differences and interior equality; it does not hide these changes or alter the approved source to satisfy a screenshot test. The final visual comparison found no substantive design drift. Baseline and unchanged event-opening comparisons pass with zero pixel differences.

## Implementation checklist

- Complete: favorite recorded in project instructions, registry and dedicated favorite record.
- Complete: original preserved, source hashes recorded, baseline comparison available.
- Complete: two additive studies with static links and scrolling details.
- Complete: native/responsive comparisons, contrast, source and archive checks.
- Complete: generated poor-photo asset and exact prompt stored in the project.

## Scope / future decisions

These examples establish ad placement and photo resilience. Production ad frequency, advertiser approval, loading/error states, upload cropping and quality controls remain future decisions. The intentionally poor composition is left visible so the design can be judged honestly. No P3 layout change is required before reviewing these studies.
