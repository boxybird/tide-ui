# Architecture and ownership

Tide UI and application kits are separate deliverables. The reference site documents Tide; it is not an application kit. Each application kit consumes the same canonical UI distribution without forking it.

| Home | Owns |
| --- | --- |
| `packages/tide/` | UI kit: public component CSS, semantic tokens, themes, canonical HTML recipes, registry, assets and contracts |
| `site/` | UI-kit documentation rendering and presentation |
| `application-kits/lineup/` | Lineup application kit, layout family option 1: responsive page composition, authored event/result states, routing fixtures, assets, templates, contracts and application tests |
| `tools/` | Repository integration: build, checks, local preview and packaging |

Tide is the source of truth. Application work adopts documented component recipes/options without changing UI-kit CSS, recipes, tokens, palette values or ownership rules. Private application layout is distinct from shared component appearance. Kit extensions require separately authorized UI-kit work with canonical CSS/HTML, states, registration and all-theme specimens. Integration-test path changes during a move do not alter the kit API or generated stylesheet.

Build order is UI kit → reference site → Lineup, driven by `tools/build.py`. Output goes only to ignored `build/`. Lineup sources live solely in `application-kits/lineup/`; its generated output retains `build/events/` and native `/events/` preview URLs. Historical migration hashes keep their original paths as provenance. Old studies are not build dependencies.

The kits have independent versions: Tide 1.10.0 and Lineup 2.0.4. “Option 1” identifies a layout family, not version 1. Future alternatives get named sibling homes with their own application versions. Tags/release assets preserve snapshots, rather than copied implementation folders. See the [application-kit guide](../application-kits/lineup/README.md).

Every theme resolves the same semantic names. Tide, Bumble, Slate, Grove and Iris each have light/dark appearance; themes do not redefine type, spacing or radius. Manrope, square controls, neutral notice borders and unframed event compositions remain shared decisions.

Lineup bundles five registered `src/styles/` modules into one application stylesheet. Its private `tide-app`, `tide-app-document`, `tide-lineup` and `tide-venue` blocks own composition and placement. See [component ownership](../application-kits/lineup/docs/COMPONENT-OWNERSHIP.md) and [the responsive audit](../application-kits/lineup/docs/AUDIT.md).

Build-time HTML expands registered partials through the dependency-free renderer in `application-kits/lineup/tools/`. All 64 routes use one document shell; 62 list/venue/event/saved/result routes share one workspace. Three unique venue/help/submission fragments remain in `src/pages/`. All 54 event details consume structured samples and a common recipe. Eleven submission fields consume registered form partials. Plain values are escaped; unknown/missing/cyclic/invalid includes fail. See [templates](../application-kits/lineup/docs/TEMPLATES.md), [details](../application-kits/lineup/docs/DETAILS.md) and [pages](../application-kits/lineup/docs/PAGES.md).

Browser deliverables contain zero JavaScript. Native HTML/CSS owns links, history, fragments, scrolling, popovers, reset, validation and file selection. Category/empty layouts are authored result pages. Node/Python are development tooling only. Retired search, storage and message engines are not current behavior. See [browser policy](NO-BROWSER-JAVASCRIPT.md).

Normal checks verify fresh output, associations, component ownership, all-theme parity, contrast, byte budgets, local references and the browser-script boundary, then run Python/Node tests. Optional history verification is separate. Browser evidence is Chromium on Windows; Firefox/Safari, physical devices and screen readers remain deferred unless explicitly recorded otherwise.
