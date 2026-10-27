# Contributing

Browser deliverables must contain zero JavaScript: no script files, script imports, inline handlers or JavaScript URLs in the kit, documentation specimens or events example. Node/Python are development tools only. Prefer native HTML and CSS; author static UI states where behavior would require an application engine. See [browser policy](docs/NO-BROWSER-JAVASCRIPT.md).

Preserve the [loading and performance contracts](docs/LOADING-PERFORMANCE.md). Budget changes require review; replacing a lossless asset requires decoded pixel verification and updated provenance. Normal checks include local HTTP regression tests.

Use `main` as the only lasting branch. Any temporary working branch must be merged and removed. Versioned history belongs in tags/release assets, not sibling implementation folders.

Contributions serve the UI kit, its documentation/best practices or example pages built with it. See [project scope and completion criteria](README.md#project-scope). Service operations are not completion criteria or a follow-on backlog.

1. Edit canonical sources in `packages/tide/`, `site/` or `application-kits/lineup/` according to ownership.
2. Reuse an existing component before adding one. New kit components need a BEM block, CSS/HTML source, variants/states, accessibility/behavior contract, registry entry and specimens in every theme/mode. Remove duplicate app styling when adopting a pattern.
3. Run `npm run build` and `npm run check`. Inspect relevant keyboard behavior and all affected theme/mode/viewport states. Record actual browser coverage; do not equate source checks with assistive-technology or cross-browser testing.
4. Update component contracts, changelog and version for the affected package/example. Keep generated `build/`, `dist/`, caches and routine screenshots out of Git. Keep a small amount of reviewed regression evidence when it helps explain an accepted contract.
5. When a downloadable kit/example snapshot is useful, package with `npm run package`. ZIPs/checksums support repository review and reuse; packaging is optional for UI completion.

Keep API-preserving fixes in patch versions, additive components/themes in minor versions, and incompatible public markup/token/behavior changes in major versions. The UI kit and each named application kit have independent versions. Lineup is layout family option 1, not version 1. Application-kit work must not modify Tide component sources, tokens, recipes, themes or registry; adopt documented kit options in application markup and record gaps in its audit. Integration-test paths may follow a source move without changing the UI-kit API or distribution. Repository-only moves need a changelog entry and parity verification; they do not silently change component APIs.

Never rerun an historical importer against maintained sources. Use the optional history verifier and recovery instructions when older studies are needed. Never rewrite published history as part of routine cleanup.
