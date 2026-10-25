# Repository migration verification

Verified on October 25, 2026. The structural migration retains kit 1.3.0 and app example 1.1.0 behavior/appearance while establishing permanent source homes.

- [Source parity](source-parity.json): all 420 app HTML documents and 105 kit/site HTML documents match the prior output exactly after normalizing local navigation/asset paths. The compiled CSS and complete app runtime retain their SHA256 hashes. The new app review landing page is the additional 526th document.
- [Fresh-source verification](fresh-build.json): the copied maintained source builds and passes checks with no `.git`, archived directories or old study paths present. Python and Node are selected through normal executables/PYTHON, with no hardcoded personal runtime path.
- Current root checks validate 526 HTML files, 36,171 local HTML references, BEM/ownership, native labels/associations, component fixtures, semantic roles, token bindings, documentation links and paired palette contrast. Fourteen palette/markup tests and sixteen sample-search assertions pass.
- [New browser observations](browser.json): thirteen Chromium checks cover all six modes in both the kit and venue app, desktop geometry and sticky hit tests, live draft/apply, scoped event/return URLs, no-results guide retention, Reset, tablet Escape/focus, the phone venue fragment and the full-screen phone event with a correctly loaded organizer image.
- At 1440×900, list top 117px and list/Show events bottom 866px match the previous release. The native 10px gutter gives the established 34px bottom allowance. At the venue month handoff, the outgoing heading begins at 158.333px underneath the 249px summary bottom; summary hit tests resolve correctly. Phone venue target focuses at 121px below the 97px header; phone event hero is 844px high.
- The design-history tag identifies all 5,300 tracked files at commit `60864d0`; its tree/object inventory and standalone Git bundle verify. Additional ignored non-cache artifacts have a separate verified local archive. Local dependency caches were retained in an ignored holding directory.

Reviewed captures: [desktop](desktop.png), [component reference](kit.png), [phone event](phone.png). Source/generation changes do not rely on screenshot assertions alone.

Limits remain explicit: current native visual evidence is Chromium on Windows. Firefox/Safari, physical-device and screen-reader checks are deferred. Browser zoom was unavailable through the connected browser. GitHub Actions is configured for independent Windows/Ubuntu source builds; a locally passing check is not presented as proof that a hosted job has already run. No UI publication, npm publication, live data integration or PWA service was added.
