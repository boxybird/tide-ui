# Separate successor app release 1.1.0

This app combines only the approved baseline, accepted sticky-heading correction and accepted venue navigation. It is a reviewable successor, not yet a user-selected replacement baseline. Keep all frozen inputs untouched, including their QA/docs/archives and bytecode. Always run Python with `-B`.

Edit `src/pages/` and `src/runtime/`, then run `tools/build.py`. The `app/`, `themes/`, `runtime/` and root review HTML are generated. Do not run the one-time importer again. Read-only dependency: `../shared-filter-release/kit/` 1.3.0. Do not add public kit components or redefine their selectors.

Retain baseline host CSS bytes, all themes/tokens/components, unframed panes, native scrolling/links/GET state, native scrollbar measurement, Show events alignment and phone/tablet placement. Keep complete-feed isolation local beneath the permanent summary, with existing measured sticky offsets. Preserve exact venue IDs, scoped Reset/return behavior and the guide when filters match nothing. Keep all data sample-labeled and real venue facts attributed separately.

Run `python -B tools/check.py` and browser checks before packaging. New output/QA belongs only here. Native Firefox/Safari, physical-device and screen-reader checks remain deferred. Document actual tested scope rather than implying universal coverage.
