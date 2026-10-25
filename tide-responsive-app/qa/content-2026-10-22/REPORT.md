# Prose and content-page verification

22 October 2026 · App 1.3.0 / maintained kit 1.2.0.

The user requested reusable prose, an informational-page layout and a realistic help example across all themes, while preserving the current design. The implementation is in `kit/css/content.css`, `kit/templates/content/help.html` and the kit registry/documentation. App help pages supply routes and reuse the existing header. Help requires no browser JavaScript.

The portable [kit QA report](../../kit/qa/CONTENT.md) records the actual checks, outcomes and limits. Detailed data is in [browser-measurements.json](browser-measurements.json). The 200% text fixture uses the generated help HTML with a QA-only stylesheet; it does not alter the product.

## Evidence

- `desktop-{tide|summer|bumble}-{dark|light}.png`: identical wide layouts across six palettes.
- `02-phone-390.png`, `03-bumble-light-320-anchor.png`, `05-tablet-834.png`: narrow/portrait reading and native anchor navigation.
- `04-table-keyboard.png`: focused admission table after native keyboard horizontal scrolling.
- `06-text-200.png`: text enlargement at 1280 × 900.
- `07-rich-html-320.png`: contained code overflow, wrapped long URL and embedded Notice exclusion.
- `08-help-review.png`: viewport/theme comparison gallery.
- `09-kit-documentation.png`: the new components’ visible homes in the kit, after checking theme navigation and the shared screen-opening icon.

`01-tide-dark-desktop.png` is the first inspection capture, before aligning the header’s measure to the prose measure. The accepted final desktop captures use the `desktop-*` names. It is retained as iteration evidence, rather than representing the final layout.

## Preservation and checks

[preservation.json](preservation.json) compares 393 app files against [before-hashes.json](before-hashes.json): 365 unchanged, 28 review galleries changed, zero unexpected changes. The review-only difference is navigation to the new Help example. Product event pages, app CSS, search/navigation scripts, font/space/radius primitives and theme inputs remain unchanged. Original preservation locks and historical archives remain intact.

Kit structure/contrast checks and app source checks are in their normal `qa/structure.json`, `qa/contrast.json` and `qa/source-check.json` outputs. All 40 existing tests pass. Screenshot/keyboard checks used local Chromium; Firefox/Safari remain native-engine verification work, with feature compatibility documented separately in `kit/docs/COMPATIBILITY.md`.
