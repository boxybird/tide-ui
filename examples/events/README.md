# Burque events example · 1.1.1

A framework-free consuming app for Tide 1.3.0. It includes 54 authored sample events, the accepted sticky month-heading hierarchy, live draft search counts, pinned Show events actions and the Sunshine Theater venue journey. No live submissions, accounts, booking or PWA services are implemented.

Build and preview from the repository root: `npm run build`, `npm run check`, `npm run dev`. Open `/events/app/index.html?preview-filters=open`. `/events/index.html` links to complete examples for all six theme/mode combinations. All pages consume the one `build/tide/css/tide.css` distribution.

Edit `src/pages/`, `src/styles/` and `src/runtime/`, then rebuild. Source HTML uses `{{KIT_CSS}}` and `{{APP_CSS}}` route placeholders resolved by the builder. The builder bundles the five app stylesheet modules in the order registered by `consumer-manifest.json`. The fixture JSON records authorship/provenance; it is not a live event ingestion pipeline. Search assertions run against these source pages without generated output.

App-only styles now have purpose-based homes: base, lineup, desktop geometry, responsive filters and venue composition. Study-era aliases and inactive variants are removed. The kit's CSS, HTML recipes, tokens and assets are unchanged. Keep the bounded list, natural right document, unframed panes, semantic tokens, native scrollbar allowance and responsive filter behavior. See [component ownership](docs/COMPONENT-OWNERSHIP.md), [sample data](docs/SAMPLE-DATA.md) and [refactor verification](../../docs/refactors/app-css/VERIFICATION.md).
