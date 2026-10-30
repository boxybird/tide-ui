# Sunshine Theater / Midnight Electric review · October 30, 2026

Accepted checkpoint Lineup 2.4.3 / Tide 1.12.0 on `main`, preserved as `lineup-v2.4.3`. Review [Sunshine Theater](http://127.0.0.1:4187/events/app/sunshine-theater.html), then select [The Midnight Electric](http://127.0.0.1:4187/events/app/midnight-electric.html). This records the accepted pair before the broader venue/event rollout.

## Composition and journey

- Both pages use the original centered 20/35/45 desktop shell, header width, persistent filter rail, bounded middle list and natural right document. The earlier two-column Sunshine experiment and its separate filter host have been removed.
- Both lists contain the same six Sunshine events in their existing month groups. The permanent summary visibly says “Events at Sunshine Theater” and offers Venue details. Midnight Electric remains in that list with its existing In view selection.
- Sunshine keeps its venue name, proportionally sized existing photo, visitor facts, contact details and source links on the right. Midnight Electric uses its unchanged event hero and full detail template on the right; a pre-increment comparison verifies that complete detail markup is identical.
- Search is labeled “Search this venue,” with the “Event or artist” placeholder and hidden Sunshine venue scope. On Midnight, the native search action and Reset return to Midnight, retaining the selected event. All venue events opens Sunshine; All events across Albuquerque and Find Events return to the global collection.
- Below 75rem, the original native non-modal filter drawer is retained. Below 60rem, the original event-first presentation remains; Midnight’s existing Sunshine Theater link and More events at Sunshine Theater action lead to the venue list. The event hero, back control, Saved control and native destinations are unchanged.
- Shared Tide components and appearance remain read-only. No browser script, runtime matching or custom history is added.

## Review boundary

Only `midnight-electric.html` is opted into venue-scoped event browsing, through the explicit `VENUE_EVENT_ROUTES` review set in the application renderer. Sunshine and its three existing authored result states share the restored venue shell. The other five Sunshine event pages and all other venues retain their previous behavior at this checkpoint; selecting one of those unconverted events still opens its global event list. Their links are preserved.

The rendered baseline includes the preceding standalone-venue width draft. Only five documents change: Midnight Electric, Sunshine Theater, Sunshine comedy, Sunshine workshop and Sunshine empty. The other 68 routes keep their exact rendered bytes. The five standalone venue pages retain their previous width-review draft.

Ignored evidence lives in `build/qa/sunshine-context-review/`: initial route hashes, the original Midnight detail markup, shared tracked-source hashes, screenshots and verification records. The previous `build/qa/sunshine-refinement/` evidence describes the superseded two-column review.

## Verification and limits

`npm run build` and `npm run check` pass, including all 139 tests (55 application, 72 shared contracts, seven HTTP and five map tests). Application checks cover exact venue membership, retained selection/detail markup, scoped actions/reset and unchanged global collections. The separately authorized one-line `tools/check.py` update is included: Midnight Electric now expects six authored event cards instead of the old global count of 54. No assertion was removed; the application test independently verifies exact six-event membership.

- Chromium layout checks at widths 1920, 1440, 1200, 960 and 390px found no horizontal overflow. Homepage, Sunshine and Midnight have identical header bounds at desktop/split widths. At 1920px, all three headers are 1472px wide and centered at x≈216.3px; at 1440px their bounds also match exactly.
- Application CSS is 21,832 bytes raw / 4,018 bytes gzip, within the unchanged 22,000 / 5,000 limits.
- The left/middle panes retain 24px bottom clearance. At 1200×800, a November fragment lands at the feed top (y≈241.7px), below the permanent summary (bottom≈233.7px), and Midnight remains selected.
- Followed Sunshine → Midnight and confirmed six Sunshine events, Midnight selected and the original event hero. Tested Midnight’s scoped form/Reset destinations and Escape with focus returned to Filters. Its existing mobile venue-events link returns to Sunshine’s six-event list.
- Checked the 390×844 mobile event presentation and 320×568 venue drawer. The drawer body scrolls, the footer ends at the viewport bottom, and there is no horizontal overflow. Mobile event hero, hidden list/header behavior and venue links retain the original presentation.
- All 20 themed review pages (two routes × five themes × two modes) load their images, display six cards, preserve Midnight selection, expose the desktop rail and avoid horizontal overflow. These were DOM/layout checks, not a new contrast audit.
- All three authored venue empty states preserve venue information and recover to the six-event venue page. The other 68 documents are byte-identical to the starting state; Midnight’s complete detail markup is also byte-identical. Tide and site tracked-source hashes match. The approved fixture-count correction is the only shared-tooling change.
- Evidence includes `sunshine-desktop.png`, `midnight-desktop.png`, `midnight-mobile.png`, `sunshine-mobile.png`, `layout-checks.json`, `theme-checks.json`, `empty-state-checks.json`, `verification.json` and `check.log`.

Search/date/category inputs remain native UI specimens. Query parameters do not perform live filtering; the existing authored result documents remain the result-state contract. The six events and image are authored samples; no venue facts or image provenance were newly verified. Browser evidence is Chromium on Windows; Firefox, Safari, physical devices and screen readers are not covered.
