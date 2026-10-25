# Half Split · List Rhythm

Open <http://127.0.0.1:4187/list-rhythm/index.html> to compare three refinements of the preserved Pinned Apply layout. **Lineup** is the selected favorite and now carries its heading hierarchy through desktop, tablet and mobile; Calendar and Month Index retain their original desktop treatments.

1. **Lineup** makes the live result count the column heading. The month and its count remain a quieter sticky anchor.
2. **Calendar** leads with the month, a separate year, and the existing neutral Badge for the month count. Total results and ordering are secondary.
3. **Month Index** gives each month a real numeric marker, echoing Date Line's prominent dates. The year, count and month navigation remain beside it.

All three use the same 48 events, cards, controls, Half Split widths, Bumble Dark tokens and sticky header. These are private desktop composition studies, not changes to the maintained UI kit. Earlier studies, the app and the kit are preserved.

Prior refinement (1.0.1): Lineup's Apply dock has one additional 8px spacing step above the controls (24px total), giving the actions more room while preserving their bottom alignment and the 48px viewport gap. Evidence is saved as `qa/lineup-spacing-1.0.1.*`, and the source release is `dist/list-rhythm-1.0.1.zip`. This spacing remains in the responsive refinement.

## Lineup's responsive heading recipe · 1.1.0

Both the introduction and results summary use the same private `tide-feed-study__heading` composition, an explicit one-column grid with 8px gaps. Their titles share `tide-feed-study__heading-title`, consuming the existing page-size, leading, weight and tracking tokens. Direct child margins are reset by the composition, so a heading's built-in margin cannot add to the grid gap. Supporting copy retains the approved introduction's 12px/24px metrics in both columns. No arbitrary positional offset or new primitive is needed.

At the top of the desktop panels, Albuquerque and The lineup share the same text row; Coming up. and 48 events share the next. The original mismatch was the summary's 4px gap versus the introduction's 8px title margin. Both now use the same spacing source.

The Lineup eyebrow is real HTML before the existing live result count, so it remains present on tablet, mobile and without JavaScript. The count remains the original status node and is updated by the preserved search helper. Lineup's heading and month styles apply at every width; the composition script keeps its month/year and query formatting mounted when resizing. Search/filter placement, card markup, mobile event navigation and desktop docking remain owned by their existing adapters. The comparison picker now includes mobile and tablet sizes.

The 1.0.0 and 1.0.1 source archives preserve the previous versions. This remains an isolated app-composition study; the maintained kit is untouched.

## Spacing and alignment

The top gap stays at the existing spacing token: 24px below the header. The bottom gap becomes twice that token: 48px. Both left panels use `100dvh - panel top - bottom gap`, so they remain bounded by the viewport while the right event follows the natural document scroll. The list keeps this height for one result and empty results, too; it does not shrink away from the dock alignment.

The Apply/Clear action row remains docked outside the filter-options scroller. Its lower padding is removed so the **controls' bottom edge**, the filter panel bottom and the event-list bottom align. The dock keeps its inline inset and neutral separator; Lineup uses the refined 24px upper space. No outer panel frame is added.

The original Results top rule and sticky month header bottom rule are removed in these studies. Card-to-card separators remain unchanged. The larger sticky headings measure their actual height with ResizeObserver and feed that value into the list's scroll padding to keep keyboard targets visible.

## Component ownership

`list-rhythm.css` owns only private `tide-feed-study` classes and the preceding private action dock. All type sizes, spacing, weights and colors consume existing semantic tokens. It does not redefine shared kit tokens; it overrides only the preceding study's private panel-height variable. No new font family, color palette or kit component is introduced.

`headings.js` composes the original live result-count node and original month H3/count nodes after the preserved search helper runs. Their IDs, status semantics, count values and month jump links stay intact. The numeric month is decorative (`aria-hidden`); the accessible month heading still contains the month, year and result count. Calendar reuses the existing `tide-badge` class.

For Calendar and Month Index, the adapter restores the original heading text nodes below 75rem/1200px. Lineup now retains its selected heading hierarchy at every width. The smaller layouts keep the approved search/filter placement and components. This script handles composition only; native GET search, inclusive dates, categories, validation, empty states, clear actions and event navigation remain owned by the preserved app.

## Build and preservation

Run from this folder with Python's `-B` option:

```text
python -B tools/build.py
python -B tools/build.py --check
python -B tools/check.py
node --check headings.js
```

Use the existing parent preview server on port 4187. Do not run parent, app or kit writers. `tools/context.py` checks all previous source archive hashes and locked source inventories before and after work. This folder depends on its preserved siblings and the adjacent app; its source release is not a standalone application distribution.

## Responsive 1.1.0 verification · 2026-10-22

At both 1200 × 800 and 1440 × 900, the desktop eyebrow rows start at y=141 and both title rows at y=165, with identical 16px eyebrow and 36px title line boxes. Supporting text starts at y=209 in both columns. At 1440 × 900, the list and Apply controls still end at y=852. The normalized heading composition preserves the original introduction/search geometry.

The same Lineup eyebrow, 28px/36px title and 8px gap were checked at 1024 × 768 and 390 × 844. Resizing between mobile, tablet and desktop retains exactly one Lineup label and one result status node. Combined date/category filters produce one result, a nonmatching mobile query produces zero, and clearing restores all 48. Query text stays at caption size. Mobile November navigation retains the month/year and correct 32-event count. No horizontal page overflow was observed at the checked sizes.

All 160 HTML pages pass source/reference checks, and JavaScript syntax passes. The 159 product documents match the preserved generator after removing the declared private classes, references and Lineup label. All 106 Calendar and Month Index HTML files are byte-identical to 1.0.1. Original app/kit/study inventories and the 1.0.0/1.0.1 archive checksums pass. The maintained UI kit is untouched.

Evidence is saved as `qa/lineup-responsive-*-1.1.0.*`. The source release is `dist/list-rhythm-1.1.0.zip`. Browser verification used the in-app Chromium, with the same Firefox/Safari execution limits as the earlier check.

## Original 1.0.0 verification · 2026-10-22

All 160 HTML pages pass the source and reference checks (12,355 local references). After removing only declared private classes, data attributes and stylesheet/script references, the 159 product documents match the preserved Pinned Apply generator. JavaScript syntax passes. Preservation checks cover 185 original desktop-study files, 177 width-study files, 177 prior refinement files, 980 app files and 180 kit files. No kit component was added or edited.

Rendered checks used the in-app Chromium browser. At 1440 × 900, the header remains at y=0, both left panels start at y=117, and the panels and Apply controls end at y=852. This keeps the original 24px top gap and creates the requested 48px bottom gap. The 1200 × 800 and 1920 × 1080 checks retain the Half Split tracks and the same 48px bottom clearance, without horizontal page overflow. Scrolling the right document to its end leaves the header and left panels in place; scrolling filter options leaves Apply available.

The November boundary was checked at the narrow desktop width, including the longer month name, the 11 marker, count and navigation. Combined November 12 date/category filters produce one workshop; a nonmatching query produces zero results; clear returns all 48. Both one-result and empty lists retain the same viewport height and dock alignment. A long query wraps in caption-sized supporting text instead of becoming an oversized heading.

At 390 × 844 and 1024 × 768, header, list and first-card geometry match the preserved baseline exactly. Desktop-to-tablet restoration removes the composed headings and dock in all three variants. Calendar remounts without duplicate counts, badges or Apply controls.

The comparison page provides three working HTML frames and 1200/1440/1920 preview-size controls. Screenshots were saved and inspected. Raw observations, including the sparse-list issue before correction, are in `qa/browser-measurements.json`; source results are in `qa/source-check.json`. Firefox and Safari were not physically run in this pass. Native control, focus and reduced-motion behavior remain inherited from the preserved app.

Saved source release: `dist/list-rhythm-1.0.0.zip`, with an internal file manifest and adjacent SHA-256 checksum. The earlier source releases remain unchanged.
