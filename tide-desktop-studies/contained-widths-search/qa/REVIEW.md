# Contained · Width & Search · verification

2026-10-23. Live local HTML tested in the ChatGPT in-app Chromium browser. Firefox and Safari were not runtime tested during this iteration. All new product CSS is composition of the already-supported grid layout; original component appearance and fallback behavior remain inherited.

## Width and search comparisons

All nine combinations were measured at 1440 × 900. The search button retained the kit's 48px control height throughout. Moving it below added exactly **56px** to the field: the original 48px button track plus its 8px gap. Both below arrangements use the existing 12px spacing token between rows, adding 60px to the search area overall. This intentionally trades vertical space for a wider query field; Apply remains pinned outside that scroll region.

| Maximum | Open filter/list column | Event width | Inline field | Field with button below |
| --- | --- | --- | --- | --- |
| 1216px | 286px | 596px | 172px | 228px |
| 1280px | 302px | 628px | 188px | 244px |
| 1344px | 318px | 660px | 204px | 260px |

The compact button measured about166px in each; the full-width button matched the field. Source type, padding, targets, colors and radii are unchanged. Small fractional measurements reflect the browser rendering scale and scrollbar geometry.

All three widths were additionally measured open and closed at 1200 × 600 and1920 × 1080: twelve endpoint states. At1200px the maximum widths correctly converge to available space. At1920px they retain their respective maximum widths. Closed list/event halves remain equal. There was no horizontal document overflow in any of the21 desktop measurements. The list ended48px above the viewport bottom; the pinned Apply dock aligned with that bottom in every state. The sticky header stayed at y=0.

## Responsive preservation

Compared all three versions to preserved Contained at390 × 844 (list and standalone event),1024 × 768 and1199 × 800: twelve cases. Header, list, event, intro, photo and title geometry matched within0.1px. All original inputs remained singular; mobile/tablet returned to the original inline icon-button layout and hid the comparison-only visible text label. No horizontal overflow occurred.

The gallery's viewport selector was also switched to1024px and back to1440px. The button modifier returned to icon at tablet width and to normal text-button at desktop, without replacing the controls.

## Function, focus and gallery

- Enter in the compact-layout field submitted query “Ink After Dark”, inclusive October24 dates and Workshops together, producing one result and the original GET parameters.
- Clicking its search button with an unmatched query produced zero results. Clear search and filters restored all48. Switching to Desert Frequencies retained the selected compact arrangement.
- The gallery initializes its three previews with filters open using an explicit initial-state hint. It does not focus or synthetically activate the launchers; focus remained in the gallery during initial and lazy loading.
- Layout changes retained a typed, unsubmitted draft. The inline option restored the kit's icon modifier; full and compact options selected the existing normal button. Changing layout respected a manually closed filter panel.
- The shared original/rough/no-photo selector continued to work.
- Node syntax checks passed for all three new/generated JavaScript files.

One unattributed browser-side MutationObserver error was recorded during the first automated frame pass. No shipped project JavaScript uses MutationObserver. It did not recur during the subsequent pass, and no app failure reproduced. This observation is retained in the evidence rather than attributed to an app source without evidence.

## Source and preservation

`source-check.json` covers160 HTML files,13,002 local references and159 unchanged component-document comparisons after removing declared private additions. IDs, labels, BEM ownership, generated scripts and tokens pass. `browser-check.json` records the measured assertions; raw observations are in `browser-evidence.json`.

The complete preservation chain passed, including the maintained app980 files, kit180 files, all123 Sliding Filters files and all188 Reading Widths files. Contained and its archive remain byte-identical. The root preference record now identifies Contained as the preferred constrained direction, while leaving the new comparison winner unset. The UI kit was not modified; this is a documented composition of existing components.
