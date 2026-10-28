# Centered header navigation · Lineup 2.1.6

Lineup adopts the selected third header direction and reviewed Tide treatment. Tide 1.12.0 supplies the opt-in `extensions/navigation.css` recipe; Lineup 2.1.6 loads it explicitly after the core stylesheet. No documentation-only CSS or private component appearance is copied into the application.

The shared header keeps Burque and the original native Filters trigger in the leading group, centers Find events and the route-appropriate secondary destination, and places Saved in a separate utility navigation. Saved reuses the existing Bookmark icon partial. Tide owns type, padding, colors, hover, held, current-page and focus appearance. Route context still marks only the actual index, venue, submission or Saved destination as current. Native event/result documents do not identify a different collection document as current.

Desktop retains its 93px single row. Split tablet retains the original 48px Filters allowance. Narrow headers grow naturally as leading controls and primary links wrap. Native event documents keep their established narrow-screen header omission. Links, popover dismissal/focus return, field/reset behavior and browser history remain native.

## Layout boundary

All five application stylesheets, data files and workspace/content partials remain byte-identical to the starting `c612546` commit. Only header/document markup, explicit kit loading and associated registration/tests/docs change. Main content is compared across all 738 generated main documents, including the review entry. No column, pane, filter, feed, summary, right document, footer, card, typography or photo layout is redesigned.

The necessary Tide promotion contains only the approved navigation modifiers, canonical header recipe, ownership registration and associated version/docs/specimens. Default CSS modules, tokens, palettes and assets are unchanged. A separate stylesheet keeps the core distribution budget intact.

## Verification

Thirty baseline geometry cases confirm identical desktop/split-tablet pane positions. Narrow headers wrap naturally; other boxes keep their dimensions and move only in normal document flow. Ninety all-theme cases verify exact Tide control metrics and no overlaps or horizontal overflow. Ten promoted kit-state cases and native application navigation, Back, drawer resize/reset/Escape/focus return and month navigation pass. All 738 generated main-content sections remain byte-identical. The [design QA](../design-qa.md) records the combined visual comparison, evidence and testing limits. A further 60 cases verify final 320/390px header spacing across themes. Root build/check and all 121 tests pass. Firefox/Safari, physical devices, screen readers and changed OS preferences remain unverified. The user accepted this header integration and requested preservation and a push on main.
