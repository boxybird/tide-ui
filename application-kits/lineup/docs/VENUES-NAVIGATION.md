# Primary navigation and Venues · Lineup 2.2.0

The menu/route addition below is retained in 2.2.1. Its initial phone wrapping has since been replaced by the [native mobile Menu](MOBILE-NAVIGATION.md); the 2.2.0 measurements remain historical evidence for that change.

The primary menu consistently offers Find Events (`index.html`), Venues (`venues.html`) and Add an Event (`submit.html`). Saved remains a distinct utility; Help appears in the shared site footer. Sunshine Theater is reached through the directory and existing event/venue links instead of occupying a global menu slot.

Only an exact current destination receives `aria-current="page"`; an event or venue-detail route does not mark its directory or homepage as the current page. Native header omission on phone event details is retained.

## Reuse and responsive boundary

The header keeps Tide 1.12.0's shell, navigation actions, spacing, target sizes and states. Lineup's existing private grid and wrapping remain the baseline for the next responsiveness review: brand/Saved occupy the first phone row, navigation wraps in its second-row cell, and Filters stays at that row's far right. Content pages without Filters give navigation the full second row. Longer labels can create additional lines. No collapsed menu, script, fixed phone height or reduced control padding is introduced.

The directory uses the canonical Content page and unframed Venue card recipes. Its one entry links to the existing Sunshine Theater profile, `#results` and `#venue-information`. Address/description reuse existing authored profile information; no new fact research or real-listing claim is made. No event photograph is presented as a venue photograph, and no placeholder destinations or invented profiles are added.

The 2.1.9 filter heading, drawer clearance and compact choices remain intact. This addition changes no filter behavior, event data or operational services. Tide sources and the separate consumer experiment remain unchanged.

## Sources and migration

`data/pages.json` registers the new route; `src/pages/venues.html` supplies authored content through the existing renderer. There are 68 routes per mode, 65 workspace routes, four unique page fragments and fourteen non-event contexts. The default and ten theme/mode combinations yield 748 application documents. Original routes remain.

Header-template consumers replace `SECONDARY_HREF`, `SECONDARY_LABEL` and `SECONDARY_CURRENT` with fixed Venues/submission destinations and `VENUES_CURRENT` / `SUBMIT_CURRENT` values. Obsolete `secondaryNav` metadata is removed. Include the new route, preserve native links and exact current-page semantics, and keep Saved separate. The [consumer integration guide](CONSUMER-INTEGRATION.md) retains the runtime boundary.

## Verification · 2026-10-28

- Forty theme/viewport cases cover index and directory in all ten theme/mode pairs at 390 and 1440×900. All three primary links remain available, with one h1, no scripts or horizontal overflow. Desktop primary/Saved separation remains 24px.
- Six additional cases cover index, directory and submission at 320 and 1024×900. Controls retain at least 44px targets and do not overlap. At 320px the current home-page grid wraps the primary links into three lines; directory/submission pages use two. At 390px the home menu also uses three lines, while the directory's full-width navigation fits one. These observations inform the next responsive-design pass; this change does not claim that wrapping is the final phone design.
- Native journeys cover directory to venue profile/information, Add an Event, Saved, footer Help and return to Find Events. Venue information fragments and the six scoped venue events remain intact. Current-page state follows the actual route.
- The tablet filter panel still has 24px heading clearance, 44px category steps and exactly one original query control. Source fingerprints confirm the four 2.1.9 filter-template/style files remain unchanged by this menu task, along with all protected Tide/reference-site/shared-tooling sources.

Root build/check pass: 748 application documents, 72 Tide tests, 43 application tests and the 7-test HTTP suite. The new application test covers directory/profile/fragment destinations and the absence of filter controls; existing navigation tests now enforce the consistent menu across all 68 routes.

Measurements and screenshots remain ignored under `build/qa/lineup-real-navigation/`. Browser evidence is in-app Chromium on Windows with viewport emulation. Firefox/Safari, physical devices, screen readers, text zoom and changed system reduced-motion/forced-color settings remain unverified. Canonical component CSS is unchanged; no new hover/focus styling is claimed.

## Current directory · 2.3.0

The one-entry baseline above is superseded by the six-entry native [list/map directory](VENUE-DIRECTORY.md). Rows consume the same photo-free Tide listing treatment as Find Events; individual venue documents retain their images. Five additional venue documents expose existing fixture events without adding new factual profiles. Shared navigation, exact current-page behavior, Sunshine Theater information and all original destinations remain.
