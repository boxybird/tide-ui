# Contained · Margin Reveal

One additive iteration of the selected original **1216px Contained** composition. [Open the prototype](http://127.0.0.1:4187/contained-margin-filters/demo/index.html), or [use the viewport comparison](http://127.0.0.1:4187/contained-margin-filters/index.html). All prior versions and the UI kit remain preserved.

## Geometry contract

The constrained main grid stays exactly as it was: equal list/event halves and the original gutter. Opening filters never changes that grid, its inset, the individual event's left edge or its width. Only the browsing wrapper expands leftwards by the difference between the main inset and the wider header inset. Its right edge stays fixed beside the individual event. The filters' outer left edge consequently aligns with the wordmark's left edge. Existing24px interior component spacing remains intact.

The filter column uses `clamp(16rem, 20vw, 17rem)` (256–272px at the unchanged root). This gives the list the remaining browsing space. Its right edge stays at the original midpoint and its width never exceeds the original596px maximum. On roomy desktops, the outer margin can supply essentially all of the filter space. On extremely wide screens, additional whitespace remains between filters and the bounded list; neither becomes a needlessly wide form or card.

On compact desktops there is less—or no—unused outer margin, so the list must still narrow while the event remains fixed. The narrower filter column and existing below-field search arrangement help, without an overlay or any right-pane displacement. Below75rem, all new geometry switches off and the approved tablet/mobile composition and native disclosure return.

Both opening and closing animate the browsing width, its negative inline margin, the filter track and the gutter using the existing440ms timing/easing. Width and margin change by equal opposite amounts, keeping the browsing area's right edge stationary throughout. Initial/restored state and reduced motion switch without this animation.

## Preserved interaction and ownership

This is CSS composition, not a new kit component. `margin-filters.css` uses private BEM `tide-margin-study`, layer `tide.margin-study`, alongside existing study wrapper selectors. It does not target kit component selectors or redefine shared tokens, type, color, borders, radii or controls. The existing below-field full-width search is the default; the review retains the previous compact/inline comparisons and image fixtures.

All original nodes, GET search/date/category/clear behavior, focus return, Escape, inert collapsed filters, sticky header, independent left scrollers,48px bottom breathing room, pinned Apply and natural event document scroll are retained. The generated filter adapter changes only the prior study's session namespace. Other scripts are reused directly from frozen dependencies. New source does not introduce a router or any framework.

The closed prototype defaults to the original two-column layout unless an existing per-tab preference is open. The review uses the established `preview-filters=open` initial-state hint, without taking focus from its controls. The image selector still applies only to Ink After Dark's existing illustrative original/rough/no-image fixture.

## Build, checks and preservation

Use Python `-B` to run `tools/build.py`, `tools/check.py`, then `tools/package.py`. There are54 generated HTML documents and one namespaced adapter. The checker compares all53 product documents to the previous original-width generator, stripping only declared private additions. It verifies the complete preceding archive/hash chain, now including all182 files in Width & Search1.0.0. The maintained app/kit and every prior package remain read-only.

QA lives in this sibling. Packages are source releases with preserved adjacent dependencies, served by the existing local port4187 server. Nothing is published.
