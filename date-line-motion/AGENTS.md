# Date Line — Continuity

- This is an isolated, interactive HTML/CSS/vanilla-JavaScript motion prototype requested on 2026-10-21.
- The visual authority remains Quiet Assembly 01 Date Line. Original studies and Date Line In Practice are preserved.
- screens.css, cards.css, themes.css and fonts.css are unchanged copies. Additive behavior belongs in motion.css and app.js.
- app.html is generated from the two byte-identical reference/ frame copies by node build.mjs. Do not edit the generated file directly.
- Keep the resting list and Ink After Dark event at 390 × 844 pixel-identical to the reference. Motion may change; resting typography, spacing, color and imagery should remain fixed.
- app.js uses document.startViewTransition and uniquely named snapshots. No FLIP substitute or framework.
- Linked details, Title only and Soft dissolve are comparison modes. Slow motion and photo selection belong outside the phone in index.html.
- Preserve working Back/Forward, close, Escape, focus restoration, scroll restoration and direct event URLs.
- If the event title is off-screen when returning, use a dissolve rather than animating an invisible source.
- Respect reduced motion and retain direct navigation without native API support.
- ?checkpoint=.25 (or another fraction between zero and one) pauses native animations for deterministic QA captures only. Do not use checkpoints in the user-facing default link.
- Local loopback preview: port 4179. No publishing or external integrations.
