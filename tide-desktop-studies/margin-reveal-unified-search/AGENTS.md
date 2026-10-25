# Margin Reveal · Unified search

The user selected the Browse First live match-count and single-apply behavior on tablet, and explicitly requested the same behavior on desktop. Preserve the previous 75-file Browse First release and every preceding release. Both kits remain untouched. Python runs with `-B`.

This sibling changes desktop search behavior only: no separate query submit, shared live count, Reset all draft action, one pinned Show events submit. The original desktop rail geometry, filter alignment, list/event widths, bounded scroll and natural document scrolling stay owned by the preserved sources. Mobile/tablet flyout behavior and appearance stay the same.

One original form/control set and one status/reset/apply set move between the desktop dock and mobile/tablet dialog. Keep the count rules in TideSearch. Draft count changes do not mutate the applied feed. GET links, Enter, validation, Back, empty states and no-script native fallback remain.

Private composition block `tide-unified-search`, layer `tide.unified-search`. Register and document the candidate; do not create a second maintained kit. Serve locally on4187.

Spacing refinement1.0.1: desktop bottom clearance for both bounded panes equals `--tide-app-pane-gap` through the existing private `--tide-shell-panel-height` calculation. Dock start padding and status-row end margin both use space4. Show events stays aligned to the list bottom; the filter scroll body absorbs the dock height change. Keep tablet/mobile unchanged. The original68-file1.0.0 ZIP/checksum remain immutable; new current files package as1.0.1.

Native-gutter refinement1.0.2: user explicitly requests native scrollbar retention and actual occupied-width measurement. Add the measured event-list gutter to the existing pane-gap token in the shared desktop height. The private input is `--tide-unified-search-scrollbar-gutter` with zero fallback. Its ResizeObserver uses precise inline box sizes minus inline padding/borders, writes only changed values via requestAnimationFrame, and disconnects/cancels/removes the input below75rem. No custom/hidden scrollbar, forced gutter reservation, polling or scroll-position changes. Show events remains bottom-aligned with the list. Preserve the1.0.0 and1.0.1 archives/checksums and all earlier studies/kits; package current files as1.0.2.
