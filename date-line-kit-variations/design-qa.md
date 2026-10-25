# Design QA — Date Line appearance studies

final result: passed

Date: 2026-10-22. Source is the approved static UI kit at port4182, not any motion experiment. New collection at port4183: Date Line reference, Daybreak, Tide and Lift. The user explicitly permits palette/radius/elevation variations while freezing all component primitives and screen inventory.

## Findings resolved

- P2: adding the appearance picker made the sidebar slightly taller than a 720px window. Tightened only the comparison footer leading/margin. Re-captured the final Daybreak components view; sidebar clientHeight and scrollHeight both measure 720px. App component dimensions were never changed.
- P3 visual refinement: Daybreak's first card texture pass darkened the warm card too far. Reduced its overlay opacity from .10 to .035, keeping the same texture asset and placement. Revised search capture shows the intended warm-white event surface with the original anatomy.
- The source's hardcoded selected-state colors, status borders, icon paint and radii required complete theme coverage. Each is mapped in skin.css; the six source stylesheets remain byte-identical. Dark photo surfaces use their own fixed readable foreground tokens, so Daybreak does not put dark type on a dark scrim.

## Source-grounded comparison

Opened the live source and each rendered kit in the in-app browser. `qa/compare-search.png`, `compare-states.png`, `compare-01-event.png` and `compare-review.png` combine the actual source and three implementations in the same image at native 390×844 CSS/image pixels. Inspected these together, including readable metadata, input text, status words, photo crop and controls. The desktop component boards were also captured at the same default browser size. The source column is not expected to share palette/radii/shadows with the new skins; those are the requested variables.

`qa/layout-390.json` contains the source + four kits × 11 screen/state pages (55 views). `qa/invariance.json`: zero differences in body text or the measured component bounds, type family, size, weight and leading. `qa/fixture-lock.json`: all 44 normalized frame bodies match the source, excluding only asset-path rebasing in the normalization. `qa/reference-pixels.json`: source and neutral reference captures are pixel-identical for search, form, status, event opening and review.

Five required fidelity surfaces:

- Typography: Manrope throughout, same family/weights/sizes/leading/tracking and wrapping. Page, card and event hierarchy unchanged. No new font.
- Spacing/layout: same insets, 4px rhythm, touching cards, 44/48px targets, widths and heights. Corners intentionally differ. Shadows in Lift alter paint only.
- Color/tokens: deliberate Daybreak light/plum, Tide navy/teal/square and Lift lavender/raised systems. Palette swatches and radius documentation reflect each skin. Checked normal body/accent/status text and control boundaries numerically; weakest normal text sample is Daybreak tertiary at 5.02:1 on canvas, weakest field boundary is Lift at 3.64:1. See structural-checks.json. This is not a full contrast audit of every photo pixel.
- Images/icons: original local dot texture, photo, font and Radix icons retained. Identical image crop/scrim and hero geometry. Daybreak icons are recolored through CSS filters; photography is not recolored. Photo openings deliberately retain a dark contextual surface in every kit.
- Copy/content: identical app fixture text, form labels, dates, prices, empty/recovery/confirmation states, coverage table and inventory. Only documentation swatches, appearance names, radius values and explanatory comparison text vary.

## Responsive/native checks

- 390px: 55 views; no horizontal overflow.
- 320px: all four kits × 11 app pages plus four library pages (48 views); no horizontal overflow or unlabelled form controls.
- Appearance links tested between Daybreak/Tide/Lift with #components and #screens preserved. Hidden alternate anchor groups are not in the tab order. This is selected-section retention, not automatic scroll tracking.
- Daybreak filter checkbox/reset returns to the original defaults; the remaining behavior is unchanged native HTML from the source. No browser JavaScript, backend, live filtering or submissions introduced.
- 52 HTML files, 983 local references, no missing local resources, zero script tags. Shared source CSS hashes match. Temporary viewport override reset before handoff.

## Limits

Desktop in-app browser verification only. No physical-device, screen-reader or cross-browser conformance run. Native checkbox/radio geometry is preserved and may vary by browser. Disabled controls retain the source's lower-contrast treatment. This is a controlled visual comparison, not a production application. The original source kit and all previous collections remain preserved.

## Subsequent user-requested change

2026-10-22: Tide was selected as favorite. Its colored left callout stripes were removed with a neutral uniform outline; body text position and geometry remain identical. Earlier Tide status captures retain the pre-change appearance for historical comparison. Current before/after evidence and QA: ../tide-ui-kit-studies/design-qa.md. Other kit styles were not changed.
