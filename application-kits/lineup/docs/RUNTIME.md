# Native runtime boundary · Lineup 2.1.4

There is no browser JavaScript. `behaviorHome` is empty; `document.html` loads stylesheets only. The old search/runtime/navigation/headings/filter/rail/preview scripts and their script partials are removed. The reference site and canonical kit specimens are script-free as well. See the [repository policy and audit](../../../docs/NO-BROWSER-JAVASCRIPT.md).

## Native behavior

- Links and fragment URLs navigate normally, including modified clicks and browser Back.
- Below 75rem a native `popover="auto"` panel and `popovertarget` buttons provide the left filter drawer, explicit Close, Escape/outside-click dismissal and focus return. CSS supplies sliding motion, reduced motion and responsive placement; the same controls form the permanent desktop column. This is a non-modal popover, with no authored focus trap, draft rollback or control relocation. Native details/summary still provides date/category disclosure. See the [drawer contract](FILTER-DRAWER.md).
- Native form reset restores source defaults. Required/type constraints use browser validation. From/Through controls do not implement relational date validation.
- The file chooser provides its native selection/replacement UI. Content and size validation are not supplied by the UI kit.
- CSS supplies grid/subgrid, sticky headings, viewport height and native gutter reservation. The result summary is outside the scrolling feed, eliminating dynamic sticky offsets.

## Authored states

The build creates all, Music, Comedy, Workshop and empty result documents from the same catalog. Each category page includes only its authored category and a complete matching preview. These are reference layouts, not live matching. The application has normal Search events, date and category labels, with no tutorial result-state navigation. Kit reviewers reach the reference layouts through `/events/index.html`. Query parameters are not evaluated by the static preview. Venue information remains authored and visible independently of results. The [handoff contract](HANDOFF.md) records form integration, fixed Saved content, submission limits and fictional fixture provenance outside the product interface.

Custom scroll-to-top delays, reading-position stores, session preferences, fetched first-result previews, draft result counters and photo/inspection parameters are retired. Existing file paths still load native pages; old query parameters have no browser behavior. No application service replaces the removed scripts.

Build/check reject script files/imports, inline handlers and JavaScript URLs at browser boundaries. Tooling may use Node/Python, but is not shipped to the browser. Actual browser coverage and limits are recorded in the desktop contract and policy.
