# Native runtime boundary · Lineup 2.1.4

**Current 2.4.0 boundary:** the approved map is now in `src/map/` and builds from the current Lineup templates. Review `/events/app/venues.html` on port 4187. There is no active separate consumer or copied source snapshot. Only the venue directory loads browser modules; prior no-script/map-provider-exclusion statements below describe the earlier native baseline. The current [source-of-truth contract](SOURCE-OF-TRUTH.md) takes precedence. Native event/search journeys and service limits are unchanged.


There is no browser JavaScript. `behaviorHome` is empty; `document.html` loads stylesheets only. The old search/runtime/navigation/headings/filter/rail/preview scripts and their script partials are removed. The reference site and canonical kit specimens are script-free as well. See the [repository policy and audit](../../../docs/NO-BROWSER-JAVASCRIPT.md).

## Native behavior

- Links and fragment URLs navigate normally, including modified clicks and browser Back.
- Below 34rem a native auto popover supplies the mobile Menu, with CSS anchor placement and unchanged Tide Panel/navigation appearance. Tab, Escape, outside-click dismissal and invoker focus return remain native. The inline fallback stays available when popover selectors are unsupported. See [mobile navigation](MOBILE-NAVIGATION.md).
- Below 75rem a native `popover="auto"` panel and `popovertarget` buttons provide the left filter drawer, explicit Close, Escape/outside-click dismissal and focus return. CSS supplies sliding motion, reduced motion and responsive placement; the same controls form the permanent desktop column. This is a non-modal popover, with no authored focus trap, draft rollback or control relocation. Native details/summary still provides date/category disclosure. See the [drawer contract](FILTER-DRAWER.md).
- Native form reset restores source defaults. Required/type constraints use browser validation. From/Through controls do not implement relational date validation.
- The file chooser provides its native selection/replacement UI. Content and size validation are not supplied by the UI kit.
- CSS supplies grid/subgrid, sticky headings, viewport height and native gutter reservation. The result summary is outside the scrolling feed, eliminating dynamic sticky offsets.

## Authored states

The build creates all, Music, Comedy, Workshop and empty result documents from the same catalog. Each category page includes only its authored category and a complete matching preview. These are reference layouts, not live matching. The application has normal Search events, date and category labels, with no tutorial result-state navigation. Kit reviewers reach the reference layouts through `/events/index.html`. Query parameters are not evaluated by the static preview. Venue information remains authored and visible independently of results. The [handoff contract](HANDOFF.md) records form integration, fixed Saved content, submission limits and fictional fixture provenance outside the product interface.

Custom scroll-to-top delays, reading-position stores, session preferences, fetched first-result previews, draft result counters and photo/inspection parameters are retired. Existing file paths still load native pages; old query parameters have no browser behavior. No application service replaces the removed scripts.

Build/check reject script files/imports, inline handlers and JavaScript URLs at browser boundaries. Tooling may use Node/Python, but is not shipped to the browser. Actual browser coverage and limits are recorded in the desktop contract and policy.

## Independent consumers

The zero-script boundary describes the delivered kit. An independent consuming website may add its own navigation/search runtime while retaining complete direct documents and native fallback. Requests, partial replacement, history/cache coordination, loading/error feedback, additional motion and return-state preservation then belong to that consumer. See the [consumer integration guide](CONSUMER-INTEGRATION.md); no runtime, endpoint or test client is added to Lineup by that documentation.

## Venue directory · 2.3.1

[Venue navigation](VENUE-DIRECTORY.md) uses native fragments, focus, scrolling and CSS target visibility. Cards select map points and map links reveal their row; separate document links open venue details. Selected caption links replace the earlier marker popovers. The separate prototype runtime is not imported. Live venue search, geographic panning/zoom, provider maps, fetched content and persistence remain consumer integrations; the native venue search form uses the same GET integration contract as event search, while matching stays consumer-owned. No simulated camera or zoom controls are shipped. Native return uses the URL target and progressive CSS `scroll-initial-target`; supporting-browser evidence and restoration limits are documented.
