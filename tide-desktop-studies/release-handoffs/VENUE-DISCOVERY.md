# Accepted carry-forward: venue page and navigation

Accepted by the user on 2026-10-24. Preserve the complete Sunshine Theater venue study and carry its page/navigation patterns into the **next app release**. This does not replace the approved Shared Filters baseline or authorize changes to its UI kit.

Integrated on 2026-10-25 in the separate [app1.1.0 successor](../app-release-1.1.0/README.md). Its [ownership contract](../app-release-1.1.0/docs/COMPONENT-OWNERSHIP.md) maps the accepted composition to the private `tide-app-release` block. New [verification](../app-release-1.1.0/qa/VERIFICATION.md) covers all six modes, scoped search and native venue journeys on desktop/tablet/phone. Original study, approved baseline and UI kit remain unchanged.

## Preserved reference

- Study: `../venue-discovery/`, version 0.1.0. Its source, generated pages, QA and archives are frozen. The historical README's pending-review wording is superseded by this acceptance record.
- Entry event: [High Desert Signal](http://127.0.0.1:4187/venue-discovery/app/high-desert-signal.html?inspect=1&preview-filters=open).
- Venue destination: [Sunshine Theater](http://127.0.0.1:4187/venue-discovery/app/sunshine-theater.html).
- Exact archive: `../venue-discovery/dist/venue-discovery-0.1.0.zip`.
- SHA256: `a0a892b9c355d5e85f0b84b73abe27ce391fb076087d95a955e2dfc3d684ac2f`.
- Full study inventory: `../locks/venue-discovery-0.1.0.json`. Verify with `python -B release-handoffs/check_venue_preservation.py` from the desktop-studies directory. This checker writes its report outside the frozen study.

The snapshot uses the existing sibling `shared-filter-release/kit/` at runtime; it is not a standalone deployment package. The study contains 48 existing samples and six fictional Sunshine Theater events. Its real venue facts are sourced separately from the venue's official contact/about/FAQ pages. Preserving this UI does not turn the sample schedule into live listings.

## Page and navigation contract

| Pattern | Required behavior |
| --- | --- |
| Event → venue | The linked venue name in event facts and a clear More events at Sunshine Theater action open the venue destination. Keep venue links separate from the whole-card event link; never nest interactive links. |
| Venue destination | Show venue identity, address, useful visitor information and upcoming events. Reuse the event cards and calendar groups from the global feed. A venue photograph is optional; the accepted guide works without one. |
| Venue → event | Selecting a show opens its real event URL with the venue context retained. The surrounding list stays scoped to that venue, and a return action leads back to its schedule and applied refinements. |
| Venue identity | Use an exact stable ID, demonstrated by `venue=sunshine-theater`. A venue is separate from the free-text query and from the event organizer. Display-name spelling must not determine which events belong to it. |
| Search and filtering | Query, date and category narrow the venue's events. Count, month counts/jumps, results and selected-event links must use the same scope. Do not allow a keyword match elsewhere to bring another venue into this list. |
| Reset and clear | Reset all clears the query/date/category draft; applying restores all events at the current venue. Clear-search links also retain the venue. The venue alone does not count as an active user refinement or enable Reset all. |
| Leaving the venue | Explicit All events or Find events navigation exits venue scope and returns to the global feed. Reset and clearing refinements must not perform that navigation. |
| Empty filtered results | Preserve venue identity and its useful information alongside recovery controls. No matches does not mean that the venue itself has disappeared. An intrinsically empty venue schedule remains additional integration coverage, not an already-built sample state. |
| Refresh and native navigation | Real links and GET URLs serialize the venue and refinements, making refresh and return destinations reproducible. Preserve normal Back/Forward and modified-click behavior; do not introduce a client router for this pattern. |

The venue guide's address, telephone, directions, official website, seating/entry and access-arrangement notes are distinct from event-specific ages, admission and doors/show times. Do not turn one show's conditions into venue policy. Do not infer unconfirmed access facilities. Preserve source attribution and distinguish factual venue information from illustrative events/images.

## Responsive composition

- **Desktop/tablet:** retain the approved contained workspace, bounded event list and natural right document scroll. The guide occupies the existing detail slot. Selecting an event replaces that destination with its familiar event detail while retaining the venue's schedule.
- **Phone:** lead with venue name, address and upcoming events. Venue details is a real fragment jump to the fuller guide below the list; its destination takes native focus and clears the sticky header. Event selection opens the existing full-screen event composition, with a return link to the scoped schedule.
- Preserve the existing search/filter rail and modal behavior, native controls, focus/cancel behavior, spacing, type and themes. Keep Show events aligned with the list and the dynamic desktop bottom clearance of `24px + occupied native scrollbar gutter`.
- Carry the [accepted sticky-heading hierarchy](STICKY-HEADINGS.md): the complete feed has local stacking isolation beneath the permanent desktop summary. Date groups push each other away underneath that summary without covering its count or controls.

## Ownership in the next release

| Responsibility | Preserved source | Integration home |
| --- | --- | --- |
| Venue guide composition and facts | `venue-discovery/tools/build.py`, `data/events.json`, `README.md` | App page/data composition, with source provenance. Keep venue facts separate from event fixtures. |
| Visible context, entry and exit links | `venue-discovery/app/js/venue-context.js` | Host navigation/context coordinator. |
| Exact venue matching and serialized state | Copied `app/js/search-core.js`, `event-search.js`, `filters.js` | Host search/routing behavior. Retain the venue in form/URL state when resetting other refinements. |
| Placement, fragment clearance and feed stacking | `venue-discovery/css/venue.css`, private `tide-venue-study` block | Documented app composition CSS; map to the successor's private owner rather than adding global component overrides. |
| Cards, dates, badges, hero/details, headings, summaries, notices, links/buttons, controls, calendar groups, empty state and filter panel | Frozen Tide kit | Reuse directly. No primitive, theme, component CSS or registry change is approved by this handoff. |

The venue guide is an accepted app composition, not a newly registered public kit component. If a later release needs a reusable venue block in the kit, give it a separate adoption decision with canonical HTML, states, CSS ownership and all-theme specimens.

## Integration and release checks

1. Create a successor app copy and implement these accepted patterns there. Leave the frozen baseline, kit, venue study and earlier studies untouched. Do not run the frozen study's build/check writers; use the external preservation verifier for that reference.
2. Follow the complete event → venue → another event → venue journey on desktop, tablet and phone. Verify identity, useful facts, all scoped cards, selected-event context and return links.
3. Exercise one match, no matches, query/date/category combinations, Reset/apply, clear-search and explicit global navigation. Ensure a query that matches other venues never escapes the selected venue. Refresh and history navigation must retain the appropriate state.
4. Check the phone venue-details fragment and keyboard focus, modal open/cancel, month jumps/handoffs, short desktop height, zoom and breakpoint changes. Preserve list/detail geometry and the accepted sticky-heading correction.
5. Consume the existing themes through semantic roles; check all six theme/mode combinations when integrating. Register any new host classes and state contracts in the successor's ownership/release documentation. Close this carry-forward item only after integration and verification in that successor.

## Existing evidence and limits

The preserved QA covers 61 HTML pages, 4,935 local references, sixteen venue scope/search assertions and twelve browser interaction/geometry checks. Chromium on Windows was inspected at 320 × 740, 390 × 844, 1024 × 768 and 1440 × 900. The native 10px gutter on that environment produced 34px desktop bottom clearance with Show events aligned. The phone fragment target focused correctly below the header. The outgoing October label remained beneath the summary at an actual handoff.

Source results, screenshots and observed values live in `../venue-discovery/qa/`. Firefox/Safari, physical-device and screen-reader checks remain deferred, not passed. Venue following, a venue directory, live ticketing, submissions and a CMS remain outside this accepted scope.
