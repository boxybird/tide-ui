# Current maintained successor: kit 1.3.0

Filter panel internals ship in css/filter-panel.css; shell template and integration rules are in templates/filter-panel.html and docs/SEARCH-FILTERS.md. This independent successor is maintained here; earlier kit/app trees remain frozen. Preserve existing primitives and theme inputs.

# Tide official HTML/CSS kit

Current contract clarification: **1.2.1**. Event lists and individual-event compositions are unframed on mobile, tablet and desktop. Decorative outer border boxes or rounded clipping shells are not kit styling. Do not add them when composing larger screens. Existing row separators, control/state borders and focus indicators keep their own contracts. App 1.3.1 removes its desktop frame; shared kit component CSS is unchanged.

Latest additive release: **1.2.0**. `css/content.css` owns `.tide-prose` (ordinary rich HTML, explicit `__exclude`, optional `__table-wrap`) and the `.tide-content-page` composition. Both are bundled in `tide.components.extensions`, registered and documented in `docs/CONTENT.md`. Help source is `templates/content/help.html`, consumed by kit fixtures and the app via `tools/content.py`. The reusable skip link now ships in utilities, rather than docs CSS. Preserve all existing primitives/themes; no Tailwind or browser runtime is added. The 1.1.0 ZIP remains frozen.

The user chose Tide's appearance and Date Line's layout. This is an isolated production-oriented CSS/HTML foundation, not permission to redesign previous collections or build application services.

- Preserve Manrope, the fixed spacing/type scale, touching cards, prominent inline dates, full-screen photo opening, square 2px controls / 4px documentation panels, and uniform neutral callout outlines.
- Three themes (Tide, Summer, Bumble), each with light and dark modes. System appearance is independent from the theme.
- Edit theme inputs only in tokens/themes.json. Run tools/build.py; the foreground/surface contrast gate must pass before generated outputs change. Do not promise accessible arbitrary inline color overrides.
- Public semantic colors are --tide-color-{role}. Mode-specific implementation values are --tide-palette-{role}-{light|dark}. Components may not depend directly on palette tokens or theme names.
- BEM blocks use tide-, elements use __, modifiers use --. App components are plain HTML/CSS; no client runtime framework.
- CSS cascade order is declared in css/tide.css. Put additive component extensions in tide.components.extensions; use tokens and explicit state semantics.
- A new theme or component must include light/dark fixtures, focus/disabled/error/selected coverage as applicable, contrast validation, narrow layout checks, and documentation. Keep the existing kit fixed unless the user explicitly changes its contract.
- Run tools/build.py --check, tools/check.py and unittest before handoff. Record actual browser tests separately from compatibility research.
- Keep everything local. Earlier studies and favorites remain preserved.

- This is the maintained kit 1.2.0 consumed directly by the app, while the original sibling `tide-ui-kit/` is frozen. User explicitly asks that accepted app discoveries return here. Follow `docs/ADOPTION.md`: reuse first, distinguish components/compositions/host behavior, give new public blocks a registry and CSS/HTML/state home, add all-mode fixtures, switch the app to shared styles and remove duplicates. `css/patterns.css` is bundled in `tide.components.extensions`. Native disclosure and calendar groups are kit-owned; In view reuses Badge plus an optional Event card modifier/status slot. Keep all primitives and original hashes intact.
