# Lineup application-kit changelog

## Consumer integration documentation · 2026-10-28

- Added a framework-neutral [consumer integration guide](CONSUMER-INTEGRATION.md) covering the existing document/form/region composition, native fallback, optional navigation, collection loading, focus/history, failures, motion and upgrade responsibilities.
- Linked the guide from the README, handoff, starter, runtime and ownership documents. Distinguished current private markup from a public integration API and kept the external consumer experiment separate.
- Documentation-only clarification: Lineup remains 2.1.8 with Tide 1.12.0. Application sources, fixtures, styles, assets, tests, manifests and browser behavior are unchanged; no runtime dependency or Tide recipe is added.
- Verified `npm run build` and `npm run check`, including 72 Tide tests, 42 application tests and the local HTTP suite. The first HTTP run was blocked by sandbox loopback access; the final run passed with local access. Documentation links resolve, and source/output fingerprints match. No browser interactions were changed or newly exercised for this documentation update; the external experiment's browser limits remain as stated in the guide.

## 2.1.8 · 2026-10-28

- Hid the event photo's top-left return link from 60rem, matching the breakpoint where the event list and detail appear together. Retained the working native link on smaller event documents.
- Used private application hosts to control availability, preserve the optional Saved control's position and omit an empty toolbar. Shared Tide sources, event content and pane geometry are unchanged.
- Recorded the expectation that consuming websites can adopt later Lineup releases independently, with release notes and migration guidance. The current workflow uses reviewed source updates; detailed extension boundaries remain a separate discussion.
- Verified 25 route/viewport cases and 20 all-theme cases, breakpoint visibility, keyboard omission, native mobile return and browser Back. See [design QA](../design-qa.md).

## 2.1.7 · 2026-10-28

- Moved the primary navigation beside Saved on the right, separated by a named 24px external gap. Below 60rem, Burque and Saved occupy row one; primary links and the right-aligned Filters trigger occupy row two. Links wrap naturally on small phones.
- Kept Tide 1.12.0 unchanged. A private application grid composes the existing Site header shell, navigation actions and original native Filters button without overriding component appearance or the centered kit recipe.
- Preserved all main content, desktop/split-tablet pane geometry, native routes/current-page semantics and the single popover control set. See [header navigation](HEADER-NAVIGATION.md) and [design QA](../design-qa.md) for responsive and ownership evidence.

## 2.1.6 · 2026-10-27

- Adopted reviewed centered primary navigation and separate Saved using Tide 1.12.0's opt-in recipe. Kept native route/current-page semantics, source icon and the original Filters trigger.
- Application stylesheets, data and main content are unchanged. See [header navigation](HEADER-NAVIGATION.md) for ownership, parity and verification.

## 2.1.5 · 2026-10-27

- Implemented the selected compact Search & filters / result-count headers using Tide 1.11.0's canonical utility variant. Removed the Coming up intro, general tagline and repeated The lineup context label.
- Kept the count heading outside the drawer, one visible h1 per document, a contextual accessible name, the original form/controls, 20/35/45 desktop columns, permanent summary, complete isolated feed and natural detail document. Native event titles remain h1; Saved retains its default Results recipe.
- Preserved venue information/recovery, native drawer/resize/reset/focus behavior and month navigation. Updated application geometry, heading contracts, visual comparison and responsive evidence in the [compact-header record](COMPACT-HEADERS.md).
- The user reviewed and accepted both the authorized Tide recipe and application changes for preservation on main.

## 2.1.4 · 2026-10-27

- Removed tutorial result-state navigation, duplicate sample counts, example search/category labels and explanatory demo text from the application. Retained the native search form, dates/categories, Reset, venue context and useful recovery links.
- Cleaned Help, submission labels, page metadata, footer and event prose into ordinary product copy. Moved fictional-content/photography provenance and static-service limits into the [handoff contract](HANDOFF.md). All event IDs, routes, dates, prices and venue facts remain intact.
- Retained the existing native popover and modern CSS drawer: transitions, reduced motion, pinned footer, desktop anchors and one control set. No browser JavaScript was present or added. Reference result documents remain available from the kit review entry, outside the application navigation.
- Updated application contracts and verification for the handoff. Tide and shared repository sources remain unchanged.

## 2.1.3 · 2026-10-27

- Completed strict one-to-one adoption of Tide 1.10.0 HTML/CSS. Search now uses the real Field label/wrapper; fieldsets use the canonical Stack recipe. Links and supporting/footer copy use kit typography. Cards use the current category/metadata markup, and the panel uses its semantic footer recipe.
- Removed private hero padding/scrim/photo-reserve, component safe-area/print appearance, compact link type, selected-card outline suppression and inward focus-ring overrides. A private outer header wrapper owns the sticky canvas; Tide owns header interiors. External filter wrappers reserve room for canonical outward focus rings.
- Added application-only strict appearance/interior guards, primitive/field/card/footer markup coverage and reproducible Tide-only browser probes. Recorded full-route responsive comparisons, all-theme component comparisons, native journeys and shared-source fingerprints in the [completed alignment record](TIDE-ALIGNMENT.md).
- UI alignment is complete. Personalization remains a separate task. All changes are inside Lineup; Tide and shared sources are unchanged.

## 2.1.2 · 2026-10-27

- Restored Tide's Filter panel rail footer and wrapping status row. Removed private footer/status/count aliases, forced Reset whitespace and count alignment. Two private child wrappers reserve narrow drawer start/bottom safe-area clearance while leaving the public footer a direct child of the rail with its canonical padding/gap.
- Corrected the private header-row allowance from 44px to the existing 48px control input only when Filters is present in the 60–75rem split range. Tablet panes now retain their documented 24px bottom clearance. Saved/navigation-only and permanent-desktop headers keep the 44px input.
- Added focused application ownership guards for all properties on rendered footer/status/count aliases and the Reset hook. Preserved the original form/control set, native Reset/venue routes, drawer dismissal/resize behavior and zero browser JavaScript. See [verification](FILTER-FOOTER-TABLET.md).
- Tide 1.10.0 and shared repository sources are unchanged. The fresh audit's R01/R02 findings are resolved; historical evidence remains intact.

## Audit checkpoint · 2026-10-27

- Re-audited Lineup 2.1.1 with fresh phone, portrait/split-tablet and desktop evidence, all-theme component comparisons and native journeys. The six original fixes hold; two application-only findings remain: R01 pane bottom clearance and R02 Filter panel internal footer/status-row overrides. See [the report and testing limits](FRESH-AUDIT.md).
- Updated only Lineup documentation and retained audit evidence. Application templates, CSS, data, assets, tests and version remain unchanged; Tide, shared tooling and the reference site remain unchanged.

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
