# Tide UI — maintained repository

The user authorized repository cleanup on 2026-10-25. The complete earlier project (5,300 tracked files) is preserved at Git tag `design-history/2026-10-25`, commit `60864d0`. A standalone recovery bundle lives in `.git/design-history-2026-10-25.bundle` on this machine. Archived studies belong in that tagged history; do not recreate version folders in the active tree or run historical writers against current sources.

## Current homes

- `packages/tide/`: maintained kit1.3.0 CSS modules, theme inputs, canonical HTML recipes, registry, contracts and tests.
- `site/`: reference-site builder and presentation; Foundations / Components / Screens / Coverage / Tokens / Themes / Extend.
- `examples/events/`: sample app1.1.2, including accepted sticky heading and Sunshine Theater patterns. App behavior/layout remains separate from kit components.
- `tools/`: portable build/check/dev/package tools. Normal checks never import archived studies or require their paths.
- `build/` and `dist/`: ignored generated outputs/artifacts. Never edit or commit generated theme copies.

Run `npm run build`, `npm run check`, `npm run dev` from the root. Node18+ and Python3.10+ are required; no dependencies need installation. `PYTHON` can select the interpreter. Local preview is port4187: `/site/index.html` and `/events/app/index.html?preview-filters=open`. `npm run verify:history` is a separate optional archive check.

## Contracts

Use BEM `tide-` names, semantic theme roles, named type/spacing/radius inputs, modern supported CSS and accessible native HTML. Tide, Summer and Bumble each require light/dark modes. Preserve Manrope, square controls, neutral notice borders and unframed event panes; no colored left callout stripe. Reusable discoveries require CSS/HTML/state/behavior homes, registration, all-theme specimens and removal of duplicated app styles.

Preserve the app's bounded left panes, natural right document, native scrollbar measurement, 24px-plus-occupied-gutter bottom clearance, Show events alignment, responsive filter flyout and one original control set. Complete-feed isolation remains below the permanent desktop summary, with measured sticky offsets. Keep exact venue IDs, scoped Reset/return/explicit exit behavior and useful venue information when filters match no events. All54 event entries are authored samples, with real venue facts attributed separately.

App 1.1.1 consolidates app CSS into five registered `src/styles/` modules and purpose-based app/lineup/drawer/venue families. Do not restore study aliases or old comparison variants. Kit sources remain unchanged. Preserve the documented native IDs/URLs, shared controls, session compatibility and measured sticky/gutter inputs. App 1.1.2 uses registered `src/templates/` partials for header, filters and lists, `data/event-list.json` for canonical list cards and `data/pages.json` for non-event routes. Keep route-specific details in `src/pages/`. Do not paste shared markup back into page sources. The build-time renderer escapes text and rejects missing/cyclic/invalid includes; no browser templating or additional framework is needed. Current browser evidence is Chromium; Firefox/Safari, physical-device and screen-reader checks remain deferred.

End every completed repository task with `main` as the only branch. Tags/releases preserve versions. Never force-push or rewrite published history for routine cleanup. Do not publish the preview or npm package unless requested. Follow CONTRIBUTING.md and keep README/CHANGELOG/contracts current.
