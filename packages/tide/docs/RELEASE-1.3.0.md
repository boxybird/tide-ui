# Tide 1.3.0

An additive Filter panel (`tide-filter-panel`) now owns the accepted search/filter shell. It adds optional header, scrolling body, pinned footer, reset/count status row and flush rail modifier. Full-width submits reuse Button. The kit remains HTML/CSS with no runtime dependency.

The canonical HTML renderer is consumed by the kit and independent app copy. All six themes/modes retain the same structure. Existing component styles, primitive inputs and theme seeds are unchanged. Patterns for combined forms, draft versus applied counts, Reset/Cancel/Clear, validation, empty recovery and launcher semantics are registered and documented in [SEARCH-FILTERS.md](SEARCH-FILTERS.md).

The previous kit 1.2.1, app and approved Unified Search 1.0.2 prototype remain frozen. The new consumer removes duplicated panel internals, retains measured native scrollbar spacing and preserves desktop/mobile/tablet geometry. Browser and preservation evidence are shipped alongside the consumer release. Firefox/Safari remain deferred.
