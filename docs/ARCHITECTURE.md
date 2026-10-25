# Architecture and ownership

Tide is an HTML/CSS library. Its consuming app and documentation site share one compiled distribution. There is no application framework, package installation, CMS or external build service.

The package owns public component CSS, semantic tokens, theme seeds, canonical HTML recipes and their contracts. The site owns documentation rendering and presentation. The events example owns product-specific layout, responsive filter/modal orchestration, event/venue routing, search matching and scroll position. A reusable app discovery enters the kit only through the documented adoption process, with canonical CSS/HTML, states, registration and all-theme specimens.

Build order is package → site → example, driven by `tools/build.py`. Output goes only to ignored `build/`; no builder modifies a source template or writes inside an archive. `npm run check` verifies fresh/stale output and current contracts, then runs portable Python/Node tests. Old study preservation is independent through `npm run verify:history`; it is never a normal build dependency.

Every theme resolves the same semantic names. Light/dark are appearance modes rather than separate libraries. Theme changes cannot redefine typography, spacing or radius. Neutral notice borders, Manrope, square controls, accessible labels and unframed event compositions are preserved decisions.

The event example's five registered `src/styles/` modules bundle into one app-only stylesheet. Private layout, lineup, responsive drawer and venue classes describe their purpose; abandoned study variants are absent. The kit's public selectors, canonical recipes and themes remain unchanged. See the app ownership contract at `examples/events/docs/COMPONENT-OWNERSHIP.md`. Existing per-theme session keys remain compatible across the refactor.

Downloadable kit artifacts retain the independent kit version. Reference artifacts include both kit and app versions, so an app-only patch can be packaged without overwriting an earlier reference release.

App HTML expands shared partials at build time using the small dependency-free renderer in `examples/events/tools/html_templates.py`. The example manifest registers every partial; canonical card fixtures supply the all-events, exact-venue and saved lists. All 60 native routes use one document shell; 58 event/list/venue/saved routes share one workspace. Three explicitly registered content fragments retain unique venue/help/submission HTML. All 54 event details are generated from their shared recipe and canonical sample data. The output remains standalone HTML, with unchanged browser CSS/JavaScript. See `examples/events/docs/TEMPLATES.md` for authoring and escaping rules.

Individual details use structured paragraphs, places, inclusions, schedules, attendance notes and links. Existing full/concise compositions preserve heading levels, original photo controls, timestamps and venue links. `tools/template_engine.py` handles escaping/includes; `tools/event_details.py` owns detail composition. See `examples/events/docs/DETAILS.md`. Document/skip/script/footer profiles and eleven native submission-field recipes are documented in `examples/events/docs/PAGES.md`. Field definitions live in `data/submission-fields.json`; `tools/form_fields.py` escapes and composes them without adding browser behavior.
