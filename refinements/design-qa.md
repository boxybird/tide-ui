# Quiet Studies — final design review

final result: passed

Completed 2026-10-21, America/Denver. Six static HTML/CSS refinements; no browser JavaScript or app framework.

## Visual target and evidence

- Source concept: Pocket Nights 3 / Pocket Texture, especially Ink After Dark. Source mock: `../research/concepts/pocket-nights/03-pocket-texture-refined.png` (1327 × 1185). Earlier rendered app evidence: `../burque-pocket/qa/list.png` and `../burque-pocket/qa/detail.png` (393 × 852).
- User-authorized changes: carefully varied fonts, optical sizing, spacing and dark tonal palettes; same two-frame anatomy and original workshop image. Static HTML explicitly replaces app runtime and device chrome for this task.
- Actual browser captures: `qa/01-list.png` through `qa/06-list.png`, and `qa/01-event.png` through `qa/06-event.png`. Each is 390 × 844 pixels at a 390 × 844 CSS-pixel viewport. No transforms or physical phone masks are used. The browser returns one image pixel per CSS pixel for these captures; no separate display-DPR claim is made.
- Full-view comparison: `qa/six-pairs-contact-sheet.png` (2424 × 1824), composed from the twelve browser screenshots. `qa/source-comparison.png` places the earlier list/detail and refinement 01 together in the same input; original status/home regions are cropped, with source aspect ratio preserved. Remaining height differences are intentional after removing device chrome.
- Focused typography comparison: `qa/type-details.png`, with native-width card and detail text regions from all six versions. Reviewed type shapes, weights, wrapping, secondary values, date/time punctuation, baseline alignment and price hierarchy.
- Full listing captures: `qa/01-event-full.png` through `qa/06-event-full.png`. These include the richer content beneath the photo.
- Presentation evidence: `qa/01-pair-desktop.png` and `qa/gallery-narrow.png`. The desktop browser viewport was requested at 1440 × 1200; client width is1425 after the native page scrollbar, and the screenshot API returns1425 ×1188. Both iframe rectangles measure390 ×844 CSS px. Native phone captures, rather than this wider canvas, were used to judge fine typography.

## Findings and fixes

1. **P2, fixed — mismatched frame width.** Initial desktop review showed a reserved scrollbar narrowing the event document relative to the list. Screens now scroll without reserving that gutter. Final iframe measurements and raw captures show equal390px phone widths.
2. **P2, fixed — weak small text on the presentation canvas.** Early gallery caption colors were approximately4.24–4.30:1. Darkened the supporting gallery labels/links to meet4.5:1. This affects the presentation canvas, not the dark mobile palettes.
3. **P2, fixed — photo readability needed a stronger margin.** Increased the functional scrim before the first small text. A conservative white-photo-pixel calculation now gives at least6.10:1 for the checked photo eyebrow across the six studies. The chosen photo is darker there. This is a targeted stress check, not full accessibility certification for arbitrary future images.
4. **P2, fixed — irregular eyebrow and mixed-size fact rhythm.** Replaced the inline eyebrow with an explicit16px block line box. Year and duration now use the same optical size as their fact row, differentiated by tone. Admission uses a32px line region. Final native geometry lands on the shared4px rhythm: versions01/02/04/05 have eyebrow428, title452, and action bottom768px; the serif version uses424/448/768; the airier version uses416/440/764. Those differences correspond to its declared type/spacing tokens.
5. **P2, fixed — full-width keyboard focus outline.** A positive offset would extend the card-link outline beyond the viewport. The full-card link now uses an inset outline; keyboard Tab reaches it and the browser reports the visible2px ring. Other action and close targets remain at least44px.
6. **Implementation correction — preference cascade.** Put theme values in a declared cascade layer, so the later higher-contrast state can override them. Protected app-runtime files were not changed.
7. **Final content correction.** Kept the year attached to the date with a comma and separated duration with a middle dot. Rebuilt all six event documents, recaptured their full/photo states, and rechecked them at320px. All fact lines remain24px high and all actions fit the first viewport.

No actionable P0/P1/P2 findings remain.

## Required fidelity surfaces

### Fonts and typography

Seven local WOFF2 files supply six title families and the limited Plex Mono labels. Real variable weights, `font-synthesis:none`, optical sizing and explicit title line boxes are used. Manrope, Source Sans3, Newsreader/DM Sans, DM Sans, Plex Sans/Mono and Instrument Sans are visibly distinct in the native focused comparison. Source Sans is optically larger; the serif keeps a lighter weight. Running text remains proportional, while dates/times/prices use tabular lining numerals. No clipped titles, facts or metadata were found.

### Spacing and hierarchy

A shared4px spacing scale, semantic token sets, consistent horizontal edges, clear local versus sectional gaps, and common event anatomy keep the variations comparable. Cards are edge-to-edge and carry only summary data. The photo fills a viewport and continues into additional event information. At narrow sizes, content wraps rather than truncating. Six native pairs, twelve raw frames, and the gallery’s stacked layout are all usable.

### Colors and contrast

Near-neutral dark bases, subtly lifted panels, off-white primary text, distinct secondary values and a restrained warm accent stay within the source direction. Critical title, secondary, label, accent, action and modeled first-photo-text checks all exceed4.5:1; current minimum is6.10:1. `qa/contrast-results.json` records each check and its assumptions. Gallery captions were checked separately. Decorative lines and texture are not being presented as text-contrast checks.

### Imagery and icons

All six use the exact same existing workshop PNG, identical viewport geometry and `object-position:50% 38%`. No new idealized event photography was substituted. The original quiet dot PNG is reused at controlled opacity. Radix library SVGs are used consistently, with its MIT license included. Font licenses are included. There are no handcrafted substitutes for imagery or icon assets.

### Copy and content

The same three cards and Ink After Dark facts are present in every version. The event adds subtitle, duration, materials, description, inclusions, schedule, guidance and arrival information beyond the card. Dates remain plausible upcoming mock dates relative to the original brief. No inaccurate generated street address was introduced. Fictional-event disclosure appears below the listing. Static bookmark marks and Saved text are identified as visual study content in the notes.

## Browser and structural verification

- Native390 ×844:12 frames checked and captured.
-320/430px phones:24 responsive checks, no page overflow, clipped text or action extending below the initial hero. `qa/responsive-metrics.json`.
- Final event punctuation:6 additional320px checks; all three fact rows remain24px and no clipping. `qa/final-event-checks.json`.
- Gallery at requested1440/960/768/436/320px widths: measured client widths1425/945/753/421/305 because of the browser’s page scrollbar. Correct paired/stacked layouts, no horizontal overflow. `qa/gallery-metrics.json`.
- Keyboard focus, full-card HTML navigation, ordinary detail-anchor navigation and the design-notes link verified in the browser.
- Design notes list all six variants; no scripts and no horizontal page overflow.
- Download link exercised; portable ZIP contains57 static delivery entries and passes CRC validation. Archive rebuilt after final corrections.
- Source validation:20 HTML documents,12 standalone frames,7 valid local WOFF2 files, no duplicate IDs, missing embedded resources, broken local links or script tags. `qa/validation-results.json`.
- Final browser console review returned no warnings or errors.
- Hidden local static server is running on127.0.0.1:4175. It remained available through the overnight session. No deployment or external publishing occurred.

## Limits / follow-up polish

- Browser review was performed in the desktop in-app Chromium surface with phone viewports, not physical iOS/Android hardware or every browser engine.
- OS higher-contrast and reduced-motion settings were not changed. Their CSS branches are present; reduced-motion limits smooth anchor scrolling.
- The font sizes and palette decisions are six considered alternatives, not a claim that a particular spacing scale is universally optimal.
- A future production event feed should be checked against much longer submitted titles and arbitrary photo crops. This delivery intentionally holds content/image constant for a fair refinement comparison.
- No additional P3 work is required for the agreed static studies.

## Completion checklist

- [x] Six subtle, named HTML/CSS refinements with two matched frames each.
- [x] Original image/content and dark concept preserved.
- [x] Local fonts, reusable semantic CSS, readable source and licenses.
- [x] Source/implementation and focused comparisons reviewed.
- [x] Findings fixed and post-fix browser evidence captured.
- [x] Portable archive, design notes and local preview ready.
