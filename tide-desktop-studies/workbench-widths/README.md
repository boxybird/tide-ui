# Workbench · Width comparisons

Open <http://127.0.0.1:4187/workbench-widths/index.html>. This is a child of the preserved Wide Open collection. The original Workbench, all prior studies, app 1.3.1 and kit 1.2.1 remain unchanged. The new comparison reuses the exact Workbench components, CSS, responsive adapter, content and behavior.

| Version | Filters | Event list | Individual event |
| --- | --- | --- | --- |
| Matched | Existing feed width | Same width | Remaining track space |
| Half Split | Half of the browsing group | Half of the browsing group | Same width as the complete browsing group |
| Midpoint | Average of the first two versions | Same width | Remaining track space |

The existing feed width is 352px from 1200px and 390px from 1440px. Half Split divides usable content space across a central 24px gutter into two equal groups: the browsing pair, including its internal 24px gap, and the individual event. Insets, typography, padding, controls, borders, photos, sticky heights and scroll behavior are identical. Below 1200px the original mobile/tablet composition returns. The right event remains natural document scrolling.

`widths.css` owns only three desktop grid recipes. It does not restyle components or redefine kit/app tokens. Midpoint is calculated from the other recipes at the actual width, rather than choosing an arbitrary extra percentage. No new component or script is added to the product.

`tools/build.py` calls the parent's Workbench generator and adds one private modifier, the width stylesheet and relative dependency paths. `tools/check.py` removes exactly those additions and compares every product document with the original. All 53 original routes are generated for each version, so event browsing, search, filtering, empty states and clearing work within the selected layout.

The comparison page reuses the existing review presentation and viewport selector. The 1200, 1280, 1440 and 1920px previews are live HTML, not images. Open links use the actual browser viewport.

Run from this folder:

```text
python -B tools/build.py
python -B tools/build.py --check
python -B tools/check.py
```

Use the existing parent's `node server.cjs` preview server on port4187; do not start a second server when it is running. Keep this directory in its existing parent location when moving the sources. Dependencies are read-only references to the original study and adjacent app, not copied component implementations. Never invoke parent/app/kit commands that write generated files or QA.

`tools/preserve.py` verifies the complete app/kit locks plus all 185 parent-study files from the original versioned archive. New files are confined to this child directory. Browser evidence and results live in `qa/`.

## Verification · 2026-10-22

160 HTML pages pass source checks, with 11,737 local references resolving. Removing the declared width-study additions leaves all 159 product documents identical to the original Workbench generator. The 185 original desktop-study files, all 980 original app files and 180 kit files remain byte-identical. No new kit component or product JavaScript is introduced.

Measured column widths (filters / list / event), rounded to pixels:

| Browser width | Matched | Half Split | Midpoint |
| --- | --- | --- | --- |
| 1200px | 352 / 352 / 369 | 262 / 262 / 548 | 307 / 307 / 459 |
| 1440px | 390 / 390 / 533 | 322 / 322 / 668 | 356 / 356 / 601 |
| 1920px | 390 / 390 / 981 | 434 / 434 / 892 | 412 / 412 / 937 |

Measurements account for native scrollbars, outer insets and gaps. In Half Split, both left columns plus their 24px internal gap exactly match the event width at all three desktop sizes. Midpoint's two left widths are the mathematical average of the other recipes.

No horizontal overflow occurs in the page, tools, results or detail at the measured desktop sizes. The list retains its 24px bottom gap. At 390 × 844 and 1024 × 768, all three versions match the original app's measured header, list, first-card geometry, title size and closed filter state; the tools slot is hidden.

Browser checks also cover combined date/category filters returning one event, an unmatched query returning zero, and clear-all restoring all 48 events. The longest event title fits its natural event opening at the smallest desktop width and remains in normal document flow. The comparison viewport selector resizes all three live frames and updates their labels without horizontal overflow. No console warnings/errors were observed in the test tab.

Evidence is saved in `qa/browser-measurements.json` and the PNG screenshots. Visual review covered the three desktop versions, a wide monitor, the smallest desktop and the long-title fixture. Browser execution used Codex's in-app Chromium; Firefox and Safari were not physically run. Shared behavior is inherited from the preserved Workbench adapter rather than reimplemented.

The saved source release is `dist/workbench-widths-1.0.0.zip`, with a SHA-256 checksum and an internal file manifest. It depends on this folder's original parent study and the adjacent preserved app; it is not a standalone replacement distribution.
