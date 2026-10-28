# Tide navigation · review and canonical recipe QA

The original sections record the accepted 1.11.0 review checkpoint at `c612546`. The current 1.12.0 promotion is recorded below; earlier isolation statements describe that checkpoint.

## Findings

No actionable P0/P1/P2 findings remain in this isolated comparison specimen. The proposal reuses existing compact action geometry and native state rules, instead of copying the generated mock's approximate measurements. The review sheet exposes complete before/after headers and puts the proposed controls beside their actual Tide relatives.

This is a documentation proposal. It is not a released navigation variant and has not been applied to Lineup.

## Source, implementation and comparison

- Source visual truth: the third displayed header mock, `C:/Users/andre/.codex/generated_images/01a17fc5-fe3d-7ad0-be3e-879bb2737e03/exec-2c7a6b62-b149-42d2-bd91-9d629f5bedb7.png`.
- Source pixels: 2128 × 739, representing the intended 1440 × 500 CSS header/context crop. Only the header is the comparison target for this task; the application content beneath it is outside this component review.
- Implementation: `http://127.0.0.1:4187/site/bumble-dark/frames/navigation-review.html` at 1440 × 1000 CSS pixels, Bumble Dark, initial document position, no current hover or keyboard focus.
- Browser-rendered overview: `build/qa/tide-navigation-review/overview.png`, 1425 × 990 raster pixels. The screenshot service uses JPEG encoding despite the filename suffix. DevicePixelRatio was approximately 1.
- Component capture: `build/qa/tide-navigation-review/after-header.png`, 1377 × 93 raster pixels, from the exact 1376.667 × 92.667 CSS component rectangle.
- Combined comparison: `build/qa/tide-navigation-review/comparison.html` and `visual-comparison.png`, rendered at 1424 × 650. The source and actual component appear together in the same input. Source is normalized to 1440 × 500, with its 32px application outer inset removed. Actual is displayed at its measured CSS component size. Matching focused crops compare the primary links and Saved utility at the same scale.

The full-header comparison confirms the brand / centered primary destinations / trailing utility arrangement. The focused comparison confirms the quiet current fill and text, secondary Saved treatment, source icon and existing control proportions. It deliberately retains Tide's 14px/22px compact type and 44px minimum, rather than the mock's approximate larger current box and softer Saved border.

## Required fidelity surfaces

| Surface | Result |
| --- | --- |
| Fonts and typography | Local Manrope, 14px/22px, weight 550, normal tracking and case match existing compact controls exactly. Brand remains the existing Brand recipe. The mock's incidental type size is normalized to the canonical compact input. |
| Spacing and layout rhythm | 44px minimum, 10px/16px padding, 12px icon gap, reserved hairline and 2px radius match existing controls. Both full headers are 92.667px high on desktop. Centered primary links wrap beneath brand/Saved when the component is narrow. Header/application outer geometry is intentionally excluded from the component crop. |
| Colors and tokens | Existing selected surface/text, raised surface, secondary text, control border and focus roles are reused. Current-link color pair equals the existing selected quiet button in all ten theme modes. Saved uses the canonical secondary border, which is intentionally clearer than the generated mock. No palette changes. |
| Image quality and assets | The exact existing Bookmark SVG supplies the decorative 18px glyph. Brand is unchanged. No new decorative asset, replacement icon, photo repaint or custom drawing was introduced. The mock photo is outside the component target. |
| Copy and content | Find events, Sunshine Theater and Saved retain the selected direction. Review labels distinguish current location from a toggle and clearly identify the proposal as isolated documentation. |

## Native browser verification

In-app Chromium on Windows, using viewport emulation:

- 40 geometry cases: all five themes in light/dark at 320, 390, 768 and 1440 by 1000. No horizontal document overflow, zero scripts, one h1. Current/inactive navigation geometry equals existing quiet compact geometry. Header Saved geometry equals the existing secondary compact link. The primary group is centered at desktop width.
- Ten live state cases: actual pointer hover of quiet/inactive/current/selected/Saved/unavailable controls and actual keyboard Tab focus in every theme/mode. Inactive hover matches the quiet action; current hover preserves its selected pair with the same 1px inset keyline as the selected action. Disabled foreground/background wins. Keyboard focus uses a 2px outline and the shared nominal 3px offset (computed 2.667px after device-pixel snapping).
- Real held-pointer checks in Bumble Dark: current destination and existing selected quiet button both show a 2px inset keyline, retain selected colors and stay 44px tall. Inactive and Saved destinations use the existing selected active pair, with unchanged geometry. These were read while the native pointer was held; no pseudo-state classes or browser JavaScript simulated them.
- Native lab fragments preserve the inspection section; keyboard focus is independent of current location. Unavailable anchors have no href. Proposed destination anchors never use aria-pressed.
- Browser console warnings/errors: none recorded.
- Detailed evidence: `geometry.json`, `live-states.json`, `held-focus.json`, `current-hover.png`, `current-focus.png` and `current-held.png` in `build/qa/tide-navigation-review/`.

The first visual comparison required no P0/P1/P2 fix. A separate repository check caught an oversized library entry and theme-specific review-body metadata. The sheet now has a short library link, and all review bodies are identical across themes; neither correction changes the component appearance or relaxes the checks.

Firefox/Safari, physical devices, screen readers, actual browser text zoom and OS forced-colors/motion preference changes remain unverified. The source contains the system-color fallback; no runtime support is claimed from source inspection alone.

## Isolation and completion

SHA-256 parity checks confirm unchanged Tide production CSS/tokens/assets, the complete built Tide distribution, Lineup source files and the complete generated application output against the initial `ebca5d5` baseline. The proposal's private stylesheet is loaded only by its ten documentation pages. The release remains Tide 1.11.0 and Lineup 2.1.5.

Visual review, native state checks and responsive/theme measurements are complete. `npm run build` and `npm run check` passed after the documentation corrections: 1,041 HTML documents, 56,144 local references, 581 Markdown references and 119 tests (7 preview HTTP, 71 Tide contracts/palettes and 41 application templates). Performance budgets, theme structure parity, ownership and zero browser JavaScript checks pass without exemptions. The user accepted the navigation-only review and requested a commit and push on main. The changed files support only the navigation specimen, its registration, build integration, tests and documentation; unrelated Tide components and Lineup remain unchanged.

## Canonical promotion · Tide 1.12.0

The approved treatment now lives in `extensions/navigation.css` and `templates/navigation.html`, with Site header/Button ownership and variants registered. The comparison sheet consumes these canonical classes; its private stylesheet supplies documentation layout only. Existing default CSS modules, token/palette inputs, assets and action geometry remain unchanged.

The modifiers join their existing `tide.components` owner layer. This fixes an initial current-page-input cascade defect caught during app integration. Current-page state uses the approved selected pair, transparent quiet border, native 1px/2px inset feedback and inherited focus. The responsive header supports a leading action without changing its geometry; below 44rem it uses the existing 8px named gaps and natural wrapping.

Ten promoted all-theme state cases pass; Lineup's 90 theme/viewport cases match the reviewed control metrics. The actual reviewed-Tide and Lineup headers were inspected together with focused primary-link and Saved comparisons. No actionable P0/P1/P2 visual finding remains. See Lineup's current design QA for source/capture normalization and unchanged-main-content evidence.

Final build and full repository check pass, including 121 tests, theme parity, native references, ownership, zero-browser-JavaScript and unchanged core performance budgets. The navigation extension is 2,540 bytes; the core entry point remains 99,988 bytes. Sixty final narrow-theme app cases confirm wrapping without overlaps. The user accepted the Lineup integration and its required Tide navigation recipe, and requested a commit and push on main.

final result: passed
