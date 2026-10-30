# Start from Lineup

**Current 2.4.0 boundary:** the approved map is now in `src/map/` and builds from the current Lineup templates. Review `/events/app/venues.html` on port 4187. There is no active separate consumer or copied source snapshot. Only the venue directory loads browser modules; prior no-script/map-provider-exclusion statements below describe the earlier native baseline. The current [source-of-truth contract](SOURCE-OF-TRUTH.md) takes precedence. Native event/search journeys and service limits are unchanged.


Lineup 2.4.0 is layout family option 1, derived from Tide UI 1.12.0. Tag `lineup-v2.3.0` preserves the approved venue list/map foundation for further iteration. Burque Events supplies realistic authored sample content for evaluating the interface. Both kits remain separate, with independent versions. Start with the [handoff contract](HANDOFF.md) for product-copy, native CSS behavior, fixture provenance and service integration boundaries.

The [compact-header contract](COMPACT-HEADERS.md) covers the selected workspace and its canonical utility recipe.

1. From the repository root, run `npm run build`, `npm run check` and `npm run dev`. Open `/events/app/index.html`; `/events/index.html` exposes all five themes in light/dark modes.
2. Start with `data/pages.json` for route/collection context and `src/templates/document.html` / `workspace*.html` for composition. All 73 documents are generated from those sources. Venue profile, venue directory, Help and submission use the four authored `src/pages/` fragments.
3. Replace sample content in `data/events.json`, detail presentations, submission-field definitions and authored fragments as appropriate. The renderer escapes text; do not put raw HTML in sample JSON. Preserve valid native links, labels, IDs and associated field hints.
4. Adjust private layout in the five registered `src/styles/` modules. Use Tide's semantic roles and named type/spacing inputs. Adopt public kit recipes and supported modifiers in markup; do not redefine public component type/spacing or change `packages/tide/` while working on Lineup.
5. Start from the completed [Tide alignment baseline](TIDE-ALIGNMENT.md). Personalization is a separate task and must preserve canonical component adoption. Review the [responsive audit](AUDIT.md), [ownership](COMPONENT-OWNERSHIP.md), [desktop layout](DESKTOP-LAYOUT.md) and [native drawer](FILTER-DRAWER.md) before changing pane geometry or responsive behavior. Rebuild and run normal checks; record the actual browsers/devices/states exercised.

Use `header.html` for Lineup's private header grid inside Tide's Site header shell, and `skip-link.html` for the Skip link recipe. Keep `extensions/navigation.css` loaded after the core kit CSS for the reviewed navigation action states; see [header navigation](HEADER-NAVIGATION.md). The application does not consume or override Tide's centered header modifier. Route context derives `aria-current="page"` from the actual link destination; do not mark a collection link as the current detail/result page. Main links remain available on narrow screens. See [navigation and title ownership](NAVIGATION-TITLES.md).

`navigation-items.html` authors the link items once for inline and mobile presentations. The mobile popover adopts Tide's existing Panel extension; the application builder emits an unchanged generated dependency copy rather than maintaining application-owned Panel CSS. See the [mobile navigation contract](MOBILE-NAVIGATION.md) for mounting, native behavior and the 34rem breakpoint.

Filter footer spacing/layout stays in Tide. Use the private child wrappers in `filter-rail.html` for narrow viewport clearance; keep public footer/status/count classes free of private appearance aliases. The split-tablet height input accounts for the visible Filters control. See [the repair contract](FILTER-FOOTER-TABLET.md).

The application ships native HTML/CSS only. Links, fragments, browser Back, native controls, popover dismissal, reset, validation and file selection work locally. Category and empty layouts remain authored reference pages, available from the kit review entry rather than a tutorial menu inside the application. Search uses ordinary product labels and a native GET form contract. Arbitrary search/date matching, persistent saved state and operational submission remain service integration boundaries, documented outside the product UI. The [consumer integration guide](CONSUMER-INTEGRATION.md) maps the current markup and responsibilities for an independent consumer adding enhanced navigation, search or collection loading.

Keep application releases in tags/artifacts. A different application layout belongs in its own named sibling directory under `application-kits/`, with its own ownership and version. Do not copy or fork Tide into it. The root builder currently builds Lineup; adding another kit includes registering its build/check/output ownership in repository tooling.

## Consuming-site upgrades

Lineup is a maintained application kit. A website should record the Lineup release it consumes and be able to adopt later releases during its own update cycle. Releasing a website does not freeze the kit, and a new kit release does not automatically update a consuming website. Tide, Lineup and the consuming website have separate version and change ownership.

Lineup releases should describe reusable changes and any required consumer migration in their changelog. The current HTML/CSS workflow uses reviewed source updates; automatic downstream migration tooling is not implemented. Use the [integration ownership and upgrade guidance](CONSUMER-INTEGRATION.md) to review consumer adaptations. Private implementation references do not become a version-independent integration API; any such API needs its own explicit contract and review.

For a scoped working session, invoke your personal guard with `Use $application-kit-scope for application-kits/lineup/.` The UI kit, shared tooling and sibling applications remain read-only; canonical edits and current application docs belong here.
