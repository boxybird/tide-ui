# Tide UI and derived application kits

The complete earlier project is preserved at tag `design-history/2026-10-25`, commit `60864d0`, and `.git/design-history-2026-10-25.bundle`. Archived studies stay in tagged history; do not recreate version folders or run historical writers against current sources.

## Scope and ownership

- `packages/tide/`: Tide UI kit 1.10.0, the source of truth for components, CSS, tokens, themes, recipes, registry, assets and contracts. Theme research lives in `packages/tide/docs/COLOR-DESIGN.md`; preserve the accepted Bumble Dark palette.
- `site/`: UI-kit documentation and reference presentation; Foundations / Components / Screens / Coverage / Tokens / Themes / Extend.
- `application-kits/lineup/`: Lineup application kit 2.0.4, layout family option 1. Burque Events is its authored sample website. Owns application composition, responsive layout, templates, fixtures, assets, docs and tests. This replaces the former `examples/events/` source home.
- `application-kits/README.md`: application-kit index and independent-version rules. Future layout alternatives get named siblings, not copied version directories.
- `tools/`: portable build/check/dev/package integration. `build/` and `dist/` are ignored generated output; never edit or commit generated theme copies.

UI-kit work and application-kit work are distinct. While working on an application kit, do not modify Tide CSS, tokens, palettes, recipes, registry or public component contracts. Use documented kit options in application markup; record gaps in the application audit. Kit extensions require a separate authorized UI-kit task. Source-move updates to shared integration-test paths do not change the UI-kit API or distribution.

Hosting, deployment, production launch, ingestion, backend services, operational submissions/moderation, accounts and ticketing are outside scope. They are not deferred completion milestones. Saved/submission specimens demonstrate UI patterns. A deliverable is finished when its sources/ownership, docs/specimens and applicable build/contract/interaction checks are current, with testing limits recorded.

## Development

Run `npm run build`, `npm run check`, `npm run dev` from the root. Node18+ and Python3.10+ are required; no dependencies need installation. `PYTHON` selects the interpreter. Port4187 serves `/site/index.html`, `/events/app/index.html` and `/events/index.html`. `/events/` URLs and `build/events/` output intentionally survive the Lineup source move. Query parameters do not activate runtime behavior. `npm run verify:history` is optional and separate.

Browser deliverables ship zero JavaScript: no scripts, inline handlers or JavaScript URLs. Node/Python are development tools only. Native links, fragments, history, controls, reset, validation, file selection and popovers remain; authored result pages replace live matching and counts. See CONTRIBUTING.md and docs/NO-BROWSER-JAVASCRIPT.md. Historical JavaScript/session/preview notes are provenance, not current requirements.

## Contracts

Use BEM `tide-` names, semantic roles, named type/spacing/radius inputs, modern supported CSS and accessible native HTML. Tide, Bumble, Slate, Grove and Iris each require light/dark modes. Summer is removed. Preserve Manrope, square controls, neutral notice borders and unframed event panes; no colored left callout stripe.

Lineup preserves bounded left panes, the natural right document, native scrollbar gutters, minimum 24px bottom clearance, centered 20/35/45 desktop columns and one original filter control set. The complete isolated feed sits below its permanent summary. Below 75rem use the native non-modal left popover, browser-owned dismissal/focus return, scrolling body/pinned footer and reduced motion. Do not restore script-based geometry, custom history or storage. Retain exact venue/event IDs, native paths and useful venue information. All 54 events are authored samples; venue facts are separately attributed. See the application desktop/drawer/ownership contracts and docs/AUDIT.md.

Five registered `src/styles/` modules own application styling. All 64 routes use `document.html`; 62 workspace routes share `workspace.html`. Only venue information, help and submission remain as three unique `src/pages/` fragments. All 54 event details use structured `data/events.json`, shared `event-detail.html` and `data/detail-presentations.json`. Eleven submission fields use registered `form-*.html` partials and `data/submission-fields.json`. Preserve native labels, validation, hints and reset. Keep unique prose, venue facts, uploads and permissions in authored HTML; no raw HTML in sample JSON or duplicated shared fragments. The build renderer escapes text and rejects invalid includes. No browser templating/framework is needed.

Current browser evidence is Chromium on Windows. Firefox/Safari, physical devices and screen-reader checks remain deferred unless a new record explicitly covers them. When asked what is next, use a specific UI need or documented audit gap; Coverage is an inventory, not a product/service roadmap.

End completed repository tasks with `main` as the only branch. Tags/releases preserve versions; never force-push or rewrite published history for cleanup. Keep previews local. Follow CONTRIBUTING.md; keep README/CHANGELOG/contracts current. Repository-only moves need parity evidence and a changelog entry, not a silent API version reset.
