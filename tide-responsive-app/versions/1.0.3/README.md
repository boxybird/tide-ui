# Tide in use

A mobile-first, static HTML/CSS app study using the approved Tide kit. The original `../tide-ui-kit/` is preserved. A reviewed copy is included in `kit/`.

App study 1.0.1 refines the desktop list height: the complete container fits on arrival with a 24px bottom gap, accounting for the header and top spacing. Event details retain natural document height. See `qa/VIEWPORT-FIT.md`. The original 1.0.0 package remains in `dist/`.

App study 1.0.2 adds native smooth in-page scrolling, gated by the user's reduced-motion preference. Wheel and trackpad behavior remain native. Earlier packages are retained.

App study 1.0.3 applies that return motion when selecting another event after reading down the desktop detail page. A small optional script waits for the CSS-driven return to the top, then follows the real HTML link. The list keeps its scroll position; Back restores the previous reading position. Mobile, reduced-motion and modified clicks retain immediate/native navigation.

Start `node server.cjs`, then open http://127.0.0.1:4186/review.html. Open `index.html` for the actual responsive app. All pages also work directly from disk.

## Review

- `review.html`: browse at phone, portrait tablet and desktop sizes.
- `event-review.html`: the full event at the same sizes.
- `search-review.html` and `submit-review.html`: additional compositions.
- Six named theme/mode directories use identical markup and layout: Tide, Summer and Bumble, each dark/light. Root pages are Tide dark.
- `kit/index.html`: reviewed component library, preserved foundations and all previous screen specimens.

The comparison page scales actual HTML iframes for inspection. Use **Open app** to try the real page at the width of your browser. Screenshots are in `qa/`.

## Source

- `data/events.json`: three fictional events, shared across all routes.
- `tools/build.py`: deterministic HTML generation; no runtime framework.
- `js/event-navigation.js`: optional desktop return-to-top enhancement for real HTML event links. No content replacement or app framework.
- `css/app.css`: layout compositions, importing component geometry and semantic colors from `kit/css/tide.css`.
- `css/review.css`: review presentation only, not part of the product.
- `kit/css/`, `kit/tokens/`, `kit/templates/`: reviewed kit source.
- `docs/REVIEW.md`: code/accessibility findings and limits.
- `docs/RESPONSIVE.md`: responsive behavior, extension contract and PWA considerations.

To rebuild, run `python kit/tools/build.py` then `python tools/build.py` from this directory. To validate:

```
python kit/tools/build.py --check
python kit/tools/check.py
python -m unittest discover -s kit/tools -p "test_*.py"
python tools/build.py --check
python tools/check.py
node --test tools/test-event-navigation.cjs
```

No dependencies need downloading. Python 3 and Node.js are only build/preview tools; the delivered HTML/CSS is portable.

## Scope

Event navigation, anchored details, native filter disclosures, reset buttons and form inputs work. Search and saved lists are fixed examples. The form does not send anything. There are no reservations, accounts, persistent bookmarks, installations, offline cache or service worker. The PWA product work follows once the responsive design is selected.
