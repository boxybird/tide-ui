# Motion sketches QA

final result: passed

## Evidence and normalization

Source visual truth: preserved Date Line frame copies in reference/baseline-list.html and reference/baseline-event.html.
Fresh source captures: qa/source-list.png and qa/source-event.png.
Implementation: qa/list.png, qa/gather-event.png, qa/aperture-event.png, qa/shutter-event.png.
All at 390 × 844 CSS px and 390 × 844 PNG pixels, density 1. No resizing or normalization.

Combined endpoint comparison inspected: qa/endpoint-comparison.png. Source and implementation are in the same input. The list and all three event openings have zero changed pixels against the approved corresponding source; see qa/pixel-checks.json.

Intermediate native snapshots inspected: qa/gather-mid.png, qa/aperture-mid.png, qa/shutter-mid.png, combined in qa/motion-studies.png. Text and layering are readable at this scale; endpoint equality additionally checks focused glyph positions and spacing.

## Required fidelity surfaces

- Typography: original Manrope, weight, size, line height, tracking and wrapping retained. Resting glyph rendering is identical.
- Layout/spacing: original card geometry, touching edges, 24 px inset, hero/content placement, controls and below-fold article retained.
- Color/tokens: original palette, texture opacity and photo scrim retained; only transition snapshots change temporarily.
- Images/icons: existing photos, texture and Radix icons copied without replacement. No new generated or handcrafted assets.
- Copy/content: original event material retained. Only the external motion-comparison labels and instructions changed.

## Findings and fixes

P2 resolved: the first aperture experiment mixed independently moving date/time/title fragments with already-visible destination facts. It created competing text paths. Aperture now reveals the complete event as one masked snapshot. Gather retains the smaller set of shared anchors; Shutter moves only the surface/title.

Custom animation effects are cancelled after transition completion so masks cannot carry into later transitions. Finished screen captures confirm cleanup.

No remaining actionable P0/P1/P2 findings.

## Verification and limits

All three natural openings and returns use the native API and complete. Return focuses the corresponding card. Controls select the matching mode and duration. Aperture also completes at 320 × 740 without horizontal overflow. The forced direct-navigation fallback works. Existing history, detail scrolling and saving code is reused rather than rebuilt.

The standalone app warning/error log is empty during the three-treatment test. The inherited iframe workbench has the browser-tool observer diagnostic documented in the prior Continuity QA; no page error is recorded. This pass does not claim that diagnostic is fixed.

Reduced-motion behavior is retained, not OS-emulated in this browser tool. Physical phones and other browsers remain follow-ups; no full accessibility conformance claim.

## Checklist

- [x] Preserve earlier prototypes and static design.
- [x] Native snapshots rather than a simulated morph.
- [x] Inspect intermediate frames and eliminate conflicting paths.
- [x] Match endpoints pixel for pixel.
- [x] Test three openings/returns, comparison controls, narrow viewport and fallback.

P3 follow-up: choose a direction with the user, then tune its pace and easing on an actual phone before expanding product scope.
