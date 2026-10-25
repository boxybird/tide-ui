# Tide official HTML/CSS kit

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
