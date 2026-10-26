# Tide UI

A framework-free HTML and CSS UI kit with semantic OKLCH colors, BEM components and five themes—Tide, Bumble, Slate, Grove and Iris—each with light, dark and system appearance. The documentation and Burque events example consume the same generated stylesheet.

Kit **1.4.0** · Events example **1.1.5** · MIT licensed. This is a local sample interface, without live event data, submissions, accounts or booking.

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

Open the [UI kit](http://127.0.0.1:4187/site/index.html), [events example](http://127.0.0.1:4187/events/app/index.html?preview-filters=open) or [all-theme app review](http://127.0.0.1:4187/events/index.html). The reference site includes Foundations, Components, Screens, Coverage, Tokens, Themes and Extend. `PORT` changes the local server port.

## Repository

| Home | Owns |
| --- | --- |
| `packages/tide/` | CSS modules, theme inputs, canonical HTML recipes, component registry, fonts/assets/licenses and component contracts |
| `site/` | Reference-site builder and documentation presentation CSS |
| `examples/events/` | Sample app HTML, app-only layout CSS, search/navigation behavior and authored fixtures |
| `tools/` | Portable build, contract checks, local preview, packaging and optional history verification |
| `docs/` | Architecture, contribution/versioning rules, design decisions and migration evidence |
| `build/` | Generated distribution, reference site, example and reports; ignored by Git |
| `dist/` | Generated release ZIP and checksums; ignored by Git |

Edit named sources and rebuild. Generated theme/mode copies are never edited or committed. The kit supplies CSS and HTML recipes; JavaScript integration belongs to the consuming app. Python and Node are build tools, not browser dependencies.

## Use the CSS

After building, copy `build/tide/css/` and `build/tide/assets/` together, keeping their relative arrangement and the included licenses.

```html
<html lang="en" data-theme="tide" data-mode="dark">
  <head><link rel="stylesheet" href="tide/css/tide.css"></head>
  <body class="tide"><button class="tide-button" type="button">Find events</button></body>
</html>
```

Use the same semantic tokens in every theme. Set `data-mode="light|dark|system"`; omitting it follows system appearance. See [package guide](packages/tide/README.md), [architecture](docs/ARCHITECTURE.md), [contributing](CONTRIBUTING.md) and [changelog](CHANGELOG.md).

## Design history

The complete earlier project is preserved at Git tag **`design-history/2026-10-25`**, including all studies, version archives and the approved originals. The active tree contains the maintained sources. See [recovery instructions and important milestones](docs/DESIGN-HISTORY.md).

## Verification

`npm run check` validates generated output, HTML associations, component ownership, local references, theme parity, contrast and search behavior. It does not require old study directories. App JavaScript cleanup is recorded in [runtime verification](docs/refactors/app-javascript/VERIFICATION.md). Venue and utility extraction is recorded in [page verification](docs/refactors/utility-pages/VERIFICATION.md). Individual event template extraction is recorded in [detail verification](docs/refactors/event-details/VERIFICATION.md). Shared app HTML extraction is recorded in [template verification](docs/refactors/app-html/VERIFICATION.md). App-only CSS cleanup is recorded in [refactor verification](docs/refactors/app-css/VERIFICATION.md). Browser observations and limits are recorded in [migration verification](docs/migration/VERIFICATION.md) and the kit's [compatibility contract](packages/tide/docs/COMPATIBILITY.md). Support targets current Chrome, Firefox and Safari; current visual evidence is Chromium on Windows. Native Firefox/Safari checks remain deferred, rather than reported as passing.
