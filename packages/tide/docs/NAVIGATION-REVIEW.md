# Navigation comparison · review proposal

This records the accepted 1.11.0 review checkpoint at `c612546`. Tide 1.12.0 subsequently promotes the approved treatment into the [canonical optional recipe](NAVIGATION.md); the following isolation statements describe the original review checkpoint.

This is the Tide component review requested before any Lineup implementation. It compares the current site header with the centered navigation direction selected from the third mockup. It is a documentation-only proposal against Tide 1.11.0, not a new published component variant or a change to the application dependency.

Open `frames/navigation-review.html` in any theme/mode library. The Components sheet links to it beside the button specimens. The page includes complete before/after headers, the closest existing controls, a native state lab, neighboring regular controls and a geometry/state comparison. The existing navigation and button matrices remain available.

## Reuse before extension

| Proposed part | Existing recipe reused | New proposal behavior |
| --- | --- | --- |
| Inactive primary destination | `tide-button tide-button--quiet tide-button--compact` on a real anchor | None |
| Current primary destination | Same compact quiet recipe and existing selected surface/text roles | Map `aria-current="page"` to the selected pair; keep it visible on hover/held; use the existing 1px/2px inset selected-state feedback |
| Saved destination | `tide-button tide-button--secondary tide-button--compact` plus the supplied Bookmark icon | None |
| Header | Existing Site header, Brand and native nav/list structure | Review-only centered composition, with a separate trailing utility; wrap into two rows when the component lacks room |

The proposed current link keeps a transparent reserved border at rest. This distinguishes quiet location emphasis from a selected toggle, whose existing recipe also exposes an accent border. Hover and held feedback use the same inset keyline widths/color role as the selected action. No geometry changes during state transitions.

The third mock is an arrangement and hierarchy reference. The actual specimen uses Tide’s exact compact 44px target, 10px/16px padding, 14px/22px weight-550 Manrope, reserved 1px border, 2px control radius and 18px source icon. It inherits the shared 2px focus outline with a 3px offset. It does not copy incidental image-generated measurements or invent a new button density.

## Native states and semantics

The live lab exercises rest, hover, held pointer, keyboard focus, current page and an authored unavailable state. Other destinations inherit the existing quiet-action raised hover and selected active colors. Current destinations retain their selected pair with inset feedback. Focus is independent of current page. A navigation destination uses `aria-current`, never `aria-pressed`; toggles in the comparison remain native buttons with their existing semantics. An unavailable anchor omits href. The proposal adds a system-color current-state fallback without replacing the shared focus rule.

Native fragment links keep the state lab in view and inspection local. They do not implement a router or application interaction. There is no browser JavaScript, state controller, generated focus ring or simulated hover/active class.

## Isolation and review boundary

Source: `site/templates/navigation-review.html`; isolated proposal styling: `site/css/navigation-review.css`; generation: `site/tools/build.py`. The review stylesheet is loaded only by the ten review documents. Its private `tide-doc-navigation` block is registered as documentation presentation. It is not part of `tide.css` and is not a public kit API.

Tide’s production CSS, tokens, palettes, component manifest and asset bytes remain unchanged. Lineup sources and generated application output remain unchanged. The kit version stays 1.11.0 because this is a review specimen, not promotion of a component extension. If approved for adoption, canonical ownership, registration, release version and application consumption are a separate step.

The proposed layout is contextual documentation styling; its geometry is not a private application override. The only new control appearance is the current-page mapping. Existing button geometry, hover, active, disabled and focus styles remain owned by their original canonical sources.

## Verification

In-app Chromium on Windows: 40 geometry cases across all ten theme/mode combinations at 320, 390, 768 and 1440 by 1000. Navigation geometry exactly matches the existing compact actions; selected colors match the selected quiet button; disabled precedence is preserved; no horizontal overflow or scripts. Ten native hover/keyboard-focus cases cover every theme/mode. Bumble Dark held-pointer checks confirm the same 2px inset feedback and unchanged 44px geometry. No console warnings/errors were recorded.

SHA-256 parity confirms the distributed Tide CSS/tokens/assets and complete Lineup sources/output remain unchanged. The [design QA record](../design-qa.md) contains measured states, combined source/component comparison, captured evidence and testing limits. Firefox/Safari, physical devices, screen readers, actual text zoom and system-forced colors/motion preferences remain unverified.

Root build and full check pass, including 119 tests, native markup, ownership, all-theme structure parity, local references and the unchanged performance budgets. The user accepted this navigation-only review and requested preservation on main and a push. Unrelated Tide components and Lineup remain unchanged.
