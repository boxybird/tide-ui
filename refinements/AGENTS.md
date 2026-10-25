# Quiet Studies — project instructions

- The user explicitly requested six static HTML/CSS refinements, not a new interactive app. Keep the browser deliverable free of JavaScript and application dependencies.
- Preserve the Ink After Dark concept, exact workshop photo, same event content, dark aesthetic and two-frame list/opened-listing presentation. Explore small typographic, spacing and color refinements.
- Numbering and names: 01 Soft Focus, 02 Humanist, 03 Warm Editorial, 04 Open Form, 05 Studio Notes, 06 Quiet Air.
- User requires deliberate typography, hierarchy, coherent spacing and pixel review. CSS tokens and browser evidence matter more than introducing features.
- `screens.css` owns shared anatomy, `themes.css` owns the six token sets, `fonts.css` holds local font faces, and `gallery.css` styles only the comparison canvas.
- `build.mjs` emits static HTML and copies existing images, fonts and library icons. It runs only at build time. `notes.mjs` emits static rationale. Neither is shipped as browser JavaScript.
- All external font/icon licenses are bundled. Original photo and texture come from the existing Burque prototype; do not regenerate them for these studies.
- Existing `../burque` and `../burque-pocket` prototypes must remain intact. This study uses its own local static preview on port4175.
- The user authorized independent design decisions and requested completion without overnight intervention. Finish the agreed deliverables and checks; do not ask for preference selection during production.
