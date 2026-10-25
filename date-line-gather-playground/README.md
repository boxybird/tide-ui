# Gather, amplified

A local, dependency-free microinteraction study. Original Gather remains at http://127.0.0.1:4180/.

Run `node server.cjs`, then open http://127.0.0.1:4181/. `node build.mjs` regenerates app.html from the preserved reference frames. All imagery, fonts and Radix icons reuse the existing project assets; see licenses/ and assets/ for provenance.

Two intensities: Expressive (720ms native travel) and Overdrive (1000ms, twice the hover displacement, larger return arc and rebound). Slow motion makes native travel 2200ms. The resting Date Line layout remains unchanged.

Try hovering a card, opening Ink After Dark, hovering the close control and closing. The close snapshot becomes a warm directional token, arcs to the originating card, then shrinks away with a ring and card rebound. Bookmark feedback has a separate elastic lift and ring. Keyboard focus exposes interaction states; touch gets press feedback without hover. The workbench's Preview hover response rehearses the same engaged styles without requiring a mouse.

Native named snapshots handle the large transition. CSS handles hover; WAAPI handles the return arc and short release feedback. Reduced motion and missing API skip the large movement. Long-detail returns use a dissolve when the source title has scrolled away, avoiding flying invisible elements across the viewport. Browser Back and Escape use the same return flow. Fictional event content; no booking service.

See research.md and design-qa.md for references, evidence and limits.
