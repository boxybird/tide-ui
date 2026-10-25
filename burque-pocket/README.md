# Burque — Pocket Nights

Working mobile prototype of Pocket Nights3 (Pocket Texture), with the user's requested simpler cards and richer event detail.

Local preview: http://127.0.0.1:4174/ (kept running at handoff).

Tap an event to see its fullscreen photo and shared-element View Transition; scroll for full details. Close, Escape, or browser Back returns to the list. Saved events persist locally. Planning is a demo; calendar downloads are explicitly fictional.

Source files: `src/Prototype.tsx`, `src/events.ts`, `src/prototype.css`. Mobile runtime is preserved. Main desktop exploration remains in `../burque`.

In an environment with pnpm available: `pnpm install`, `pnpm dev --host 127.0.0.1 --port 4174 --strictPort`. `pnpm build` compiles the client and prepares local hosting artifacts. No deployment is required.

Use `?motion=off` to inspect the immediate-update fallback. System reduced-motion preference also disables shared-element animation.

See `design-qa.md` for rendered comparison, verified interactions and remaining limits. Generated source/photo prompts are in the research folder and `public/images` provenance notes. All imagery and events are fictional.
