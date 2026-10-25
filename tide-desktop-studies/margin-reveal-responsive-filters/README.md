# Margin Reveal · Tablet and mobile filters

[Live review](http://127.0.0.1:4187/margin-reveal-responsive-filters/index.html) · [Open the responsive prototype](http://127.0.0.1:4187/margin-reveal-responsive-filters/demo/index.html) · [Approved desktop](http://127.0.0.1:4187/margin-reveal-aligned/index.html)

The user approved and preserved Margin Reveal / Header alignment. This sibling explores the smaller-screen filter flow. Its new CSS is entirely below75rem; the approved desktop markup, dependencies, spacing, sidebar interaction and geometry remain intact.

## Proposed flow

Search stays in the list. Filters opens a full-screen panel below48rem, and a448px drawer from48rem to below75rem. The drawer overlays the tablet page so neither the list nor its event preview is squeezed into another column. The same original date fields and category choices move into the panel. There are no duplicate form controls.

The header and action footer stay visible while the middle scrolls. A live count previews the intersection of the current query and draft filters using the existing48-event search rules. Show events applies the whole form through the original GET navigation. After applying on a smaller screen, the results heading receives focus and the lineup returns to view. URLs, real event links, refresh and Back continue to use the original app behavior.

Reset filters clears only the draft dates/categories and preserves search words. It stays in the panel until applied. Cancel or Escape restores the choices present when the panel opened and returns focus to Filters. The page's existing Clear all link still clears query, dates and categories together. Invalid date ranges retain the original inline explanation and native form validation; the panel stays open. Zero matches can be applied and use the original empty/recovery state.

At the desktop breakpoint, an open panel cancels its uncommitted draft and restores its original nodes before the preserved desktop adapter mounts. Phone/tablet resizing within the smaller-screen range retains an open panel and draft. Without JavaScript or native dialog support, the original inline details/summary remains the fallback.

## Ownership and CSS

The experiment has one private block, `tide-responsive-filters`, in `responsive-filters.css` under `tide.responsive-filters`. HTML is registered in `component-candidates.json` and generated from `tools/build.py`. State/placement belongs to `responsive-filters.js`. Existing Field, Fieldset, Choice, Button, Icon, Badge and native disclosure components retain their kit CSS. Semantic theme, space, type, border and target tokens are reused; there are no raw colors, primitive overrides or new dependencies. Dynamic viewport height, a scrolling middle and safe-area-aware padding keep the action in the visible panel.

The filter dialog is an app-owned composition candidate. A disclosure alone cannot provide a modal focus scope or a fixed action with an independently scrolling body. If selected for shared use, adopt its shell and documented state contract into the maintained kit, add all-theme/mode specimens, and remove the equivalent app-owned styling. The maintained kit is deliberately unchanged during this exploration.

Native `dialog.showModal()` provides the modal surface and background inertness; a visible Cancel control, Escape, title focus and return focus follow the platform and modal-dialog guidance. The title has negative tabindex; the dialog itself has no tabindex. See [MDN: dialog](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog) and [W3C: modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). This uses established dialog methods rather than newer command/closedby attributes.

## Preservation and verification

Every build/check/package verifies all66 approved aligned release files and the entire preceding chain, including both frozen kits. A source parity check removes only the declared stylesheet/script references and hidden modal/launcher markup, then compares all original product documents exactly. Desktop browser measurements and screenshot comparisons accompany responsive flow checks in `qa/`.

Use Python `-B tools/build.py`, `-B tools/check.py`, then `-B tools/package.py` from this folder. The release depends on the adjacent preserved studies served locally on4187. Do not edit dependencies or overwrite a release.
