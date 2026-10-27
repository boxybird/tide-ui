# Lineup application-kit changelog

## 2.0.5 · 2026-10-27

- Corrected Saved's two-track desktop placement: results occupy column 1 and detail occupies column 2. Browse pages retain their explicit three-column overrides. Saved's list is 352px at 1200px and 390px at 1440px; no unused first or implicit third track remains.
- Restored Tide's result-summary and calendar recipes. The application context label now sits in its own wrapper beside the canonical Results block. Removed private type/spacing/border aliases from result counts and month headers, including the smaller calendar year. Counts/month titles use the kit's 14px/24px type.
- Removed the shared private heading aliases and caption-size override from page introductions, including submission. Tide owns their title, supporting-copy type and internal rhythm. Updated native month-target clearance for the canonical result row and Saved intro.
- Added application-only regression checks that join rendered public/private classes before checking typography ownership. Verified rendered parity against the unchanged kit in every theme/mode, plus responsive placement, native month navigation and the phone drawer. See [verification and limits](SAVED-TYPOGRAPHY.md).

Tide UI remains **1.10.0**, unchanged. Layout family remains **option 1**. Native paths, IDs, authored event data, form controls and the zero-browser-JavaScript boundary remain in place.

## 2.0.4 · named baseline

The existing events application was named Lineup and moved to its own canonical home without changing its application sources or generated route documents. The [initial audit](AUDIT.md) records that baseline and its findings. Earlier application releases remain preserved in Git history and the repository changelog.
