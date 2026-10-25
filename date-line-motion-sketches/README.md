# Date Line — Motion Sketches

Local preview: http://127.0.0.1:4180/

A motion-only iteration using the existing Date Line prototype. No new product features, framework, backend or assets. All earlier versions remain preserved.

- **01 Gather:** selected card expands; title, category, day and start time travel. Other facts arrive together. 480 ms.
- **02 Aperture:** the whole event opens through a circular native snapshot mask from the selected card. 620 ms. Keeping the complete event together avoids competing text paths.
- **03 Shutter:** title stays connected while the named photo plane opens across the expanding card. 560 ms.

Slow motion is 1800 ms. Every treatment reverses on close. Reduced-motion preferences and unavailable native API support retain direct navigation.

Run **node server.cjs**. Files are already built; no package installation. The helper controls are in index.html; app.html is the standalone view. All three cards still open, using the unchanged existing event content and assets.

The original shared CSS files remain unchanged. experiments.css and the small app.js additions target native View Transition pseudo-elements. The aperture and shutter masks are actual animations of browser snapshots, not video or substitute image assets.

Evidence: qa/motion-studies.png, qa/endpoint-comparison.png, qa/interactions.json and design-qa.md. Add ?checkpoint=.25 to a standalone URL for a paused native animation checkpoint; omit it for normal playback.

Primary reference: [Chrome for Developers — same-document View Transitions and pseudo-element animation](https://developer.chrome.com/docs/web-platform/view-transitions/same-document).
