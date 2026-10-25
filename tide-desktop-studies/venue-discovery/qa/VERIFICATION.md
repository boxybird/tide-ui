# Venue discovery verification — 2026-10-24

## Scope

This is an independent Bumble Dark app study, consuming the frozen kit. It adds six authored Sunshine Theater shows to the existing 48 samples and one venue destination. Venue facts come from the official contact/about/FAQ pages cited in the README and venue guide. No real show listings, ticket inventory, API, venue following or CMS is introduced.

## Source and preservation

The source checker verifies 61 HTML pages, working local references/fragments, one H1/main, unique IDs, valid date/time attributes, control associations, private/shared BEM ownership, source/build consistency and six venue-only cards in the static venue destination. The copied base host CSS remains byte-identical; private CSS uses existing tokens and composition classes only.

All 283 approved baseline files and all 11 accepted sticky-fix source/snapshot/evidence files are checked by their existing hashes. Earlier frozen kit/app inventories are also checked through the preservation chain. QA writes stay here; no writer or builder runs in a frozen release.

Sixteen search assertions cover the 54-event global feed, exact six-event venue scope, query/category/date combinations, zero and one result, default venue context, URL serialization, invalid ranges and the distinction between resetting refinements and leaving a venue.

## Browser observations

Actual browser: connected Chromium on Windows. The entry event's linked venue opens Sunshine Theater's guide and its six-event schedule. Selecting Sunday in Stereo carries `venue=sunshine-theater`, keeps the six-event list and provides a return link to the venue. Search for ink yields no venue results even though it matches global events. The venue guide remains available beside that empty result. Reset/apply restores all six venue events. An exact October 30 range yields one event and removes unnecessary month jumps; refresh retains that date and venue. Explicit Find events returns to all 54 samples.

Responsive inspection covers 320 × 740, 390 × 844, 1024 × 768 and 1440 × 900. The tested venue pages have one H1, no horizontal overflow and the correct six cards. Phone shows the venue name/address, schedule and a real Venue details fragment link to the guide below. That destination accepts native focus and clears the sticky header. The phone filter drawer applies one matching venue event; choosing it opens the original full-screen event composition and retains a return link to the filtered venue.

Desktop/tablet use the existing bounded list and natural right-side guide/detail document. The accepted feed isolation rule is applied to every generated search feed, keeping calendar headings below the permanent desktop summary. The guide is a shared-component composition rather than a new kit block.

At 1440 × 900 the measured native gutter is 10px, the list/detail gap is 24px, bottom clearance is 34px, and Show events and the list both finish at y866. At a real month handoff (list offset 459.3333px), the outgoing October header geometrically crosses the summary area but its pointer hit points still resolve to the summary. All twelve recorded interaction/geometry checks pass. The refined phone details jump places its focused destination at y121 below the y97 header.

Detailed values and interaction results are in `browser-checks.json`; source results are in `checks.json`. Screenshots are actual viewport captures. Firefox/Safari, physical devices and screen readers were not tested; their earlier deferral remains in place. This is not a claim of full accessibility compliance.

## Ownership and future review

The new screen reuses Event card/Date/Badge, Hero/Details, Page intro, Summary, Notice, Link/Button, Field/Choice, Empty, calendar groups and Filter panel. New private composition owns only venue context, guide placement and spacing, fragment clearance and local feed isolation. An accepted reusable venue information composition could move into a later kit release with full registration and specimens; this study does not alter the current kit or close that adoption decision.
