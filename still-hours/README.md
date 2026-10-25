# Still Hours

A second family of six subtle dark refinements of Burque’s Ink After Dark.

1. Sage — Fraunces + DM Sans
2. Bookish — Lora + DM Sans
3. Soft Margin — Fraunces + Instrument Sans
4. Field Notes — Literata + IBM Plex Sans
5. Umber — Lora + Source Sans 3
6. Hushed — Fraunces + DM Sans

Open `index.html` for all six pairs. Each pair has a 390×844 list and event frame. Use Open HTML to view a responsive standalone document. Everything is static HTML/CSS with local assets, so no network or package install is needed for viewing.

Optional local preview: `node server.cjs`, then http://127.0.0.1:4176/.

`screens.css` owns the shared anatomy. `themes.css` contains semantic per-study tokens, generated from `studies.json`. `fonts.css` holds local faces. `gallery.css` styles only the comparison canvas. `design-notes.html` explains the choices.

`build.mjs` is optional build-time authoring, not browser code. It uses Node built-ins and the bundled assets. `detail-content.inc` holds the shared long-form listing. To regenerate: `node build.mjs`, `node qa/contrast.mjs`, `node notes.mjs`.

Ink After Dark opens by a normal HTML link. The event page includes full details below the first frame. Bookmark marks, Saved, and the first two event cards are visual-only in this design study. All events and photography are illustrative; no booking is made.

The first collection, Quiet Studies, remains unchanged in the sibling `refinements` folder. This collection is portable and does not need that folder to view or rebuild from bundled assets.

Photo: exact Ink After Dark workshop image from the existing Burque mobile prototype. Fonts: OFL, licenses included. Icons: Radix Icons, MIT license included. Surface texture: CSS.
