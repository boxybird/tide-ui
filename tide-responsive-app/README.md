# Tide in use

**Current release: app 1.3.1 / kit 1.2.1.** Event lists and individual-event panes have no decorative outer border or rounded clipping shell at any width. Desktop list sizing/scrolling and the natural event document remain intact. The previous 1.3.0 and kit 1.2.0 packages are preserved.

A mobile-first HTML/CSS app playground consuming the maintained Tide kit in `kit/`. The original `../tide-ui-kit/` is preserved as a reference.

App 1.3.0 / kit 1.2.0 added scoped Prose and a reusable Content page layout, with a realistic help page across all six theme/modes. Open `help-review.html` for comparisons, `help.html` for the actual page or `kit/index.html#content-pages` for the component specimens. Existing event pages, search and filtering retain their design and behavior. See `kit/docs/CONTENT.md` for the shared HTML/CSS contract.

App study 1.0.1 refines the desktop list height: the complete container fits on arrival with a 24px bottom gap, accounting for the header and top spacing. Event details retain natural document height. See `qa/VIEWPORT-FIT.md`. The original 1.0.0 package remains in `dist/`.

App study 1.0.2 adds native smooth in-page scrolling, gated by the user's reduced-motion preference. Wheel and trackpad behavior remain native. Earlier packages are retained.

App study 1.0.3 applies that return motion when selecting another event after reading down the desktop detail page. A small optional script waits for the CSS-driven return to the top, then follows the real HTML link. The list keeps its scroll position; Back restores the previous reading position. Mobile, reduced-motion and modified clicks retain immediate/native navigation.

Start `node server.cjs`, then open http://127.0.0.1:4186/review.html. Open `index.html` for the actual responsive app. All pages also work directly from disk.

## Review

- `review.html`: browse at phone, portrait tablet and desktop sizes.
- `event-review.html`: the full event at the same sizes.
- `search-review.html` and `submit-review.html`: additional compositions.
- `help-review.html`: long-form help content at phone, tablet and desktop sizes, with all theme links.
- Six named theme/mode directories use identical markup and layout: Tide, Summer and Bumble, each dark/light. Root pages are Tide dark.
- `kit/index.html`: reviewed component library, preserved foundations and all previous screen specimens.

The comparison page scales actual HTML iframes for inspection. Use **Open app** to try the real page at the width of your browser. Screenshots are in `qa/`.

## Source

- `data/events.json`: 48 fictional events, shared across all routes; 16 in October and 32 in November.
- `data/events-core.json`: original three records; their details remain preserved in the larger dataset.
- `tools/seed_events.py`: authoring source for the expanded fixture. Only reseeding needs IANA timezone data; ordinary builds use committed timestamps.
- `tools/build.py`: deterministic HTML generation; no runtime framework.
- `js/event-navigation.js`: optional desktop return-to-top enhancement and list-only month jumps. No content replacement or app framework.
- `js/search-core.js`: tested text, date/category and query-string rules shared with the fixture tests.
- `js/event-search.js`: local HTML filtering and native GET submission; a matching desktop preview loads from an existing static event page.
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
python -m unittest discover -s tools -p "test_*.py"
node --test tools/test-event-navigation.cjs tools/test-search.cjs
```

No dependencies need downloading. Python 3 and Node.js are only build/preview tools; the delivered HTML/CSS is portable.

## Scope

Search, date/category filters, clear-all recovery, event navigation, month jumps and anchored details work. Search applies on submission rather than every keystroke. Search and filters require JavaScript; all 48 event links remain available without it. Use the localhost server for automatic matching event previews; local files retain functional matching and event links. Saved is still a fixed one-event shortlist. The submission form does not send anything. There are no reservations, accounts, persistent bookmarks, installations, offline cache or service worker. The PWA product work follows once the responsive design is selected.
