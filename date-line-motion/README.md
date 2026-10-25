# Date Line — Continuity

A focused HTML/CSS/vanilla-JavaScript prototype using the native View Transition API. No dependencies or framework.

Preview: http://127.0.0.1:4179/

Run **node server.cjs** from this folder. The server listens only on 127.0.0.1:4179. **app.html** is the standalone phone view; **index.html** adds comparison controls outside it.

## Try it

1. Open Ink After Dark, or either of the other two cards.
2. Close with the top-left control, browser Back, Escape, or the comparison panel’s Return to list button.
3. Compare Linked details, Title only and Soft dissolve.
4. Turn on Slow motion to inspect the movement.
5. Choose Organizer upload to reuse the preserved poor-photo case for Ink After Dark.
6. Scroll for richer details. Returning from below the title uses a dissolve.

Natural linked/title movement lasts 480 ms; dissolve lasts 280 ms. Slow motion lasts 2400 ms. These are prototype choices, not prescribed standards.

## Preserved foundation

The four shared stylesheets and reference frame copies remain unchanged. The resting list and Ink After Dark opening at 390 × 844 match fresh reference screenshots with zero changed pixels. See qa/source-comparison.png, qa/pixel-comparison.json and design-qa.md.

New behavior lives in motion.css, app.js, lab.css and lab.js. The included build.mjs reads the reference frame bodies to generate the already-included app.html; run **node build.mjs** only if regenerating the HTML.

Assets are copied from the existing project. No new photographs, fonts, icons or textures were generated. Font and Radix icon licenses are in licenses/; image history is in assets/images/.

## What moves

Linked details names the selected surface, title, category, day, weekday, month, start time, venue and price separately. The date number follows a small arc as the compact stamp becomes the full date line. Abbreviations release before their boxes widen. Venue visibility is staggered to keep the crossing path clear. Supporting controls have reveal layers above the photograph.

Title and price use one incoming snapshot to avoid ghosting between font sizes. Text movement uses snapshot geometry and crossfading; it does not interpolate glyph outlines.

History, direct event links, keyboard opening/closing, focus return and scroll restoration work. Saved events persist locally, with a saved filter and empty state. No booking, accounts, network event source, tracking or advertising integration is included.

Reduced-motion preferences and unavailable native API support take the direct-navigation path. The forced fallback app.html?native=off exercises that branch. Verified in the Codex in-app browser; physical-phone and cross-browser checks remain.

## Visual QA helpers

Adding ?checkpoint=.25 or ?checkpoint=.65 pauses native animations at that fraction of their duration after a navigation. Omit this parameter for normal use. Inspector geometry and native pseudo-element names are recorded as DOM data attributes for local QA.

## Primary implementation references

- [MDN — Using the View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using)
- [Chrome for Developers — Same-document transitions](https://developer.chrome.com/docs/web-platform/view-transitions/same-document)
- [MDN — view-transition-name](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/view-transition-name)

Earlier collections and the overall Date Line favorite remain intact.
