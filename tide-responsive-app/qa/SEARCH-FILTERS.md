# Search and filter verification · 1.2.0 · 2026-10-22

The approved Tide layout, primitives, palettes and 48-event fixture are preserved. The current local app adds matching, URL/form behavior and existing-kit empty states. Earlier 1.1.0 and 1.0.x packages remain intact.

## Source and behavioral checks

- 38 tests pass: 10 search-rule cases against the committed 48 events, 11 navigation cases, 5 fixture cases, 12 reviewed-kit cases.
- 392 generated HTML documents are current. Source/markup/reference checks pass for 26,817 local references and three registered deferred scripts. Explicit form-owner references are checked alongside labels/descriptions.
- 324 palette contrast pairs pass across all six theme/modes. No palette, typography, space, radius, target or font primitives changed.
- All 176 original kit hashes and 263 frozen 1.0.3 files verify unchanged.

## Rendered behavior

Tested in the Chromium in-app browser using the actual controls and real HTML navigation:

- **One result:** `Ink After Dark` returns one matching card. From/Through November 1 plus Workshops returns one different event, First Sunday Print Exchange, with the matching full event preview.
- **Combined filters:** October 31–November 1 plus Music and Workshops yields four events, two per month. Both month headings/counts remain accurate. Multiple categories combine with OR; text, dates and category intersect.
- **Empty state:** unmatched text combined with existing dates/categories returns zero cards, removes empty month groups/jumps and shows an actionable empty state. The right pane does not retain an unrelated event.
- **Clear:** the empty-state action returns all 48 events and clears query, both dates and every category. Counts return to October 16 / November 32.
- **Invalid dates:** a start date later than the end date shows the inline error, focuses the end date on submission and keeps the applied results unchanged.
- **Retained choices:** search submission includes current dates/categories; opening a result retains them in the URL and fields. Event toolbar/back links return to the same results. Reload and browser Back retain applied state. URL state overrides browser-restored unsubmitted drafts.
- **Deep navigation:** Comedy yields 13 events (October 4 / November 9). From document `y=1550`, list `scrollTop=2519.3333`, selecting Leftovers & One-Liners opens that actual event at document `y=0` with the identical list position. Browser Back restores both `1550` and `2519.3333`, including the matching search preview. The helper waits for preview height to avoid clamping the reading point to the shorter loading panel.
- **Narrow layouts:** at 320 × 768, date controls fit, no horizontal document overflow, and Enter submits the complete form. At 834 × 1112, the empty state and clearing work in the single-column layout. At 1024 × 500, the closed results pane still leaves exactly 24px below it, and the right detail is not a nested scroll area.
- **Themes:** a one-result search and fetched matching preview work in every theme/mode, with a 1120px workspace and 24px arrival bottom gap at the default desktop viewport. Selected first cards measure 188px consistently (the existing In view badge adds 4px over the unselected 184px card). See `search-theme-checks.json`.
- No console warnings/errors were reported in the final browser checks.

## Evidence

`search-one-result.png`, `search-no-results.png`, `search-date-validation.png`, `search-phone-filters.png`, `search-tablet-empty.png`, `search-deep-back.png`, `search-theme-checks.json`.

## Limits

Native Firefox/Safari, assistive technology, operating-system forced colors and physical-device testing are not claimed. Existing kit contrast checks do not constitute a full accessibility audit. There is no backend, account storage, saved-event persistence or reservation service. Search works locally in JavaScript; automatic preview loading uses same-directory HTML over localhost and falls back to the working result link if unavailable.
