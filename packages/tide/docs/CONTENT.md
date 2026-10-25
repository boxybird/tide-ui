# Prose and content pages · Kit 1.2.0

These additions extend the existing Tide system. Manrope, colors, fixed scales, 2/4px corners and neutral outlines remain unchanged. The app consumes the kit implementation; it does not restyle these blocks.

CSS source: `css/content.css`, bundled in `tide.components.extensions` within `css/tide.css`. Registry: `component-manifest.json`. Full help source: `templates/content/help.html`. Rich-HTML specimen: `templates/frames/prose.html`. Both specimens are generated in every theme and light/dark mode.

## Prose

Use one `.tide-prose` wrapper around ordinary HTML from a trusted renderer. Descendant elements need no editor-specific classes. All selectors are scoped; prose rhythm does not change cards, forms or event details outside the wrapper. Descendant selectors use `:where()` to keep specificity low.

```html
<article class="tide-prose">
  <h2 id="admission">Admission</h2>
  <p>Check the organizer’s <a href="event.html">event details</a>.</p>
  <ul><li>Confirm the price and any registration requirement.</li></ul>
</article>
```

The reading style uses existing 16px control type with 28px section leading, a 65ch maximum measure and the existing secondary/primary text roles. This is a new reading context, not a change to Tide’s 14/24 application body. Paragraphs are separated by 20px; H2 uses 40px before and 12px after; deeper headings use 32/12. First/last block margins are removed inside the scope. Nested lists use the smaller 8px relationship. All values come from existing rem tokens and scale with browser preferences.

Supported elements: H1–H6, paragraphs, strong/emphasis, links, nested UL/OL, definitions, blockquotes/citations, rules, figures/images/video/captions, tables/captions/TH/TD, inline code/KBD/SAMP and PRE. H4–H6 retain a readable 14px size; semantic level does not imply continually shrinking text. Choose heading levels from the outline, not from their appearance.

Links remain underlined. Unvisited/hover links use the audited accent roles; visited links use the audited secondary text role. Focus comes from the shared focus-visible contract. Quotations have the same neutral border on all sides. No colored left stripe, new palette, runtime dependency or Tailwind is introduced.

The preserved Manrope font asset is upright. Within Prose only, EM/I permit synthetic italic styling so genuine emphasis remains visible; synthetic weights stay disabled. An excluded component keeps its own typography contract.

### Tables and overflow

Small tables without a wrapper use a fixed layout and wrap their cells. For a wide table, use the optional BEM element below. It contains horizontal scrolling instead of making the page scroll sideways. Keep the native TABLE/THEAD/TBODY/TH/TD structure; CSS cannot supply missing header associations.

```html
<div class="tide-prose__table-wrap" role="region"
     aria-labelledby="admission-caption" tabindex="0">
  <table>
    <caption id="admission-caption">Admission options</caption>
    <thead><tr><th scope="col">Option</th><th scope="col">Details</th></tr></thead>
    <tbody><tr><th scope="row">Free</th><td>Check registration.</td></tr></tbody>
  </table>
</div>
```

The optional wrapper has a 32rem table minimum; its own width is bounded. Its visible caption supplies an accessible name. A tab stop gives keyboard access in engines that do not automatically focus scroll containers. Avoid assigning a scrolling region to every short two-column table. Long code samples scroll within PRE; give a potentially scrolling PRE `tabindex="0"` and a useful accessible name. Ordinary text, inline code and URLs wrap. Printing releases the scrolling constraints.

Images/video retain their intrinsic ratio. Supply correct dimensions, meaningful alt text or an intentional empty alt, and a caption where useful. Prose does not invent alt text, sanitize HTML, permit arbitrary embeds or establish a video-player contract. Sanitize rich HTML and validate URLs in the eventual content pipeline. Styling is not a security boundary.

### Embedded components

An editor may insert a real kit Notice, Button or other block. Wrap it in `.tide-prose__exclude`. Prose descendant styles, including heading/list/link/margin rules, do not enter that subtree; its text defaults return to the kit’s 14/24 body. The host still needs to include that component’s required classes and semantics.

```html
<div class="tide-prose">
  <p>Ordinary prose.</p>
  <div class="tide-prose__exclude">
    <div class="tide-notice"><strong>A useful note</strong><p>Notice copy.</p></div>
  </div>
  <p>Prose resumes.</p>
</div>
```

Do not nest another prose wrapper inside an excluded subtree. Use a sibling prose section instead. The supported component extension point is `--tide-prose-measure`, defaulting to `--tide-layout-reading`. Theme definitions continue to change colors only.

## Content page

`.tide-content-page` is a documented composition of a title/intro, optional metadata, optional contents navigation, body and optional footer. It is not tied to the event-list workspace. It uses natural document scrolling, a 70rem contained canvas, existing 24px insets and a prose reading measure.

```html
<main class="tide-content-page" id="main-content" tabindex="-1">
  <header class="tide-content-page__header">
    <p class="tide-eyebrow">Help</p>
    <h1 class="tide-content-page__title">Planning your visit</h1>
    <p class="tide-content-page__lead">The essentials before you go.</p>
    <p class="tide-content-page__meta">Updated <time datetime="2026-10-22">October 22, 2026</time></p>
  </header>
  <div class="tide-content-page__layout">
    <!-- Optional nav.tide-content-page__contents -->
    <div class="tide-content-page__body">
      <article class="tide-prose"><h2 id="arrival">Arrival</h2><p>…</p></article>
      <footer class="tide-content-page__footer">
        <p>Page context.</p>
        <nav class="tide-content-page__footer-links" aria-label="Related pages">
          <a href="index.html">Find events</a>
        </nav>
      </footer>
    </div>
  </div>
</main>
```

At 60rem and above, a supplied contents nav occupies a 12rem column with a 48px gap. The title aligns with the reading column. The nav is sticky only when the viewport is also at least 40rem tall; short windows keep it in document flow. A long sticky contents list can scroll within the viewport, with 24px breathing room above and below. Below 60rem the contents precede the body. Omit the nav for shorter pages; the layout becomes one column automatically. No extra empty column or placeholder is required.

Give the contents nav a visible heading and `aria-labelledby`, use a semantic UL of real fragment links, and give destination headings unique IDs. The example uses `tabindex="-1"` on destinations so native fragment navigation can place focus without extra Tab stops. Keep a single page H1, a main landmark and a skip link. The existing `.tide-skip-link` is now shipped in `css/utilities.css`, rather than belonging only to documentation styling. Contents are native links; there is no simulated tab system or automatic active-section state.

The app’s existing motion preference controls smooth document scrolling. Standalone kit fixtures use native instant fragment navigation. Back, modified clicks, opening new tabs and browser history retain native behavior. Footers must contain working destinations; omit unpublished policy links rather than adding dead placeholders.

Supported layout extension points: `--tide-content-page-width` (70rem) and `--tide-content-page-contents-width` (12rem). These are composition dimensions, not theme palette inputs. Keep components’ internal scales intact when composing a new page.

## Example and scope

The help page covers finding events, dates/categories, preview selection, access questions, admission tables, changed plans and organizer guidance. It explicitly describes which features work in the current preview. It does not claim live booking, support messages or event submission. Help content is a realistic fixture; privacy and terms copy require the eventual service’s actual data practices.

The kit’s `theme-mode/frames/help.html` and `prose.html` use the same source across all six modes. The consuming app generates `help.html` and `help-review.html` at the root and in every theme directory. The app’s review gallery is presentation only; its theme links and viewport frames are not part of the prose API.

## Verification

Run the kit and app build/check commands from their READMEs. Check focus/fragment links, no-contents layout, exclusions, nested lists, images, long URLs, tables and code at 320px, normal phone, tablet and desktop widths, plus enlarged text. Verify all themes and modes without adding theme selectors. Actual observations and limits are recorded in [the historical content QA record](CONTENT-EVIDENCE.md); feature-support research remains separate in `COMPATIBILITY.md`.

## Release and preservation

Kit 1.2.0 adds Prose and the Content page composition. App 1.3.0 consumes them directly, with no duplicated prose styles or browser scripts on help pages. No existing primitive/theme inputs change. Kit 1.1.0 and app 1.2.1 ZIPs, the original 176-file foundation and the 263-file three-event baseline remain preserved.
