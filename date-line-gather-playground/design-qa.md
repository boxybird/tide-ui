# Design QA — Gather, amplified

final result: passed

Source: original Gather at http://127.0.0.1:4180/app.html, itself a preserved Date Line extension. Implementation: http://127.0.0.1:4181/. Local IAB verification on 2026-10-21.

## Findings resolved

- P2: invalid linear() easing time positions initially caused landing feedback to throw. Corrected to percentage positions. Native open/close then completed with result=native, microState=landed and zero remaining return-marker classes.
- P2: scaling the entire card-content during press created a stacking context that interfered with bookmark hit testing. Moved press scale to the title only. Re-tested Save → Unsave → Save → Unsave through real controls; state and labels reverse correctly. Final captures made after the fix.
- P2 visual: initial return token was too faint against the transitioning dark surface. Gave the transient token an accent fill and dark icon. Inspected the revised native closing checkpoint at 46%; the token remains visible. It disappears after its landing, leaving the resting layout intact.
- First list comparison captured the source before its texture finished loading. Re-captured the loaded source; do not treat that loading mismatch as design drift.

## Fidelity evidence

`qa/endpoint-comparison.png` places fresh source and final implementation in the same image, at 390×844 CSS pixels and 390×844 image pixels. Inspected the combined input, including readable typography, date/fact spacing and controls. `qa/pixel-checks.json`: zero changed pixels for both list and Ink event at rest. `qa/preservation.json`: all four inherited foundation stylesheets remain byte-identical to the original Gather copies. Typography/Manrope weight and tracking, spacing rhythm, dark/accent colors, photo crop and content all match. The ordinary endpoints do not need separate crops because the combined image preserves readable native resolution.

## Interaction evidence

- Native Expressive opening and return for Ink. Focus returns to `View Ink After Dark`.
- Native Overdrive opening and return for Ink. Flight has its own `return-control` group in the observed native animation list; motionMap records a match from toolbar (20,20,44,44) to the card anchor (322,579.33,44,44) at 390px width.
- `qa/return-mid.png` is an actual paused native close snapshot at 46%, not a drawn or substituted image.
- 320×740: list and Desert event have no horizontal overflow. Native navigation and Escape return complete.
- Forced missing-API path with `native=off`: Late Set opens directly; direct Ink close leaves no transient marker. Reduced-motion branch is code-inspected, not OS-emulated in this run.
- Bookmark state reverses correctly after the press fix; ring and glyph lift are added only when motion is allowed.
- Workbench Overdrive selection propagates to the iframe and full-size link; parent reports 1000ms. Preview hover response invokes the same engaged state, inspected visually. Real pointer-hover input is not exposed by this automation tool; magnetic tracking is implemented but not pointer-sweep tested.
- JavaScript syntax checks pass for app.js, micro.js and lab.js. Earlier diagnostic console error is retained in browser history, rather than suppressed; no new landing exception occurred after correction. The inherited iframe observer diagnostic remains a tool/instrumentation limitation from prior studies.

## Limits

Desktop IAB only; no physical phone or cross-browser performance measurements. This is an intentionally exaggerated design experiment, not a production release. Hover doesn't gate touch navigation; reduced motion is supported in code. Prior prototypes and original Gather remain available unchanged.
