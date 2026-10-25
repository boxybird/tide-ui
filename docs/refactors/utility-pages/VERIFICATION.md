# Events 1.1.4 — venue and utility HTML

This app-only cleanup starts from `9ce80e0c683aa7732febbfd6e543674844f61f47`. The kit, reference site and approved app appearance/behavior are preserved.

## Review and extraction

All 60 native routes share one `document.html`, including metadata, stylesheet/script order, body/session attributes, header and route-specific skip links. The 58 list/search/saved/venue/event routes share one `workspace.html` and hidden preview state. The common site disclaimer is a partial; help retains its distinct content footer. Route-specific venue scripts, filter controls, body classes, navigation and skip targets retain their prior differences.

Eleven repeated submission-field wrappers now compose registered label/input/textarea/select/option/hint/optional fragments from `data/submission-fields.json`. Text is escaped, supported controls and data keys are restricted, and each field must have exactly one content slot. Native required/optional state, maxlength, autocomplete, date/time/email controls and reset behavior remain intact. Upload, permission, paired rows and form sections stay in their single authored source. The existing back icon is reused.

Only three unique fragments remain in `src/pages/`: Sunshine Theater information, help and submission. The venue facts, attributed sources, prose, table, contents navigation and bespoke controls are retained verbatim. They do not need a new generic content renderer. No public kit component or styling is introduced. See `examples/events/docs/PAGES.md` for the page composition contract.

## Verification performed

- Compared all 420 generated app/theme pages to the prior build. All element order, decoded attributes, normalized text, native IDs/associations, scripts, links and content match; differences are formatting and equivalent attribute ordering/escaping.
- Compared geometry and 55 computed style properties per HTML element across 25 states: venue/help/submission in every theme/mode, phone versions of each, tablet venue and desktop list/event/saved. No recorded differences or horizontal overflow.
- Four matched screenshots are pixel-identical: Bumble Dark venue, help, submission and phone venue.
- Eleven browser observations cover native required/optional/email behavior, submission reset, help contents focus/scroll, venue live draft/commit, zero-result guide retention, scoped reset, one tablet form, completed Escape rollback/focus restoration and the phone venue-information jump. No captured console warnings/errors.
- All 79 protected source files across the kit, reference site, app CSS and browser runtime remain unchanged. All 12 generated runtime files remain byte-identical.
- Eight new utility contracts supplement the sixteen existing app contracts. They cover script/session profiles, omitted controls/footer variants, skip targets, native field validation/association, copy escaping, invalid field definitions, venue/help landmarks and document-title escaping. Existing palette/markup and venue/search tests remain required.

Measured records: [markup/source/pixel parity](parity-checks.json), [browser observations](browser-checks.json). Screenshots: [venue](bumble-dark-sunshine-theater.png), [help](bumble-dark-help.png), [submission](bumble-dark-submit.png), [phone venue](phone-venue.png).

Browser evidence is Windows in-app Chromium. Native Firefox/Safari, physical-device and screen-reader checks remain deferred. The data stays authored samples; no content correction, live ingestion, submission service, new browser rendering, CSS or navigation behavior is part of this refactor. Historical tags and preserved versions remain untouched.
