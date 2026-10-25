# Wide Open · three desktop studies

An isolated comparison of desktop compositions using the approved Bumble Dark app and Tide kit. The current app (1.3.1) and maintained kit (1.2.1) remain completely untouched. The preserved originals and their versioned ZIPs remain in `../tide-responsive-app/`.

Open <http://127.0.0.1:4187/>. The comparison page contains three working HTML previews. Change the preview viewport to compare a laptop, normal desktop or wide monitor. Open an individual study to use the browser’s actual viewport.

## The three compositions

1. **Panorama** opens the existing two-pane master/detail onto the full browser width. The list grows only within a controlled range; the image can use the remaining width. The story retains a comfortable reading column.
2. **Workbench** moves the original search and filter controls into a tools rail. The feed has room for more events, and the right event still scrolls naturally in the document. Search/date/category inputs are the original nodes, with their existing labels, form association and listeners.
3. **Open Book** puts the original photo opening and written details alongside each other. On tall screens the photo stays nearby while the story scrolls in the document. The list remains independently scrollable. Short windows use normal photo flow.

Enhancements begin at 75rem (1200px at the standard root size). Below that, the original mobile/tablet layout returns exactly. A landscape tablet below that threshold also keeps the baseline composition. No outer border boxes are introduced.

## What is fixed

Same 48 events, October/November grouping, native search and filters, real event URLs, list-position restoration, smooth return navigation, focus and reduced-motion behavior. Same Manrope, type/space/radius scales, semantic palette and all card/control/badge/notice styling. Saved/submission remain the baseline’s disclosed samples. No new service, framework or kit component is added.

`tools/build.py` reads the approved app generator and adds only composition classes, a layout stylesheet and (Workbench only) an empty tools slot plus a small responsive adapter. `tools/check.py` removes those declared additions and compares every generated product document with the original generator’s output. Any component-markup drift fails the check. Product study CSS may not redefine type/colors/borders/shared tokens or target kit component classes.

## Ownership

| File | Owns |
| --- | --- |
| `css/studies.css` | Desktop arrangement, column widths, placement, outer insets, scroll containment |
| `js/layout.js` | Workbench’s responsive relocation/restoration of original controls; revealing moved invalid fields |
| `css/review.css`, `js/review.js` | Comparison presentation and fitting live viewport frames; no product styling |
| `tools/build.py` | Deterministic static HTML generation from the locked app |
| `locks/*.json` | Complete file inventories and hashes for the app and kit |
| `server.cjs` | Local read-only preview mounts; no writes or APIs |

The private BEM blocks are `tide-study` and `tide-study-review`; they are study compositions, not additions to the kit registry. A wider browser does not justify a new button/card/field/rail component. The tools rail is a semantic ASIDE containing existing elements.

Fluidity comes from Grid tracks, not stretched type. Insets are 32px from 1200px, 48px from 1600px and 64px from 2240px, using existing spacing tokens. The shared 24px inter-pane gap and native scrollbars remain. The Open Book story track is bounded at 42rem; shared inner reading measures remain in force.

## Build and verify

No installation is needed. Python and Node are development/preview utilities only.

```text
python -B tools/build.py
python -B tools/build.py --check
python -B tools/check.py
node server.cjs
```

Never rebuild, check, edit or package the original kit from this study: some of those tools write generated/QA outputs. This study checks preservation by reading hashes. Python bytecode writing is disabled before importing the approved generator.

The local server maps `/base/` to the approved app, read-only. Keep this study beside `tide-responsive-app` when moving it. This is an isolated study source archive, not a replacement distribution of the app or kit. Their existing versioned archives remain preserved in the original project. See `qa/REPORT.md` for actual browser checks and limits.

`python -B tools/package.py` saves the study as `dist/wide-open-desktop-studies-1.0.0.zip`, checks the archived bytes and writes a SHA-256 file. The ZIP includes a file manifest, source, generated HTML, preservation locks and review evidence; it excludes its own distribution folder and bytecode caches.
