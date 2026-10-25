# Still Hours — design review

Reviewed 2026-10-21 against the user’s request for a second dark family of six small refinements, clearly distinct from Quiet Studies.

## Result

Six static pairs completed. The family change is visible in a direct comparison: warm charcoal, serif-first hierarchy, a larger weekend header, date rails, continuous ruled cards and a price/action row with an outline control. Within the family, anatomy and content stay fixed while type, optical sizing, inset and tone vary.

## Browser evidence

- All 12 frames at 390×844: no horizontal overflow, no clipped text, zero browser scripts. Every event hero is 844px high. Actual phone controls and links meet a 44px minimum height; the primary action is 48px.
- All 12 frames at both 320px and 430px: 24 additional checks, with no horizontal overflow or clipped text. Long card titles wrap naturally at 320px.
- All six event openings at 390×667: no horizontal overflow or clipping. Content may make the hero slightly taller than the viewport; its reading surface follows the text. The Hushed hero grows to approximately 675px.
- Gallery checked at requested widths 1440, 960, 768, 436 and 320. Actual client widths are recorded. Desktop pairs remain 390×844; smaller canvases stack the frames. No page overflow.
- Ink After Dark card-to-event link exercised in the browser. Plan this evening scrolls to the full details. The return link goes back to the matching list.
- Full-length screenshots captured for all six event pages. Long-form description, inclusions, schedule, good-to-know and arrival sections are present.

## Contrast and type

Seven targeted combinations per study pass 4.5:1. The lowest is 7.10:1. This includes secondary text and a conservative white-photographic-pixel check using only the 94% content-anchored scrim. It ignores the additional photographic shade.

The scrim is anchored to `--photo-reserve`, the same value as the content’s top padding. This avoids depending on the first text appearing at a fixed percentage of a tall hero. Type uses real variable fonts and explicit line boxes; no synthetic bolding. Font files and licenses are local.

Contrast calculations are targeted checks, not a full accessibility certification. Reduced-motion and higher-contrast CSS branches are present; OS accessibility preferences were not changed for testing.

## Visual review

Reviewed the six-pair contact sheet, a native-size old/new family comparison, the first pair on the desktop canvas, 320px list/event crops, the shorter event viewport and the longer listing. Shared edges, rule placement, title wrapping, date rails, control proportions and image crop were checked. The original image is identical across all studies and both families.

## Evidence files

The workspace `qa/` folder contains native screenshots, full event screenshots, narrow-phone samples, gallery samples, `six-pairs-contact-sheet.png`, `family-comparison.png`, browser metrics, contrast calculations and structural validation. The ZIP includes the contrast source/results and this report; large QA screenshots remain in the workspace.

## Scope

Static HTML/CSS studies. The first two event cards and bookmark/Saved marks are visual-only. The workshop link and detail anchors work. No booking, save state, server data, application runtime or browser JavaScript is included. Earlier prototypes and Quiet Studies remain unchanged.
