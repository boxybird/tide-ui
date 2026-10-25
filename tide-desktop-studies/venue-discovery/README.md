# Venue discovery — separate app study

Open the [study guide](http://127.0.0.1:4187/venue-discovery/index.html), [start with an event](http://127.0.0.1:4187/venue-discovery/app/high-desert-signal.html?inspect=1&preview-filters=open), or [visit Sunshine Theater](http://127.0.0.1:4187/venue-discovery/app/sunshine-theater.html).

The approved 283-file Shared Filters baseline, kit and accepted sticky-heading fix remain untouched. This independent copy consumes the frozen kit directly. It retains 48 existing samples and adds six fictional Sunshine Theater shows across October/November. No live event import, booking, venue following, directory or CMS is added.

## Journey and state

- A linked venue name in the event facts and a More events at Sunshine Theater action open the venue destination.
- The venue destination shows six upcoming authored samples and useful venue information. The global feed retains all 54 events.
- Selecting a venue event carries the exact `venue=sunshine-theater` identity through real HTML links. The venue context remains visible in the list; returning to the venue keeps applied refinements.
- Query, date and category filters refine the venue's events. Reset all and clear links clear refinements, not the venue. An explicit All events/Find events link exits venue context.
- Empty filtered results keep the venue information available. Venue identity and free-text keyword matching remain separate.
- Desktop/tablet retain the bounded list and natural right document; the venue guide occupies the existing detail slot. Phone leads with the venue name, address and upcoming events; Venue details jumps to the full guide below. Event selection retains the original full-screen phone event destination.
- The accepted feed stacking correction is carried forward as `.tide-venue-study__feed { isolation: isolate; }`, beneath the permanent desktop summary. No new scroll owner or global z-index is added.

## Component ownership

The frozen kit owns Event card/Date/Badge, Event hero/Details, Page intro, Summary, Notice, Link/Button, Field/Choice, calendar groups, Empty and Filter panel. Existing Manrope/type/color/space/radius inputs are unchanged. `app/css/host.css` is byte-identical to the baseline.

Private `tide-venue-study` rules in `css/venue.css` own feed stacking, guide placement and spacing. No public kit component or registry entry is added. The venue guide is a composition of existing components, pending review. `app/js/venue-context.js` owns the visible venue context; copied search scripts serialize and match its exact ID. Routing and data matching remain host behavior. No nested interactive link is added to a whole-card link; venue entry links live in the event detail.

The builder reads the preserved event-card/detail markup helpers without writing to that study. All generation writes only this copy. Original source HTML remains the real navigation fallback; JavaScript enhances filtering and venue context.

## Source facts versus fixtures

Venue facts were checked on October 24, 2026 against [official contact](https://sunshinetheaterlive.com/contact_page), [about](https://sunshinetheaterlive.com/page/about-sunshine-theater) and [visitor FAQs](https://sunshinetheaterlive.com/page/frequently-asked-questions). They cover the downtown location, address, telephone, standing-room seating and re-entry. The access note deliberately does not promise unconfirmed facilities. Practical venue links point to the official website and directions.

All six added shows, prices, admission ages, descriptions and doors/show times are authored fixtures. The existing concert image is illustrative and does not depict Sunshine Theater. The page labels its sample schedule and links to the official calendar for real shows. Age and admission conditions belong to each event rather than the venue record.

## Build and checks

```text
python -B tools/build.py
python -B tools/build.py --check
python -B tools/check.py
node tools/test-venue.cjs
```

Checks write only this copy. They verify HTML semantics/links/BEM ownership, source consistency, exact venue scoping and preservation of the approved baseline, accepted sticky fix and previous studies. Actual browser evidence and verification limits are recorded in `qa/`.
