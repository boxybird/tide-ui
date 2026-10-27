# Zero browser JavaScript

The Tide kit, its canonical HTML specimens, the reference site and the events example must ship and load zero browser JavaScript. This policy covers external or inline scripts, JavaScript modules, inline event handlers, JavaScript URLs and executable SVG hooks. Node.js and Python remain local development/build/test tools only; their presence does not make them browser dependencies.

`npm run check` scans browser source/output boundaries for executable script hooks and `.js`/`.mjs`/`.cjs` files. Kit packaging runs these checks before creating an archive. Canonical kit HTML cannot import documentation-site scripts. Behavior inventories for the site and example are empty.

## Audit and replacements · 2026-10-26

| Removed browser responsibility | Native or build-time replacement |
| --- | --- |
| Runtime creation of count/month spans | Escaped build-time HTML partials |
| Summary/month-height observers | Summary outside the native feed scroller; month headers stick at its top |
| Occupied-scrollbar measurement and viewport writes | CSS `scrollbar-gutter`, bounded grid rows and viewport units |
| Desktop assembly and responsive control movement | One authored panel and native disclosures; no drawer controller |
| Click interception, delayed navigation and custom reading history | Native links, fragments and browser Back/history |
| Filtering engine and fetched first-result previews | Authored all/category/empty-result documents with complete HTML previews |
| Venue DOM rewriting | Authored route/venue context and links |
| Photo/session/message hooks | Authored image assets and static page states |
| Documentation validation/toggle/file controllers | Native constraint validation, checkbox/radio state, reset and file chooser; static summary examples |

The initial audit found two kit HTML specimens importing a site-only demo script. Those imports and the site demo script are removed. The kit CSS itself had no JavaScript runtime.

## Behavior boundaries

Arbitrary text/date matching, live counts, persistent saved state, custom modal draft/cancel logic and query-driven photo inspection are not CSS features. They are removed from this native UI specimen rather than reimplemented through hidden scripts or a new service. The events example clearly labels its controls as examples and links to authored result pages. Query parameters are not interpreted by browser code. The same 54 event records and original native event paths remain; four additional category/empty state pages support interface review.

A native form reset restores authored values, including checked fixture defaults. Native input validation covers supported required/type constraints; a From/Through relationship is not dynamically validated. Populated error summaries are authored states, distinct from native browser messages. Native file selection does not promise custom size/content checks. No operational backend is added.

## Verification limits

Build/contract checks scan all generated modes and source boundaries. Browser observations cover Chromium on Windows; native Firefox/Safari, physical devices and screen readers remain deferred. Static specimen states must never be described as a working data service or as live behavior.
