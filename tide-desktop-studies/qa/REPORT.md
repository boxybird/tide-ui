# Wide Open verification · 2026-10-22

Three isolated desktop compositions use the same approved Bumble Dark components. No change was made to the maintained kit or the current app. The study is saved separately, with complete preservation hashes for both originals.

## Source verification

- **980 original app files and 180 kit files remain byte-identical**, including their documentation, generated files, existing QA and archives. The kit inventory is a subset of the app inventory.
- All **160 study HTML pages** pass source checks: 159 product documents and the comparison page. The 159 product documents match the approved generator after removing explicitly declared study classes, stylesheet links and Workbench's empty tools slot/adapter.
- **11,478 local references** resolve. Static checks cover landmarks, heading presence, duplicate IDs, form associations, label/description bindings, inline handlers and registered component ownership.
- Product composition CSS does not redefine shared tokens, colors, typography, borders or component selectors. There are **zero new kit components**.
- Generated HTML freshness and the three JavaScript syntax checks pass. Checks run against the study only; original build/QA commands are not invoked.

Machine-readable results: `source-check.json`. Full app/kit inventories are in `../locks/`.

## Browser checks

Performed in the Codex in-app Chromium browser, using real HTML pages and native controls. Measurement data is saved in `browser-measurements.json`.

| Viewport | Result |
| --- | --- |
| 390 × 844 | All three studies match the original header, results, first-card and control measurements; no horizontal overflow |
| 834 × 1112 | Same approved tablet layout and component measurements; no tools rail |
| 1024 × 768 | Same approved landscape/tablet composition, list sizing and closed filter state |
| 1280 × 800 | Three desktop layouts fit; list ends at 776px, leaving 24px below; Open Book photo uses normal flow |
| 1440 × 900 | Three compositions reviewed visually; list ends at 876px; outer results and detail border widths are zero |
| 1920 × 1080 | Three wide compositions reviewed visually; no horizontal overflow; list ends at 1056px |

Panorama gives the photo the remaining width while keeping a bounded text measure. Workbench separates original search/filter nodes from the feed. Open Book shows the original photo opening and story alongside each other; the story remains in normal document scrolling. Its opening becomes sticky only from 896px height, leaving long event titles accessible in shorter windows.

Workbench verification includes keyword search, combined date/category filtering to one result, no results, clearing all filters, invalid reversed dates with the disclosure closed, and retaining an unsubmitted query/date and input focus when resizing to tablet and back. Native date validation reveals the moved disclosure and focuses the invalid field.

A list-position shift discovered during event switching was corrected in the study adapter: it records the restored list offset before moving the controls and reapplies it instantly after the final layout. The corrected navigation retains the 2826.67px feed offset and shows the selected November event. The shared app navigation helper remains unchanged. Earlier diagnostic measurements are retained in the JSON with explicit pre-fix labels.

Switching from a deep reading point to another event returns the document to the top; browser Back restores the prior event and its reading point (1510px document scroll and 3011.33px feed scroll in the recorded run). No browser console warnings or errors were recorded in the test tab.

The comparison page uses live HTML iframes. Its viewport selector switches all three to 1920 × 1080, updates the labels and fits the previews without outer horizontal overflow. Individual Open links use the actual browser width. The original mobile/tablet composition returns below 1200px.

## Evidence

- `baseline-current.png` — preserved current app
- `panorama-1440.png`, `workbench-1440.png`, `open-book-1440.png`
- `panorama-1920.png`, `workbench-1920.png`, `open-book-1920.png`
- `open-book-long-title-1280.png` — longest-title fixture in a short laptop window
- `comparison-overview.png` — complete comparison page

The screenshots were saved and visually inspected. These are layout studies with the baseline's sample data and disclosed placeholder actions. No bookings, submissions or external services are added. Firefox and Safari were not physically run; this is not a cross-browser certification or a full accessibility audit. The existing kit's appearance, labels, focus styles and reduced-motion behavior are inherited, not reimplemented.

## Saved release

`../dist/wide-open-desktop-studies-1.0.0.zip` contains the study source, generated pages, locks and evidence. Every archived file is checked against its source hash, and a separate archive SHA-256 is saved. It depends on the adjacent preserved `tide-responsive-app` directory; the original project and its versioned archives are not repackaged or edited.
