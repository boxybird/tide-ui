# Tide kit 1.3.0 — shared search and filters

Open [release review](http://127.0.0.1:4187/shared-filter-release/index.html), [the new kit](kit/index.html#components), or [the independent app copy](app/index.html?preview-filters=open).

One additive component, Filter panel, replaces the copied app's private scrolling-body, pinned-footer, status-row and count rules. Existing controls and states are reused. Matching, GET routing, native dialog lifecycle, responsive placement and scrollbar measurement stay in the host. No framework or kit browser script is added.

The exact primitives and three theme inputs are inherited from kit 1.2.1. All six library views and filter specimens are generated from shared source. Manrope, spacing, square controls, neutral callouts, unframed event panes and natural right-document scrolling remain fixed.

## Source homes

| Concern | Source |
| --- | --- |
| Shared component CSS | `kit/css/filter-panel.css` |
| Shared shell HTML / renderer | `kit/templates/filter-panel.html`, `kit/tools/filter_panel.py` |
| Registration | `kit/component-manifest.json` |
| Integration / state contracts | `kit/docs/SEARCH-FILTERS.md` |
| All-mode examples | `kit/templates/frames/filter-panel.html` |
| Consumer migration | `tools/build_app.py` |
| Consumer behavior / geometry | `app/js/filters.js`, `app/js/rail.js`, `app/css/host.css` |
| Preservation / adoption gates | `tools/check.py`, `qa/verification.json` |

## Build and check

Use Python with `-B` to avoid bytecode in frozen dependencies.

```text
python -B kit/tools/build.py
python -B tools/build_app.py
python -B tools/build_review.py
python -B kit/tools/build.py --check
python -B kit/tools/check.py
python -B -m unittest discover -s kit/tools -p test_*.py
python -B tools/build_app.py --check
python -B tools/check.py
```

The build reads approved prototype HTML as an immutable input, and writes only this sibling. The consumer has 53 independent pages, local host scripts/CSS, new kit assets and an organizer-upload sample. Its links stay within the copied app.

## Preservation and scope

Approved Unified Search 1.0.2: 72 files, archive SHA256 `1f8226ef94f33fec68671b6f72ac9c0de87fdf2c94554714a95f506e344ac490`. Frozen kit 1.2.1 (180 files), app 1.3.1 (980 files), original foundation and earlier studies are checked read-only. Nothing is redirected to this new release automatically.

Actual browser results and remaining limits live in `qa/BROWSER.md`. Firefox/Safari were explicitly deferred by the user; they are not claimed as tested. Saved/submission remain illustrative, as in the approved app. This is local HTML/CSS plus narrow host enhancements, not a backend or PWA implementation.
