# Lineup application-kit changelog

## 2.1.1 · 2026-10-27

- Removed retired Workbench / Half Split / Contained / Margin Reveal prefixes from Saved, Help, Add an event and 48 native event document titles. Native paths, authored event headings and all non-title event fields remain intact.
- Adopted Tide's Site header/navigation list/link and Skip link recipes. Removed private link/helper appearance and narrow-screen link hiding; all main destinations wrap naturally. Saved uses the ordinary text navigation recipe alongside the other header destinations.
- Derived `aria-current="page"` from exact native route/destination matches. Sunshine Theater identifies its own page; category results, scoped empty views and event details no longer imply that another collection page is current. Kept the focusable skip destinations and optional split-view detail jump.
- Extended application navigation/focus-target contracts and recorded responsive, all-theme and Chromium keyboard verification in [navigation and titles](NAVIGATION-TITLES.md). All canonical edits remain in Lineup; Tide and shared sources are unchanged.

## 2.1.0 · 2026-10-27

- Moved the single browse heading out of the native filter popover into the ordinary application layout. Phone/tablet headings remain exposed with Filters closed; desktop retains the first-column heading above bounded controls and results beside it. Updated native month-target clearance and short-window heading space.
- Added three venue-owned empty documents for Comedy, Workshops and No results. All/Music share the existing six-music-sample venue document. Result links, native venue Reset/form action and recovery remain at Sunshine Theater; an explicitly named link exits to all Albuquerque events. Every empty view retains venue information, with a visible same-document information jump.
- Added application regression coverage for heading uniqueness/placement, scoped destinations, venue information/recovery and global-versus-venue reset behavior. Kept all original paths, IDs, the original control set, authored data and zero browser JavaScript. Tide and shared repository sources are unchanged.
- Recorded all-theme type/heading/layout checks, native venue journeys, month jumps, drawer resize/focus and short desktop coverage in [the verification contract](HEADINGS-VENUE-SCOPE.md).

## 2.0.5 · 2026-10-27

- Corrected Saved's two-track desktop placement: results occupy column 1 and detail occupies column 2. Browse pages retain their explicit three-column overrides. Saved's list is 352px at 1200px and 390px at 1440px; no unused first or implicit third track remains.
- Restored Tide's result-summary and calendar recipes. The application context label now sits in its own wrapper beside the canonical Results block. Removed private type/spacing/border aliases from result counts and month headers, including the smaller calendar year. Counts/month titles use the kit's 14px/24px type.
- Removed the shared private heading aliases and caption-size override from page introductions, including submission. Tide owns their title, supporting-copy type and internal rhythm. Updated native month-target clearance for the canonical result row and Saved intro.
- Added application-only regression checks that join rendered public/private classes before checking typography ownership. Verified rendered parity against the unchanged kit in every theme/mode, plus responsive placement, native month navigation and the phone drawer. See [verification and limits](SAVED-TYPOGRAPHY.md).

Tide UI remains **1.10.0**, unchanged. Layout family remains **option 1**. Native paths, IDs, authored event data, form controls and the zero-browser-JavaScript boundary remain in place.

## 2.0.4 · named baseline

The existing events application was named Lineup and moved to its own canonical home without changing its application sources or generated route documents. The [initial audit](AUDIT.md) records that baseline and its findings. Earlier application releases remain preserved in Git history and the repository changelog.
