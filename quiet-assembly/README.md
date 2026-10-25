# Quiet Assembly

Three static HTML/CSS refinements combining the user's preferred elements:

1. Date Line — Manrope; the original card with a larger date in its information line.
2. Date Corner — DM Sans; a prominent date in the upper right.
3. Date Rail — Instrument Sans; a narrow rail beside the original information hierarchy.

All use continuous full-width cards with no gaps. The immersive full-screen event and longer details below it come from Quiet Studies. No editorial or serif fonts are used.

Open `index.html` for all three pairs. Each pair contains two 390×844 HTML frames. Open HTML opens a responsive standalone page. The Ink After Dark card opens its event; close returns to its list; the action and detail links scroll to the richer listing. Other event cards and bookmark/Saved marks are visual references.

Everything is local HTML/CSS with bundled fonts, images, Radix icons and licenses. No package install, API, framework or browser JavaScript is needed. An optional local preview is `node server.cjs`, then http://127.0.0.1:4177/.

`screens.css` preserves the first family's foundation and event anatomy. `cards.css` contains the three date arrangements, zero-gap list and short-height readability fallback. `themes.css` and `fonts.css` are generated from `studies.json`. `gallery.css` styles only the comparison canvas. `event-template.inc` holds the complete event HTML, adapted from the first family. `node build.mjs` regenerates all documents using only Node built-ins.

Earlier collections remain in their sibling folders, unchanged. This collection is portable and has no runtime dependency on them. Photography and event details are illustrative; no booking is made.
