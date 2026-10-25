# Date Line — appearance studies

Four complete static HTML/CSS kits: the Date Line reference plus Daybreak, Tide and Lift. Open index.html or run `node server.cjs` and visit http://127.0.0.1:4183/. The original kit at port4182 is preserved.

The same Foundations / Components / Screens / Coverage presentation appears in each kit. Use Compare appearance in the sidebar; ordinary HTML links retain the current section without JavaScript. Every kit has the exact same screen fixtures, form controls, event content, fonts, type scale, spacing, target sizes, coverage table and assets. Browser-native inputs remain native.

Daybreak uses a pale lilac canvas, warm white cards and plum actions. Tide uses navy/teal with square control and panel corners. Lift uses charcoal/lavender with raised panels, button shadows and inset fields. The photograph opening remains a distinct dark reading surface with light text in all three skins; its photo/crop/scrim/geometry stay fixed. The content below it follows the selected palette.

Only palette, corner treatment and paint/elevation vary. No gaps were added between event cards. No text sizes or spacing were changed. Shadows affect paint only, not layout. Native checkbox/radio geometry is retained rather than replacing those primitives.

Root foundation CSS and assets are copied once and shared. `build.py` generates the reference copy and three variants from ../date-line-ui-kit/. Each variant has a paint-only skin.css and tokens.json. Run the build script from the workspace root. The generator does not modify its source kit. skins.json records each palette; screen-map.json is shared across all four.

These remain static design fixtures: native selection/reset/required-field validation and navigation work, but search results and submission review content are fixed. Nothing is uploaded, saved, sent or published. The pending-review page is a sample state; no notification or real submission occurs. Events, addresses and contact destinations are illustrative.

See design-qa.md and qa/ for side-by-side captures, layout/content invariance and contrast evidence. All existing asset provenance and licenses remain in assets/ and licenses/. No new artwork, typefaces or icon library was introduced.
