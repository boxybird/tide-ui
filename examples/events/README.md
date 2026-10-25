# Burque events example · 1.1.0

A framework-free consuming app for Tide 1.3.0. It includes 54 authored sample events, the accepted sticky month-heading hierarchy, live draft search counts, pinned Show events actions and the Sunshine Theater venue journey. No live submissions, accounts, booking or PWA services are implemented.

Build and preview from the repository root: `npm run build`, `npm run check`, `npm run dev`. Open `/events/app/index.html?preview-filters=open`. `/events/index.html` links to complete examples for all six theme/mode combinations. All pages consume the one `build/tide/css/tide.css` distribution.

Edit `src/pages/` and `src/runtime/`, then rebuild. Source HTML uses `{{KIT_CSS}}` and `{{APP_CSS}}` route placeholders resolved by the builder. The existing static page compositions are retained deliberately during this structural migration. The fixture JSON records authorship/provenance; it is not a live event ingestion pipeline. Search assertions run against these source pages without generated output.

App-only CSS remains byte-identical to App 1.1.0, including private compatibility class names. A later, separately reviewed refactor can consolidate inherited layout layers. Keep the bounded list, natural right document, unframed panes, semantic tokens, native scrollbar allowance and responsive filter behavior. See [component ownership](docs/COMPONENT-OWNERSHIP.md), [sample data](docs/SAMPLE-DATA.md) and repository [verification](../../docs/migration/VERIFICATION.md).
