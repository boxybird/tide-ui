# Tide HTML and CSS kit · 1.10.0

All public blocks have required [ownership contracts](docs/OWNERSHIP.md). The [final normalization pass](docs/KIT-CLOSEOUT.md) covers remaining components and page rhythm, with an all-theme `frames/kit-closeout.html` matrix. See [completion and verification limits](docs/NORMALIZATION-STATUS.md).

Cards, dates, calendar groups and result summaries have a [listing contract](docs/LISTINGS.md) and all-theme `frames/listing-states.html` matrix. Canonical card/date recipes stay separate from consumer viewport composition.

The canonical maintained package. Five named themes—Tide, Bumble, Slate, Grove and Iris—share semantic roles, typography, geometry and component HTML. Each theme supports light, dark and system appearance. The kit ships no browser JavaScript.

From the repository root run `npm run build`, `npm run check`, then `npm run dev`. The CSS distribution is generated at `build/tide/`; the reference site is generated at `build/site/`. To consume the kit, copy its `css/`, `assets/` and `licenses/` together. The CSS entry point is `css/tide.css`. The repository and its local documentation/examples are the maintained deliverables.

| Source | Purpose |
| --- | --- |
| `css/` | Named source modules; components consume semantic roles rather than palette inputs |
| `tokens/themes.json` | Editable theme seeds/overrides; every named theme requires both modes |
| `templates/` | Canonical component/composition specimens, content HTML and shared Filter panel recipe |
| `component-manifest.json` | BEM names, variants, states, ownership and fixture/contract registration |
| `tools/compiler.py`, `palette.py` | Paired palette resolution, contrast gates and emitted color roles |
| `tools/build.py` | CSS distribution build, independent of documentation and design archives |
| `tools/contracts.py`, `test_*.py` | Accessible-markup/ownership rules and regression checks |
| `assets/`, `licenses/` | Fonts, icons and illustrative assets with original licenses |
| `docs/` | Naming, theming, components, content, filtering and extension contracts |

The repository migration preserved the compiled 1.3.0 CSS exactly; kit 1.4.0 revises Bumble Light and adds three theme pairs. See [color design guidance](docs/COLOR-DESIGN.md). Existing composed specimens remain in the package so their registry references stay authoritative; site-only rendering and presentation CSS live in `site/`. Historical one-time import scripts and prior version ZIPs are recoverable from the design-history tag.

Page recipes in [PAGE-PATTERNS.md](docs/PAGE-PATTERNS.md) add shared venue profile/card, site header and error-summary compositions, plus event-condition and native-control specimens. Canonical specimens and the reference site are native HTML/CSS only. See [zero-browser-JavaScript policy](docs/BROWSER-POLICY.md).

Read [theming](docs/THEMING.md), [components](docs/COMPONENTS.md), [extension rules](docs/EXTENDING.md), [Prose and Content page](docs/CONTENT.md) and [Filter panel/patterns](docs/SEARCH-FILTERS.md). In these original contracts, former paths such as generated `tide-dark/frames/` refer to `build/site/tide-dark/frames/`; generated colors/reports now live in `build/tide/tokens/` and `build/reports/`. Run build/check commands from the repository root. These location changes do not change the component API.

Regular and compact action geometry, typography, native states and compatibility aliases are documented in [the button contract](docs/BUTTONS.md).

Badges, notices, toast specimens and empty states share an explicit [feedback contract](docs/FEEDBACK.md) and all-theme `frames/feedback-states.html` matrix. Native links are interactive; messages and status labels are authored states.

Fields, choices, chips, disclosures and native file/error states share explicit typography and documented precedence. See [the form contract](docs/FORMS.md) and the all-theme `frames/form-states.html` matrix. This normalization changes kit presentation; application layouts remain owned by their consumers.
