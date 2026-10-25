# Sample events and venue facts

The 54 event entries are authored interface samples, not user submissions or live listings. `data/original-sample-events.json` records the original 48; `data/sunshine-sample-events.json` records the six accepted Sunshine Theater fixtures. Those two files remain provenance records. `data/events.json` is the canonical 54-event fixture extracted from the approved HTML; it supplies list/card fields and structured individual details. Shared templates and search assertions consume the same events. It preserves the authored ordering, display text, dates/times, exact venue IDs and search strings. The saved and venue collections reuse those records. Individual event detail content is stored in each record’s `detail` object; shared presentations preserve common labels and existing variants. No raw event HTML is stored in the fixture, and no CMS ingestion pipeline is introduced. `data/import-provenance.json` hashes the preserved input pages/runtime before import.

The six sample shows are High Desert Signal, The Midnight Electric, Sunday in Stereo, Voices on Central, After the Last Train and The Long Weekend. Their ticket prices, age conditions, times and descriptions are fictional event-specific details. The illustrative concert image does not depict Sunshine Theater; each show discloses this.

Venue facts retain their accepted **October 24, 2026** verification date and source attribution. They have not been newly re-verified for this release:

- [Official contact page](https://sunshinetheaterlive.com/contact_page): 120 Central Ave SW, Albuquerque NM 87102; 505-764-0249.
- [About Sunshine Theater](https://sunshinetheaterlive.com/page/about-sunshine-theater): historic Sunshine Building, downtown near Central and Second.
- [Official visitor FAQ](https://sunshinetheaterlive.com/page/frequently-asked-questions): primarily standing-room general admission, limited first-come seating, no re-entry; assistance note directs patrons to the manager on arrival.

Access facilities are not inferred. The guide asks visitors to contact the venue about entry, seating and access needs. Ages, prices, door times and show times belong to individual events. The six-show schedule is explicitly labeled as samples and links to the official site for actual listings.
