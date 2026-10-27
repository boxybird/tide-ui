# Events 1.1.2 — shared app HTML

This app-only refactor starts from commit `11563fe09b420bbf496781dac984ef7e9f28db1b`. The UI kit and the approved app appearance/behavior are preserved.

## Maintained sources

Sixteen registered partials now own the header, responsive filter controls/rail/dialog, result introduction/summary, month groups/jumps, event card, empty state and list footer. All 60 native route documents consume those shared sources. Individual event details and unique help, submission and venue content remain in their route files.

The all-events, exact Sunshine Theater and saved lists reuse one 54-card fixture and one card recipe. Explicit context preserves current navigation, heading levels, selected-card status, initial preview, collection counts and saved-page differences. The original sample JSON/provenance records remain intact. The renderer is build-time Python with no new dependencies; output remains standalone HTML.

Authored page HTML previously occupied 5,872,914 bytes. Pages, shared partials and the two new card/route data files total 855,661 bytes, an 85.4% reduction. Shared sources and contracts are described in `application-kits/lineup/docs/TEMPLATES.md`.

## Actual checks

- Compared all 420 generated route/theme pages with the approved build. Elements, decoded attributes, normalized text, native associations, event order and selected state match. Twenty-one pages are byte-identical; the remainder differ in card formatting and equivalent HTML entity escaping.
- Compared geometry and 55 computed style properties per HTML element across 20 states: desktop, short/wide windows, tablet/portrait tablet, phone list/event, 320px phone, venue, zero results, long query, help/saved/submission and every theme/mode. No recorded differences or horizontal overflow.
- Five matched screenshots are pixel-identical: desktop, tablet, phone list, phone event and venue.
- Thirteen browser behavior checks passed: live draft versus applied feed, one-result preview, scoped zero/reset, month jumps, Escape/focus restoration, open-drawer resize with one control set, inclusive date/category matching, invalid-date blocking, native event selection and browser Back restoration.
- Desktop still measures a 10px occupied native gutter at 1440×900. List and Show events both end at 866px. The November jump lands at 249px below the summary. Back restores the recorded 900px reading position.
- All 59 kit input files and all 12 generated app runtime files (CSS, browser scripts and assets) are unchanged. No public kit selector, token, theme or recipe changed.

Eight template contracts cover complete event routes, selected/scoped/saved lists, native navigation variants, text/attribute escaping, non-execution of text resembling includes, and missing/malformed/cyclic include failures. Existing palette/markup tests and 16 venue/search assertions remain required. Normal source checks also prevent pasting shared app markup back into route documents.

Measured results: [HTML/source/pixel parity](parity-checks.json) and [browser checks](browser-checks.json). Screenshots: [desktop](desktop.png), [tablet](tablet.png), [phone list](phone-list.png), [phone event](phone-event.png), [venue](venue.png).

Browser evidence is Windows in-app Chromium. Native Firefox/Safari, physical-device and screen-reader checks remain deferred. This refactor does not introduce live data, a CMS, client-side templating, a new router or new UI behavior. Historical tags and preserved source versions are untouched.
