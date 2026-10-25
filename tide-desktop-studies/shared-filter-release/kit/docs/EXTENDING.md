# Extending the kit

The core is stable. Extend it by adding a block with a clear purpose; do not fork a whole stylesheet for each theme or patch a shared primitive for one edge case.

For discoveries from the app playground, follow [adoption and ownership](ADOPTION.md). Reuse an existing component before creating a block. Accepted reusable styles, source HTML, state/behavior documentation and the app's switch to that shared implementation belong in the same change. Application data, navigation and persistence stay outside the CSS kit.

## Naming and ownership

Use BEM (Block, Element, Modifier): `.tide-event-card`, `.tide-event-card__title`, `.tide-button--secondary`. Prefix all kit classes with `tide-` to avoid host-application collisions. Keep modifiers on the same element as their base block. Use semantic attributes for actual state (`disabled`, `aria-invalid`, `aria-pressed`, `checked`); a visual class does not implement behavior or announce a state.

One file may hold multiple related small blocks. A new substantial component can have its own stylesheet, imported after the kit with a named layer. `extensions/panel.css` and its HTML example show this without modifying the core. The declaration `@layer tide.components.extensions` places a new block inside the kit's component layer. New blocks have unique names, so they do not depend on overriding existing selectors. A consuming application's deliberate overrides should have their own later top-level layer, documented as application-owned.

Keep selectors shallow: a block, its element, a state or a modifier. Native descendants inside a block are acceptable when they are part of that block's contract. Do not style an unrelated neighbor through DOM position or a theme-name selector.

## Spacing

The intentional exception for ordinary rich HTML is `.tide-prose`: its scoped descendant rhythm is the public contract, rather than a global reset or a replacement for component spacing. Embedded components use `.tide-prose__exclude`. Keep these reading rules in `css/content.css`; see [the content contract](CONTENT.md).

Components own internal spacing. Composition blocks (`tide-stack`, `tide-row`, screen sections) own the spaces between components. Default text margins are reset; there is no global `* + *` or `p + p` rhythm that silently affects a new component. Use gap for repeated relationships, logical properties for directions, and the established space scale.

Card inset, 24px page inset and zero card gap are intentional. Do not add margins to event cards to solve a parent layout problem. Use a new composition when a new context requires different grouping.

Typography uses rem sizes and explicit measured leading tokens. Do not set a global 62.5% root size. Respect zoom, OS font size and long/unbroken content. Fixed control heights apply to single-line values; buttons use a minimum height so labels can wrap, and textarea height remains resizable.

## Color and new surfaces

Use `--tide-color-*` semantic roles. Avoid raw colors in a component definition. A new decorative panel normally uses `surface`, `text-primary`, `text-secondary`, `border-subtle` and the existing radius. Use `border-control` only when a boundary identifies an interactive control.

A panel that introduces a truly different reading context needs a paired foreground/background token contract and contrast checks in every mode. Document that need; do not add a second arbitrary meaning to `accent` or read `--tide-palette-*-dark` from a component. The event photo opening is the existing example of a distinct, dark reading context in a light page.

Expose component custom properties only when they are useful supported extension points, such as `--tide-panel-padding`. Alias an established token by default. Do not create a local token for every declaration: a token name is an API to maintain.

## Required component entry

Add its name, purpose, BEM classes, HTML source, supported states, semantic roles and keyboard/behavior expectations to `component-manifest.json` and `docs/COMPONENTS.md`. Include at least the normal state and any meaningful focus, selected, disabled, error, loading or empty state. Do not add a state that the component does not actually have.

For behavior-heavy patterns (dialog, menu, tabs, combobox), HTML and CSS alone are insufficient. Specify the focus, escape, keyboard, state and announcement behavior before calling it complete. This kit intentionally contains no fake modal/menu widgets.

## Verification before adding to the contract

1. Run the compiler, generated-output check, structural check and palette tests.
2. Review every theme in light and dark, including focus/selected/disabled/error states that apply.
3. Check at the 320px narrow baseline, a normal phone width, default desktop width, and with text zoom or increased default font size. Long content must wrap without clipping.
4. Check keyboard order, accessible names, labels/descriptions, native semantics, contrast and user preference handling.
5. Record the actual browsers tested. Compatibility data is evidence of feature support, not proof that a whole page was visually tested in that engine.

New primitives require a name, rationale, intended uses and migration notes. A change to an existing public token's meaning or a component's required HTML is a breaking change; add a versioned release note instead of silently changing the contract.
