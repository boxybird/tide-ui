# Content additions · 22 October 2026

Kit 1.2.0 / app 1.3.0. This record accompanies the new Prose component and Content page composition. The original foundations, theme inputs and existing event/card styling are preserved. The kit and app consume the same help template and component CSS.

## Automated verification

- Six theme/mode palettes: 348 foreground/surface contrast checks, including 24 additional prose-hover text pairs.
- Kit: 105 generated outputs current; 99 HTML documents, 1,602 local references, 14 matching screen/specimen templates and 21 registered components. No browser scripts or inline styles.
- All 14 existing kit tests pass. App verification additionally passes five data tests and 21 search/navigation tests.
- Application source/ownership checks verify the preserved 176-file original kit, 263-file three-event baseline and unchanged primitive/theme inputs.

## Actual browser observations

Surface: local in-app Chromium, served at `127.0.0.1:4186`. Firefox and Safari were not physically run. The added CSS uses the kit’s established supported feature set; this is not a whole-product accessibility certification.

1. **Six desktop modes, 1280 × 900:** identical 192px contents column, 48px gap and 65ch prose measure (approximately 634.4px at the current font). Header and prose align. Reading type is 16/28. No page overflow. [Tide dark](content-2026-10-22/desktop-tide-dark.png), [Tide light](content-2026-10-22/desktop-tide-light.png).
2. **Six modes at 320 × 760:** no horizontal page overflow. The app’s 305px usable width contains 257px prose; the 512px admission table scrolls inside its own region. All contents links resolve. At 390px and 834px, the contents remain above the article.
3. **Keyboard navigation:** Tab reveals the skip link with a visible focus outline; Enter focuses `main-content`. Contents links focus their destination headings; Back to top focuses `page-top`. The admission region is labelled from its caption, keyboard focus is visible, and Right scrolls it by 40px.
4. **Rich HTML at 320px:** 272px prose fits the page; a 512px table and 975px code line scroll inside their bounded containers. Long URLs wrap. The no-contents composition has one column. The excluded Notice paragraph retains its existing 12/20 typography and zero paragraph margins, rather than taking prose’s 16/28 rhythm. [Narrow specimen](content-2026-10-22/07-rich-html-320.png).
5. **Text enlargement:** a QA-only copy of the real help page, with root text set to 200%, computes 32px prose text at 1280 × 900 without horizontal page overflow. This checks text scaling; it is not a native browser-zoom test.
6. **Height and state:** the contents are static at 1280 × 600; at 1280 × 900 they are sticky and bounded to 852px. Prose emphasis computes italic with style-only synthesis, preserving the upright Manrope asset and existing application typography.
7. **Documentation:** the new specimens appear in Components and the help frame appears in Screens. Exactly one theme-picker group is visible at `#content-pages`; switching to Bumble Light retains that fragment. [Kit specimens](content-2026-10-22/09-kit-documentation.png).

Full app evidence and measurements are retained in `tide-responsive-app/qa/content-2026-10-22/` in the app package. The screenshots above are exact copies of inspected captures from this verification run, included here so the standalone kit remains reviewable.

## Limits and preservation

Help routes are static HTML with native navigation, no support inbox or live booking. Prose does not sanitize rich HTML or invent table semantics/alt text. The eventual content pipeline and real policy copy remain outside this CSS/HTML addition.

A before/after hash comparison covers 393 current app files. All 364 existing product HTML files and `css/app.css` remain byte-identical. Only 28 existing review pages change, adding Help to their review navigation. Prior maintained kit 1.1.0 and app 1.2.1 ZIPs remain preserved alongside the new packages.
