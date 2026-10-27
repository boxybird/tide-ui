# Events 1.1.3 — shared individual details

This app-only refactor starts from commit `734b4015a1d46d56aa178180cb1262fae4fa9ec7`. The approved UI kit and app appearance/behavior remain intact.

## Maintained sources

All 54 native event documents now use `event-page.html` and `event-detail.html`; their URLs are unchanged. The six non-event source documents remain in `src/pages/`. Index/search/saved previews reuse the same event content at their existing heading levels.

`data/events.json` extends the canonical sample catalog with structured detail content. Existing full/concise defaults live in `data/detail-presentations.json`. Plain paragraphs, places, inclusions, schedules, attendance notes and venue links render through registered partials; no event HTML is stored in JSON. Shared inline icons retain their exact existing shapes and attributes. The include/escaping engine is isolated in `tools/template_engine.py`, with detail composition in `tools/event_details.py`.

HTML and content sources decrease from 855,661 to 267,152 bytes (68.8%). Fifty-four duplicated source documents are removed while all 54 native event routes are still generated. The authoring contract is `application-kits/lineup/docs/DETAILS.md`.

## Actual verification

- Compared all 420 generated event/theme pages with the approved build. All elements, decoded attributes, normalized text, IDs, links, event order and native associations match. Twenty-one pages remain byte-identical; other changes are formatting and equivalent entity escaping.
- Compared geometry and 55 computed style properties per HTML element across 25 viewport/theme states. Coverage includes all six theme modes, desktop/short/wide/tablet/phone widths, full/concise events, comedy, long titles/copy, saved/default previews and zero-result venue information. No recorded differences or horizontal overflow.
- Six matched screenshots are pixel-identical: default desktop, full Ink After Dark desktop, long detail, comedy detail, phone Ink After Dark and phone Sunshine Theater event. The default desktop pair was repeated at one fixed viewport after initial raster differences despite identical geometry.
- Eleven browser checks passed: full detail/list selection, attendance fragment/focus, live-filtered detail preview, venue navigation and scoped zero results, phone rough-upload/full-screen behavior, saved preview, Escape rollback/focus, scrollbar/footer alignment, smooth native event selection and Back reading-position restoration. No captured console warnings/errors.
- Desktop at 1440×900 still measures a 10px occupied native gutter, with list and Show events both ending at 866px. Browser Back restores the recorded 900px reading position.
- All 59 kit input files and all 12 generated app runtime files (CSS, browser scripts and assets) are unchanged. No kit source, theme, component recipe or primitive was edited.

Eight new detail contracts supplement the eight existing app template contracts. They cover complete native route generation, one main heading and stable anchors, preview heading levels, full/concise control differences, authored timezone/range preservation, text/attribute escaping and rejection of raw HTML blocks, unsafe links, invalid heading levels and unsupported image sources. Existing palette/markup tests and 16 venue/search assertions remain required. Source checks reject pasted event hero/story markup in non-event documents, and route validation rejects restored per-event HTML copies.

Measured records: [source/HTML/pixel parity](parity-checks.json), [browser checks](browser-checks.json). Screenshots: [desktop](desktop.png), [full detail](ink-desktop.png), [long detail](long-detail.png), [comedy](comedy-detail.png), [phone full detail](phone-event.png), [phone concise detail](phone-venue-event.png).

Browser evidence is Windows in-app Chromium. Native Firefox/Safari, physical-device and screen-reader checks remain deferred. All content remains authored samples, with existing venue-fact attribution retained. No historical tag, preserved version, live ingestion, booking, browser renderer or router was changed or added.
