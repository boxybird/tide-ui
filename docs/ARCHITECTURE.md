# Architecture and ownership

Tide is an HTML/CSS library. Its consuming app and documentation site share one compiled distribution. There is no application framework, package installation, CMS or external build service.

The package owns public component CSS, semantic tokens, theme seeds, canonical HTML recipes and their contracts. The site owns documentation rendering and presentation. The events example owns product-specific layout, responsive filter/modal orchestration, event/venue routing, search matching and scroll position. A reusable app discovery enters the kit only through the documented adoption process, with canonical CSS/HTML, states, registration and all-theme specimens.

Build order is package → site → example, driven by `tools/build.py`. Output goes only to ignored `build/`; no builder modifies a source template or writes inside an archive. `npm run check` verifies fresh/stale output and current contracts, then runs portable Python/Node tests. Old study preservation is independent through `npm run verify:history`; it is never a normal build dependency.

Every theme resolves the same semantic names. Light/dark are appearance modes rather than separate libraries. Theme changes cannot redefine typography, spacing or radius. Neutral notice borders, Manrope, square controls, accessible labels and unframed event compositions are preserved decisions.

The event app retains its existing compatibility names and concatenated host layers during migration. This makes geometry and CSS parity verifiable. Consolidating private app classes/styles is a separate future change; public component selectors and themes should remain stable.
