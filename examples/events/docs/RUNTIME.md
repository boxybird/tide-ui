# Native runtime boundary · App 2.0.0

There is no browser JavaScript. `behaviorHome` is empty; `document.html` loads stylesheets only. The old search/runtime/navigation/headings/filter/rail/preview scripts and their script partials are removed. The reference site and canonical kit specimens are script-free as well. See the [repository policy and audit](../../../docs/NO-BROWSER-JAVASCRIPT.md).

## Native behavior

- Links and fragment URLs navigate normally, including modified clicks and browser Back.
- Native details/summary provides disclosure. There is no JavaScript modal, focus trap, viewport resizing or control relocation.
- Native form reset restores source defaults. Required/type constraints use browser validation. Sample From/Through controls do not implement relational date validation.
- The file chooser provides its native selection/replacement UI. Content and size validation are not supplied by the UI kit.
- CSS supplies grid/subgrid, sticky headings, viewport height and native gutter reservation. The result summary is outside the scrolling feed, eliminating dynamic sticky offsets.

## Authored states

The build creates all, Music, Comedy, Workshop and empty result documents from the same catalog. Each category page includes only its authored category and a complete matching preview. These are static specimens, not live matching. Search/date/category inputs are labelled control examples; query parameters are not evaluated. Venue information remains authored and visible independently of results.

Custom scroll-to-top delays, reading-position stores, session preferences, fetched first-result previews, draft result counters and photo/inspection parameters are retired. Existing file paths still load native pages; old query parameters have no browser behavior. No application service replaces the removed scripts.

Build/check reject script files/imports, inline handlers and JavaScript URLs at browser boundaries. Tooling may use Node/Python, but is not shipped to the browser. Actual browser coverage and limits are recorded in the desktop contract and policy.
