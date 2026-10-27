# Start from Lineup

Lineup 2.1.1 is layout family option 1, derived from Tide UI 1.10.0. Burque Events supplies realistic authored sample content for evaluating the interface. Both kits remain separate, with independent versions.

1. From the repository root, run `npm run build`, `npm run check` and `npm run dev`. Open `/events/app/index.html`; `/events/index.html` exposes all five themes in light/dark modes.
2. Start with `data/pages.json` for route/collection context and `src/templates/document.html` / `workspace*.html` for composition. All 67 documents are generated from those sources. Only venue/help/submission need the three authored `src/pages/` fragments.
3. Replace sample content in `data/events.json`, detail presentations, submission-field definitions and authored fragments as appropriate. The renderer escapes text; do not put raw HTML in sample JSON. Preserve valid native links, labels, IDs and associated field hints.
4. Adjust private layout in the five registered `src/styles/` modules. Use Tide's semantic roles and named type/spacing inputs. Adopt public kit recipes and supported modifiers in markup; do not redefine public component type/spacing or change `packages/tide/` while working on Lineup.
5. Review the [responsive audit](AUDIT.md), [ownership](COMPONENT-OWNERSHIP.md), [desktop layout](DESKTOP-LAYOUT.md) and [native drawer](FILTER-DRAWER.md) before changing pane geometry or responsive behavior. Rebuild and run normal checks; record the actual browsers/devices/states exercised.

Use `header.html` and `skip-link.html` for Tide's Site header and Skip link recipes. Route context derives `aria-current="page"` from the actual link destination; do not mark a collection link as the current detail/result page. Main links remain available on narrow screens. See [navigation and title ownership](NAVIGATION-TITLES.md).

The application ships native HTML/CSS only. Links, fragments, browser Back, native controls, popover dismissal, reset, validation and file selection work locally. Category and empty results are authored pages. Arbitrary search/date matching, persistent saved state and operational submission are outside this specimen's scope; inputs are explicitly labeled examples. This is a reusable UI starting point.

Keep application releases in tags/artifacts. A different application layout belongs in its own named sibling directory under `application-kits/`, with its own ownership and version. Do not copy or fork Tide into it. The root builder currently builds Lineup; adding another kit includes registering its build/check/output ownership in repository tooling.

For a scoped working session, invoke your personal guard with `Use $application-kit-scope for application-kits/lineup/.` The UI kit, shared tooling and sibling applications remain read-only; canonical edits and current application docs belong here.
