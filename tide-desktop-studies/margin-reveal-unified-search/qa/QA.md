# Unified search verification — 2026-10-24

## Version1.0.2 — native scrollbar measurement

The native event-list scrollbar occupies10px in the tested Chromium environment. Both desktop panels therefore end34px above the viewport: the existing24px pane gap plus10px measured gutter. The visible card edge to individual-event edge also measures34px. At1440×900 the panels and Show events end at866px. Horizontal pane geometry, header and natural-height individual event remain unchanged.

Fifteen checks pass in `gutter-1.0.2.json`. These cover occupied gutter, one-result and no-result zero-gutter states (24px bottom clearance), reset restoring the full48-event gutter, desktop1200×600/1440×900/1600×1000 sizing, Show events alignment, retained16px reset-row spacing, native right-document scrolling, measurement cleanup below75rem and unchanged phone/tablet modal geometry. Returning to desktop restarts measurement without reloading. No horizontal overflow or duplicate query field was observed.

Proof: `desktop-gutter-1.0.2.png`. The ResizeObserver uses real box sizes and a guarded deferred write; no custom scrollbar, polling, scrollbar reservation or scroll-position write was added. Source checks verify54 HTML documents and all preserved study/kit files. Previous1.0.0 and1.0.1 archives/checksums remain immutable. Direct Firefox/Safari and native OS-overlay configurations were not exercised in this Chromium pass; zero occupied space was verified through non-overflowing real lists.

## Version1.0.1 — desktop spacing

The current desktop panels end24px above the viewport bottom, matching the existing24px list/detail gutter. Reset all has16px between its top and the divider's inner edge, matching the16px gap below the button. Show events remains aligned with the event list bottom; it moves down24px with the taller panels rather than moving upward when the dock padding is balanced.

Verified at1200×600,1440×900 and1600×1000. At1440×900 the panels and Show events end at876px; at1200×600 they end at576px. Desktop horizontal geometry and the natural-height right event remain identical to1.0.0. Phone390×844 and tablet1024×768 dialog/footer/control vertical geometry remains unchanged. Eight measured checks pass in `spacing-1.0.1.json`; proof is `desktop-spacing-1.0.1.png`.

The1.0.0 archive/checksum remain immutable. The implementation changes two desktop-only CSS relationships using existing tokens and app composition inputs; HTML, JavaScript and both kits are unchanged.

## Version1.0.0 — preserved behavioral baseline

Source checks pass for54 generated HTML pages,4711 local references and53 unchanged product component documents after the declared behavior/stylesheet substitutions. The previous75-file Browse First release and entire preserved dependency chain verify byte-for-byte. JavaScript syntax passes Node's check.

In-app Chromium verifies live desktop counts, one-result and zero-result submissions, Reset all draft behavior and recovery, inclusive date bounds, OR categories, invalid-range blocking, Enter submission, tablet count updates and cancellation, phone submission/event navigation/Back, and node restoration when an open tablet drawer becomes desktop. There remains one query and one status region across sizes.

At1440×900, header, rail, event list and individual-event rectangles are identical to Browse First. The desktop dock grows internally to hold the live count/reset row; its bottom and the list bottom remain852px. At1200×600 they both end at552px, retaining48px of bottom breathing room. No horizontal overflow was observed. Tablet1024×768 and phone390×844 retain the existing flyout arrangement and behavior.

`browser-check.json` contains observed values and18 derived passing checks. Screenshots: `desktop-live-count.png` and `tablet-live-count.png`, both showing the same one-event draft preview. This verifies the local responsive prototype in Chromium; physical keyboards/devices, screen readers and direct Firefox/Safari runs remain outside this pass. The implementation adds no new browser API beyond the previously tested controller.
