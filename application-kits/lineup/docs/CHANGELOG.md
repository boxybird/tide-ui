# Lineup application-kit changelog

## 2.4.5 · 2026-10-30

- Sunshine Theater adopts the existing Tide photo hero: full-column image, canonical scrim, eyebrow/title/subtitle and venue facts/visit links over the photo. Seating, access and venue guidance remain below. No Tide changes.
- A venue-owned `profilePresentation` setting keeps the markup composition scoped to Sunshine and its three existing authored result states. All other 69 HTML routes remain byte-identical, including all event pages. The accepted hero and height treatment is preserved as `lineup-v2.4.5` on `main`.
- Sunshine and its six event pages share a screen-only 52rem preferred hero height. The application owns this outer geometry; intrinsic content may exceed the target so facts, actions and enlarged text are never clipped. Other venue scopes and global previews keep their existing sizing.
- Build/check pass with all 139 tests. Chromium checks cover 1440/960/390/320px widths, all ten theme/mode variants and the native venue-information link. No horizontal overflow; the photo meets the detail column’s top and side edges. Firefox, Safari, physical devices and screen readers are unverified. Evidence: `build/qa/sunshine-venue-hero/`.
- Height follow-up: Chromium checks all seven populated Sunshine pages at 1440×1000, 1200×800, 960×800, 390×844 and 320×568: every hero is 832px high, with no content clipping or horizontal overflow. The venue/Midnight pair also passes all ten theme/mode variants. At 1440×1400, the retained Tide viewport-based photo reserve requires 912px for venue content and 976px for events; the intrinsic safety fallback intentionally allows these heights. This is a common preferred height, not a hard maximum. Other venue/global preview geometry remains unchanged. Evidence: `build/qa/sunshine-hero-height/`.

## 2.4.4 · 2026-10-30

- Applied the accepted Sunshine/Midnight composition to all six venue pages and all 54 event pages. Lists, counts, visible venue context, search actions, Reset and venue-detail links stay within the current venue; Find Events remains global.
- Reused the original 20/35/45 desktop shell, header width and responsive drawer. Preserved every event hero/detail and the accepted Sunshine/Midnight documents exactly. Five former standalone venue pages now share the same workspace/profile partials; their names, types, photos and directory return links remain. Removed the superseded standalone width CSS.
- Kept Sunshine visitor facts in authored HTML. No invented venue facts, demo disclosures, new runtime behavior or Tide changes. Updated the previously authorized shared fixture-count check to derive each route’s expected venue membership count, with independent exact-membership application tests.
- Build/check pass with all 139 tests. Browser checks cover all 60 venue/event routes, 120 theme/mode cases, responsive geometry and native venue/event/reset/drawer journeys. See [verification and limits](VENUE-CONTEXT.md).

## 2.4.3 · 2026-10-30

- Restored Sunshine Theater’s original three-column desktop shell and header width, retaining its name and photo. Scoped Midnight Electric’s existing list and filter controls to Sunshine’s six events, preserving the selected card and unchanged event hero/details. This accepted checkpoint covers the pair plus Sunshine’s existing result states; other events retain their prior behavior. See [Sunshine / Midnight review](SUNSHINE-REVIEW.md).
- With explicit authorization, updated the shared repository fixture-count check to expect six cards on Midnight Electric; the new application contract also verifies their exact venue membership.
- Removed the illustrative-photo/authored-sample disclosure from the five standalone venue pages. Fixture and image provenance remain in developer documentation.
- Added one private width wrapper around the unchanged Tide Content page. The current review uses a centered 48rem (768px) image/event-list column with the existing responsive insets. Captured 40rem and 56rem alternatives for comparison from this same source; width choice is awaiting user review. See [venue page width review](VENUE-PROFILE-WIDTH.md).
- The application CSS compactor omits optional final declaration semicolons and compacts whitespace across removed comments outside protected strings/URLs. Declaration-parity checks and the original asset budget remain unchanged.

## 2.4.2 · 2026-10-29

- Below 60rem, outline the marker whose native venue preview is open. The application-owned marker host uses the existing map selection accent; native close, Escape, outside dismissal and switching previews clear or transfer it automatically.
- Keep fragment-based marker highlighting on the split-layout link, so a previous desktop selection cannot leave a second compact marker highlighted. Desktop interaction and appearance are unchanged. No runtime, fixture, template or Tide changes. See [verification](MOBILE-MAP-PREVIEW.md).

## 2.4.1 · 2026-10-29

- Compact map markers now open a native, non-modal venue preview instead of navigating to the hidden list. Each uses the existing Tide Panel, name/type/count roles, Close control and direct venue-details link. Native Escape, outside dismissal and keyboard focus return stay browser-owned.
- Private CSS anchors the panel above its marker with viewport-edge placement fallbacks. At 60rem and above, the existing marker link selects the visible list; no popup is exposed. Open previews close on entry to the split layout or a native fragment change.
- Preserved compact list-to-venue navigation, the real dark map, all fixture IDs/counts, desktop selection and Tide 1.12.0. The same native preview works over the illustrated map fallback.
- Registered one shared preview partial and extended the existing venue contract test. The map stylesheet now uses the existing lossless CSS compactor at build time, keeping the original asset budgets and pinned vendor bytes unchanged. See [behavior and verification](MOBILE-MAP-PREVIEW.md).

## 2.4.0 · 2026-10-29

- Consolidated the approved Consumer Lab 0.4.2 map into this application kit; the normal build now combines the current 2.3.2 source and the map, with no copied snapshot. Preserved pinned MapLibre bytes, the dark style and demonstration coordinates.
- Preserved the fixed venue workspace, list-owned footer, map/list bottom alignment and overlaid selection actions. All other document scrolling remains unchanged.
- Registered the map as the only browser-JavaScript exception, updated module MIME/asset budgets and added current-build/dependency/route checks. Archived the old consumer history, retired its separate preview and checkout, and recorded one-source/incremental-commit rules. See [source of truth](SOURCE-OF-TRUTH.md).

- Venue cards open the venue and its event collection below 60rem, where List and Map are separate views. At 60rem and above, cards still select the adjacent map point. Private responsive hosts expose exactly one native covering link per card; the separate venue-details link and map controls retain their destinations.
- Matched the venue directory summary's mobile spacing to Find Events below the 34rem dropdown-menu breakpoint by removing its extra 12px top gap. Both rows continue to use the unchanged Tide Results utility recipe for typography, alignment, padding and divider. Wider layouts retain their existing spacing.

## 2.3.2 · 2026-10-29

- Corrected the seven actionable findings from the October 29 UI/UX audit, with Tide 1.12.0 unchanged. Missing live information and the intentional submission endpoint remain sample/integration boundaries.
- Separated the 44px map targets at compact sizes and repositioned their labels. The directory has a 48rem minimum document frame so short windows scroll instead of shrinking the illustration until controls collide. Compact selected labels retain the venue name in the existing caption.
- Added authored native List/Map states with a check icon and `aria-current="location"`; only the matching navigation is exposed. The URL fragment controls the panel and state together. Removed the focus-based map override that prevented Back from restoring the list.
- Added the existing Saved navigation utility to concise details and existing venue destinations to all 54 event details. No save persistence or new venue information is introduced.
- Made the zero-result preview agree with the empty collection and omitted populated-feed completion text there. Removed redundant Saved footer reassurance.
- Rendered H3 event-card titles below H2 collections on the five standalone venue profiles while preserving H4 titles within month groups and the unchanged Tide typography.
- Consolidated application CSS rules within the existing asset budget; no public component styling or shared build tool changed. Extended regression contracts for navigation destinations, heading contexts and empty/Saved copy. See [verification and consumer notes](AUDIT-CORRECTIONS-2026-10-29.md).

## 2.3.1 · 2026-10-29

- Preserved the user-approved selection refactor at `lineup-v2.3.1` before real-map integration work. The 2.3.0 foundation remains separately tagged. Tide is unchanged; the native kit still ships no browser JavaScript or map-provider dependency.

- Made venue cards select their map point with native fragments; View venue details is now the deliberate document link. Map markers reveal their corresponding row in the bounded list. Selected map-caption links provide direct details and a return to the same row.
- Used unchanged Tide Badge, Event card, Link and 44px Photo control recipes. A single native target identifies the selected venue in both views; other map labels temporarily hide to keep selection readable. The earlier marker popovers are replaced by this selection/caption treatment. Menu and filter popovers remain unchanged.
- Fitted the complete illustration at every width so selected points remain reachable, resolving the known tall-tablet clipped marker. Native root scroll padding keeps fragment selection inside the panes while preserving keyboard access to the footer. Smooth list movement honors reduced motion. Progressive `scroll-initial-target` restores the selected row on document return in supporting browsers; exact cross-browser restoration is not promised.
- Preserved the 2.3.0 foundation at `lineup-v2.3.0`, all venue/event IDs, the compact heading/search, individual venue documents and Tide 1.12.0. No geographic camera, map provider, browser JavaScript or consumer-test runtime is added.
- Updated bidirectional-link/selection contracts. Chromium checks cover all six selections at seven viewport sizes, all ten theme/mode pairs on phone/desktop, keyboard selection, offscreen row reveal and direct details/Back journeys. See [venue directory](VENUE-DIRECTORY.md) for evidence and limits.

## 2.3.0 · 2026-10-29

- Preserved the user-approved venue list/map foundation at tag `lineup-v2.3.0`. This checkpoint is the starting point for further iteration; individual venue-page refinement and the recorded tall-tablet map clipping issue remain separate work. Tide stays at 1.12.0 with no shared-source change.

- Adopted the reviewed list/map venue direction using unchanged Tide Utility results, Event list/card, Panel, Photo control, Button and Link recipes. The directory owns its responsive grid and native list scrolling and a fitted map frame; its header uses the existing 20px utility type.
- Refactored directory rows on 2026-10-29 after user review: removed list photos and adopted Find Events' canonical card category/title/support/metadata roles, surface, texture, 24px padding and separators. Venue type/name/city and the authored-event count replace event-specific content; each card links to its real venue document with a separate native map action. The desktop list track follows the event feed's 35% width calculation and thin scrollbar. Individual venue documents and map behavior remain unchanged.
- Condensed the directory's top area: retained the Venues / Albuquerque utility heading and native labelled search, removed the tagline and separate venue-count line, and used named 16px external spacing above/below the search area. The desktop heading-to-search gap now matches Find Events, and the search no longer touches the list surface. Mobile List/Map controls retain the same header height in both views. No card or Tide appearance changes.
- Added six venue entries and five native venue/event documents; Sunshine Theater retains its existing factual profile and six scoped events. All original 68 routes and 54 event records remain unchanged; 73 routes now render in each mode.
- Refined the translation after user review: matched the exact Find Events frame/header insets, restored the native venue search field/GET contract, and replaced two-axis map scrolling with a fitted preview. The natural footer stays below the initial viewport.
- Used native fragments for list/map switching and place navigation, and native popovers for map information, Escape dismissal and focus return. No React, HTMX, browser script, live search or map-provider dependency is imported from the separate prototype.
- Added seven optimized concept-image assets with provenance and the Phosphor Square icon license. Each image stays below the existing 200KB limit. Conservative application CSS distribution compaction preserves declarations and the existing 22KB/5KB budgets; canonical styles remain readable.
- Added venue destination/count/escape/popover/asset tests and CSS rule/value parity checks. Browser verification covers 30 theme/state cases, 16 responsive cases, all new venue destinations, native event navigation and Panel parity. See [venue directory](VENUE-DIRECTORY.md). Tide, the reference site, shared tooling and the independent consumer projects remain unchanged.

## 2.2.3 · 2026-10-28

- Extended the accepted desktop utility-summary spacing to mobile and tablet: the application gap is `space-2` at every width, yielding 16px from the divider to the first month title on unscoped browse pages. Removed the redundant desktop breakpoint override; venue context retains its information-jump allowance.
- Kept native month-fragment reservation tied to the same private gap. Desktop, Saved, filter-drawer clearance and Tide 1.12.0 remain unchanged; no browser runtime is introduced.
- Verified eighteen route/viewport comparisons, twenty theme/viewport comparisons, unchanged drawer geometry and native tablet month jumps. Build/check pass with all 124 tests; 135 protected files remain byte-identical. See [design QA](../design-qa.md) for measurements and browser limits.

## 2.2.2 · 2026-10-28

- Aligned the first month title with Search Events from the 75rem permanent-filter breakpoint. Reduced only Lineup's external utility-summary gap from `space-4` to `space-2`, retaining Tide's calendar/header padding and the existing search placement.
- Shared the private gap input with native month-fragment reservation. Preserved mobile/tablet spacing, Saved composition, the natural right document, bounded pane bottoms and zero browser JavaScript. Tide remains 1.12.0 and unchanged.
- Verified eighteen route/viewport comparisons, twenty theme/viewport comparisons, exact mobile drawer parity and native month jumps. Build/check pass with all 124 tests; 135 protected Tide/reference-site/shared-tooling files are byte-identical. See [compact headers](COMPACT-HEADERS.md) and [design QA](../design-qa.md) for measurements and browser limits.

## 2.2.1 · 2026-10-28

- Added the native mobile Menu below a content-based 34rem breakpoint. Menu/Filters share row two; brand/Saved retain row one. Wider screens keep the accepted inline navigation.
- Reused existing Tide navigation buttons, Icon and Panel recipes. Private CSS handles mounting, anchors and responsive availability; the public Panel stylesheet is copied unchanged into generated application dependencies. No Tide edit, browser JavaScript or custom keyboard/history engine is introduced.
- Authored link items once for inline and popup presentations, exposing only the appropriate Main navigation. Preserved the original filter controls and all 68 routes. See [mobile navigation](MOBILE-NAVIGATION.md) for native dismissal, resizing, fallback and consumer migration.
- Verified all ten phone theme/modes, twenty exact desktop header comparisons, small-phone/breakpoint/tablet cases and native navigation/dismissal. Build/check pass with all 124 tests; Chromium coverage and remaining browser limits are recorded.

## 2.2.0 · 2026-10-28

- Replaced the route-dependent secondary destination with consistent Find Events, Venues and Add an Event links. Saved remains separate; Help is available from the shared footer. Current-page states still identify only an exact native destination.
- Added the Venues directory using existing Content page and unframed Venue card recipes. Sunshine Theater links to its profile, schedule and information. No new venue facts, imagery, service behavior or browser dependency is introduced.
- Retained the existing header wrapping and the 2.1.9 filter-panel changes. Tide is unchanged. The application now emits 68 routes per mode, 748 total, with all original destinations preserved.
- Migration: replace retired `SECONDARY_*` header values with `VENUES_CURRENT` / `SUBMIT_CURRENT`, include the new content route, and remove obsolete `secondaryNav` metadata. See [navigation and directory](VENUES-NAVIGATION.md).
- Verified forty themed phone/desktop cases, six small/tablet cases and native directory/navigation journeys. All 122 repository checks pass. Current phone wrapping is explicitly retained for the upcoming responsiveness review, with no overlap or hidden destinations.

## 2.1.9 · 2026-10-28

- Capitalized the visible drawer and desktop utility headings as Search & Filters; the wording is application-owned.
- Added a private content wrapper with Tide's named 24px top clearance below 75rem. Kept the flush public rail body/footer and desktop search spacing unchanged.
- Adopted the existing compact Category fieldset/choice composition from Tide's filter-disclosure specimen. Removed the extra Stack gap between 44px choice targets; date-field Stack spacing remains.
- Preserved the original controls, native popover/reset behavior and zero browser JavaScript. Tide 1.12.0 and shared sources remain unchanged. See the [filter-panel spacing contract](FILTER-PANEL-SPACING.md).
- Verified all ten theme/modes at phone, tablet and desktop widths, boundary/short-screen cases, venue scope and native interactions. Desktop search rectangles are identical to the baseline. Build/check pass, including all 121 HTTP/Tide/application checks; browser limits remain documented.

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
