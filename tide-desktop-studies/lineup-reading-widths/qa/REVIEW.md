# Reading Widths · verification · 2026-10-23

Tested as live HTML in the ChatGPT in-app Chromium browser at local port4187. This is not a claim of runtime testing in Firefox or Safari. New layout uses container queries/units, grid and `:has`; shared component CSS and browser fallbacks remain inherited. Reduced-motion declarations and the original adapter's preference handling were source checked; the operating-system preference was not changed during this run.

## Geometry

All three versions were measured closed and open at **1200 × 600**, **1440 × 900**, and **1920 × 1080**: 18 states. The list bottom was exactly viewport height minus 48px; the Apply dock bottom matched it. Header stayed at y=0 with its 93px geometry. No horizontal document overflow occurred. Native document scrollbars are included in the measurements; small fractional CSS-pixel differences come from the browser's rendering scale.

| 1440 × 900 | Closed list / event | Open filters / list / event |
| --- | --- | --- |
| Contained | 596 / 596 | 286 / 286 / 596 |
| Give & Take | 390 / 802 | 288 / 390 / 490 |
| Reading Room | 390 / 704 | 288 / 390 / 635 |

At 1920px, Reading Room opens using the outer margins and keeps its event at 704px. At 1200px it yields to approximately 395px, with the photo stacked. Contained intentionally demonstrates the tighter 262px list when filters share half of the small desktop frame.

The event remains natural document scroll. After scrolling its right side 900px, the header, browser, list and Apply dock retained their viewport positions. The list scrolled independently to 1800px. Native coordinate activation of its visible filter launcher and Escape retained that list offset and the document reading position; Escape restored focus to the launcher and collapsed content was inert. Locator auto-scroll can reposition ancestors before clicking sticky controls, so the native toggle check was used to distinguish that automation behavior from the product interaction.

## Responsive comparison

Compared all three with preserved Left at mobile 390 × 844 (both list and standalone event), tablet 1024 × 768, and just below the desktop breakpoint at 1199 × 800. Contained and Give & Take matched header, list, event, intro, photo and title rectangles within 0.1px. Mobile Reading Room also matched. On tablet, Reading Room keeps the list and outer event widths but changes the photo composition as declared: at 1024px the event is 196px taller to fit stacked media. This is an intentional composition difference, not a primitive change.

The live gallery's viewport selector was also switched from desktop to tablet and back. Every frame restored the original controls with exactly one query input and no desktop browser wrapper at tablet width. All six original input nodes remained present without duplication.

## Function and media

- Query “Ink After Dark” + From/Through October24 + Workshops returned one event with the original GET URL and Filters · 2 badge.
- Query “zzzz nowhere” returned zero cards and the existing clear-search-and-filters recovery link. Clearing restored all 48.
- Selecting Desert Frequencies retained its own concert artwork and the Reading Room figure/layout. Returning to Ink After Dark restored the chosen rough capture.
- The same rough capture, original and no-image modes were checked. No image hides its image/figure and removes the empty photo track in Reading Room. Its metadata and actions remain.
- The gallery's no-image choice was made before navigating to the third lazy preview. All three loaded hidden images correctly; rough and original choices then updated their sources as expected.
- Both open and close actions worked inside the gallery. No gallery console errors were recorded.
- Node syntax checks passed for `slide-adapter.js`, `room.js`, and `review.js`.

`browser-evidence.json` contains the raw geometry and UI observations. Screenshots show open/closed desktop states for each version, short desktop, Reading Room tablet/mobile and one/zero results.

## Preservation and ownership

`source-check.json` verifies 160 HTML files, 12,684 local references and 159 component-document comparisons to the original Left generator. The sole adapter change is its session namespace. BEM, labels, IDs, token references, no inline handlers/styles and fixture identity pass. No new kit component or shared primitive change was made.

The guard verifies the maintained app's 980 files and kit's 180 files, plus the preceding study release inventories: 185,177,177,182,176,178 and all123 Sliding Filters files. All previous releases remain byte-identical. The final ZIP is additive and contains only this sibling with a SHA-256 release manifest.
