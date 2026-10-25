# Burque events example · 1.1.3

A framework-free consuming app for Tide 1.3.0. It includes 54 authored sample events, the accepted sticky month-heading hierarchy, live draft search counts, pinned Show events actions and the Sunshine Theater venue journey. No live submissions, accounts, booking or PWA services are implemented.

Build and preview from the repository root: `npm run build`, `npm run check`, `npm run dev`. Open `/events/app/index.html?preview-filters=open`. `/events/index.html` links to complete examples for all six theme/mode combinations. All pages consume the one `build/tide/css/tide.css` distribution.

Edit `src/templates/` for shared app markup, including `event-page.html` and `event-detail.html`. `data/events.json` is the canonical 54-event fixture for cards and individual details; `data/detail-presentations.json` preserves the two existing detail compositions. `data/pages.json` records the six non-event route contexts. Only their unique venue/help/submission content and list-page wrappers remain in `src/pages/`. Event URLs are generated directly from sample IDs. See [template authoring](docs/TEMPLATES.md) and [detail content](docs/DETAILS.md).

The build expands registered partials before resolving `{{KIT_CSS}}`, `{{APP_CSS}}` and `{{KIT_ASSETS}}` paths. The five stylesheet modules in `src/styles/` bundle in manifest order; browser behavior remains in `src/runtime/`. Search tests use the same canonical card data, without needing generated output. All data remains authored samples, not a live ingestion pipeline.

App-only styles now have purpose-based homes: base, lineup, desktop geometry, responsive filters and venue composition. Study-era aliases and inactive variants are removed. The kit's CSS, HTML recipes, tokens and assets are unchanged. Keep the bounded list, natural right document, unframed panes, semantic tokens, native scrollbar allowance and responsive filter behavior. See [component ownership](docs/COMPONENT-OWNERSHIP.md), [sample data](docs/SAMPLE-DATA.md) and [detail refactor verification](../../docs/refactors/event-details/VERIFICATION.md).
