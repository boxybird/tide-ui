# Tide UI

A framework-free HTML and CSS UI kit with semantic OKLCH colors, BEM components and five themes—Tide, Bumble, Slate, Grove and Iris—each with light, dark and system appearance. The reference site and derived application kits consume the same generated stylesheet.

Tide UI kit **1.12.0** · [Lineup application kit](application-kits/lineup/README.md) **2.1.6**, layout family **option 1** · MIT licensed. This is a local sample interface, without live event data, submissions, accounts or booking.

Kit normalization contracts: [buttons](packages/tide/docs/BUTTONS.md), [fields, choices, chips, disclosures and file/error states](packages/tide/docs/FORMS.md), and [badges, notices, toast specimens and empty states](packages/tide/docs/FEEDBACK.md). [Cards, dates, calendar groups and results](packages/tide/docs/LISTINGS.md) have a dedicated matrix too. Each has all-theme specimens and regression checks. See [completion status and verification limits](packages/tide/docs/NORMALIZATION-STATUS.md) for completed scope and browser-testing limits.

## Project scope

The maintained deliverables are the UI kit, its documentation and best practices, and pages composed from the kit: event details, venue pages, filter bars, event listings and other interface examples. Sample content and local interactions support design and evaluation. This remains an ongoing GitHub repository for iteration and reuse.

Hosting, deployment, production launch, live event sourcing or ingestion, backend services, operational submissions/moderation, accounts and ticketing services are outside project scope. These are not deferred milestones. Submission, review and saved-page specimens are UI examples.

A UI deliverable is finished when its canonical sources and ownership are clear, documentation and relevant specimens are current, and applicable build, contract and interaction checks pass with testing limits recorded. Packaging is optional. Further work should address a concrete kit or example-page need: components, tokens, themes, accessibility, responsive composition, reusable patterns or documentation. Coverage is an inventory of UI examples, not a service roadmap.

## Start

Requires Node.js 18+ and Python 3.10+. There are no npm or Python dependencies to install. Set `PYTHON` if your interpreter has a nonstandard executable name or location.

```sh
npm run build
npm run check
npm run dev
```

Open the [UI kit](http://127.0.0.1:4187/site/index.html), [events example](http://127.0.0.1:4187/events/app/index.html) or [all-theme app review](http://127.0.0.1:4187/events/index.html). The reference site includes Foundations, Components, Screens, Coverage, Tokens, Themes and Extend. `PORT` changes the local server port.

## Repository

| Home | Owns |
| --- | --- |
| `packages/tide/` | CSS modules, theme inputs, canonical HTML recipes, component registry, fonts/assets/licenses and component contracts |
| `site/` | Reference-site builder and documentation presentation CSS |
| `application-kits/` | Named application kits derived from Tide, with independent versions; [index](application-kits/README.md) |
| `application-kits/lineup/` | Lineup option 1: application layout, templates, authored results, sample content/assets, docs and tests |
| `tools/` | Portable build, contract checks, local preview, packaging and optional history verification |
| `docs/` | Architecture, contribution/versioning rules, design decisions and migration evidence |
| `build/` | Generated distribution, reference site, example and reports; ignored by Git |
| `dist/` | Generated release ZIP and checksums; ignored by Git |

Tide is the UI source of truth; application-kit work does not change its component sources, recipes or tokens. The application has one canonical home and keeps its existing `/events/` preview URLs. See the [Lineup audit](application-kits/lineup/docs/AUDIT.md).

Edit named sources and rebuild. Generated theme/mode copies are never edited or committed. The kit, reference specimens and events example contain zero browser JavaScript, enforced by checks. Python and Node are development tools, not browser dependencies. See [browser policy and audit](docs/NO-BROWSER-JAVASCRIPT.md).

## Use the CSS

After building, copy `build/tide/css/` and `build/tide/assets/` together, keeping their relative arrangement and the included licenses.

```html
<html lang="en" data-theme="tide" data-mode="dark">
  <head><link rel="stylesheet" href="tide/css/tide.css"></head>
  <body class="tide"><button class="tide-button" type="button">Find events</button></body>
</html>
```

Use the same semantic tokens in every theme. Set `data-mode="light|dark|system"`; omitting it follows system appearance. See [package guide](packages/tide/README.md), [architecture](docs/ARCHITECTURE.md), [contributing](CONTRIBUTING.md) and [changelog](CHANGELOG.md).

A [page-recipe guide](packages/tide/docs/PAGE-PATTERNS.md) covers reusable venue compositions, form validation, event conditions, site navigation and native control states. Open the reference site’s Screens section for all-theme examples and local demonstrations.

## Design history

The complete earlier project is preserved at Git tag **`design-history/2026-10-25`**, including all studies, version archives and the approved originals. The active tree contains the maintained sources. See [recovery instructions and important milestones](docs/DESIGN-HISTORY.md).

## Verification

`npm run check` validates generated output, HTML associations, component ownership, local references, theme parity, contrast, authored result states and the zero-browser-script boundary. It does not require old study directories. App JavaScript cleanup is recorded in [runtime verification](docs/refactors/app-javascript/VERIFICATION.md). Venue and utility extraction is recorded in [page verification](docs/refactors/utility-pages/VERIFICATION.md). Individual event template extraction is recorded in [detail verification](docs/refactors/event-details/VERIFICATION.md). Shared app HTML extraction is recorded in [template verification](docs/refactors/app-html/VERIFICATION.md). App-only CSS cleanup is recorded in [refactor verification](docs/refactors/app-css/VERIFICATION.md). Browser observations and limits are recorded in [migration verification](docs/migration/VERIFICATION.md) and the kit's [compatibility contract](packages/tide/docs/COMPATIBILITY.md). Support targets current Chrome, Firefox and Safari; current visual evidence is Chromium on Windows. Native Firefox/Safari checks remain deferred, rather than reported as passing.

Regular and compact action geometry, typography, native states and compatibility aliases are documented in [the button contract](packages/tide/docs/BUTTONS.md).
