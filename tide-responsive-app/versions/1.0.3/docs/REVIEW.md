# Code and accessibility review

Reviewed 2026-10-22. This is a targeted engineering review plus browser smoke checks, not a claim of full WCAG conformance or a screen-reader audit.

## Foundation retained

The kit already has the right overall pattern: prefixed BEM blocks/elements/modifiers, ordered cascade layers, explicit semantic color roles, invariant type/spacing/control geometry, native HTML controls, logical properties, focus-visible styles, high/forced-contrast accommodations and a contrast-gated palette compiler. No framework is required for these contracts.

Theme inputs remain limited to palette and texture. Components consume public semantic roles. Color values belong in the theme/token source, not in app-specific selectors. The new app adds `tide.app` after the kit's layers. App layout cannot mutate the original kit and does not select named themes.

## Polish applied to the independent reviewed copy

1. Removed global suppression of the browser's native tap highlight. Touch feedback should not be suppressed without a considered replacement.
2. Corrected documentation type-sample modifiers to include their BEM element base. Added a regression check for modifiers without their base class.
3. Added a visually hidden H1 to the isolated event-list fixture. It now has a primary heading without changing the selected pixels.
4. Hid a decorative bookmark preview from assistive technology. Nonfunctional specimens should not imply an actionable save control.
5. Added public BEM title/section-title classes to event and page components. A preview can use H2 while a standalone event uses H1, with identical visual typography. Legacy heading selectors remain compatibility aliases.
6. Added markup contract tests for positive tabindex, missing image alternatives, unnamed links/buttons and invalid `aria-pressed` use. These checks cover authored names and common mistakes; they do not replace a browser accessibility tree or the full accessible-name algorithm.
7. Removed the test's assumption of exactly three themes. Every theme must have light/dark modes, but new named themes can be added without changing the test.
8. Aligned field contents to the start of their grid area. In paired date/time fields, a hint under one field no longer moves the other field's label and control out of alignment.

The reviewed copy is version 1.0.1. Primitive type, space, radius and theme input files match the original. The original's source, bundle and samples remain untouched; `qa/original-kit-lock.json` records its file hashes.

## App-specific decisions

The subsequent 1.0.3 event-selection request adds one optional, deferred browser script. It only sequences the CSS return to the top before native event navigation and carries scroll positions. The underlying HTML destinations and native fallbacks remain intact; no React or content-swapping application was added. New behavior checks and rendered evidence are in `qa/EVENT-SELECTION.md`.

- Exactly one main landmark and H1 per page. Heading levels change with page context, not with typography.
- Full-card links have explicit names and never contain nested controls. All three events have real HTML destinations.
- Active desktop preview uses written “In view” text plus a neutral outline. The selected event route uses `aria-current="page"` on its card link.
- Native details/summary, radio buttons, checkboxes, selects, file inputs and reset buttons keep their keyboard behaviors. Inputs have labels; hints use `aria-describedby`. No positive tabindex.
- Skip links target both results and desktop preview; anchor destinations can receive focus. The result pane is a named, focusable region and keeps its scrollbar visible.
- The main document scrolls through the details. Only the desktop result pane scrolls independently. Its maximum height accounts for header geometry and top/bottom spacing so the full container fits on arrival, including in short desktop windows.
- Form controls retain the kit's 44px/48px targets and 16px input text. No tiny fixed mobile toolbar or hover-only action is introduced.
- Normal flow, rem sizes, wrapping and responsive columns support narrow viewports. Safe-area insets protect event controls; native browser chrome remains available.
- “Saved” is navigation to an example shortlist, not a false toggle. Submission and search limitations are disclosed. No fake successful network actions.

## Verification and limits

Palette verification checks 324 foreground/surface pairs across all six theme modes. This mathematical gate tests declared solid-color roles; photographic text also depends on the invariant scrim and rendered image review. It does not guarantee arbitrary organizer photos will be safe without validation.

Generated HTML checks inspect local links, IDs, labels, BEM usage, semantic landmarks and token references. Regression tests cover palette generation and the additional markup contracts. Browser evidence is recorded separately in `qa/`.

Chromium is available here. Current Firefox and Safari support the CSS features used, but their native rendering, VoiceOver/NVDA behavior, high-contrast operating-system modes and physical touch/safe-area behavior still need release testing on those platforms. A production app will also need dynamic result announcements, error focus, dialog focus management if dialogs are added, bookmark state announcements, loading/offline states and restored list position.

## References

- W3C [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html): avoid two-dimensional scrolling at a 320 CSS pixel equivalent.
- W3C [Focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html): sticky regions must not completely hide focused controls.
- W3C [Target size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html): the kit's 44/48px controls exceed the usual 24px minimum.
- MDN [PWA best practices](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices): adapt to viewport and input method, retain usable navigation.
