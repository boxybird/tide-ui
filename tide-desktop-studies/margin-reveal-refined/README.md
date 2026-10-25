# Margin Reveal · Desktop filters

The user selected **Margin Reveal** as the preferred desktop version. This refinement removes its redundant inner **Filters** disclosure on desktop; the original selected version is preserved byte for byte.

[Open the prototype](http://127.0.0.1:4187/margin-reveal-refined/demo/index.html) · [Viewport review](http://127.0.0.1:4187/margin-reveal-refined/index.html) · [Previous Margin Reveal](http://127.0.0.1:4187/contained-margin-filters/demo/index.html)

## Desktop-only contract

At75rem and above, when the desktop sidebar is mounted, its existing adapter keeps the native details open. The new private class on the inner summary removes that summary row from layout, keyboard navigation and the accessibility tree. Date/category fieldsets remain visible and can use the sidebar's scroll area. The existing sidebar reveal/close controls, pinned Apply and outer margin geometry remain the same. This refines the inner disclosure; it does not replace the chosen margin reveal interaction.

Below75rem, the private rule is inactive. The same original details/summary nodes return to the results pane, with their native open/closed state and keyboard behavior restored by the existing adapter. Without JavaScript, the native disclosure remains available as a usable fallback. No controls are duplicated, replaced or given new ARIA state.

`desktop-filters.css` is an app-specific responsive composition rule under `tide.filter-study`, using private BEM `tide-filter-study`. Existing Field, Fieldset, Choice and disclosure components are retained. There is no new kit primitive or change to component appearance, palette, type, spacing or interaction code. The summary's original control height disappears on desktop; existing filter-body spacing is retained.

## Source and preservation

All53 product documents derive from the selected Margin Reveal generator. Only the private body/summary hooks, independent preview state keys, dependency references and one CSS link are added. All scripts are reused directly. The checker strips these declared additions before comparing source HTML and verifies every preceding release, including all73 Margin Reveal1.0.0 files. The maintained/frozen kits remain untouched.

Use Python `-B` for `tools/build.py`, `tools/check.py`, then `tools/package.py`. New QA and the immutable release belong to this sibling only. Serve locally through the existing port4187 server.
