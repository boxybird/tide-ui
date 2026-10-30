# Venue and event context · Lineup 2.4.4

The user accepted the Sunshine Theater / Midnight Electric pair and requested the same composition for every venue and event. The accepted pair was committed first as `a37af63`, tag `lineup-v2.4.3`. This rollout continues directly on `main` from that checkpoint. Tide remains 1.12.0.

## Behavior and ownership

All six venue pages use the original centered 20/35/45 desktop workspace, the homepage’s header width, bounded filter/list panes and natural right document. The right column shows the existing venue name, type and photo; Sunshine also retains its previously authored visitor facts. The five former standalone venue pages retain their directory return links. No new venue facts or customer-facing demo disclosures were added.

All 54 event pages derive their venue from the canonical event record. Their lists contain that venue’s events, including the selected event with its existing In view indicator. The complete hero and event-detail markup is unchanged. The permanent summary names the venue and links to its information. Search this venue and Reset retain the current event; All venue events opens its venue page. Find Events and All events across Albuquerque remain explicit global exits.

| Venue | Events |
| --- | ---: |
| Sunshine Theater | 6 |
| Sister | 9 |
| Dry Heat | 13 |
| Barelas Print Studio | 10 |
| The Paper Table | 8 |
| Warehouse Room | 8 |

Below 75rem, the same native filter drawer is used. Below 60rem, individual events preserve the original event-first layout; the existing venue link leads to the venue list. No new runtime filtering, routing or history behavior was introduced.

The application renderer, registered profile partials and route fixtures own this composition. The common profile wrapper, title and photo are shared; unique Sunshine prose stays in authored HTML. The previous standalone width wrapper and photo-cropping rule were removed. Tide, map sources and event fixtures are unchanged. The previously authorized shared `tools/check.py` count check now derives expected venue counts from route/event fixtures instead of a Sunshine/Midnight special case; independent application tests verify exact event membership and selection.

## Verification

`npm run build` and `npm run check` pass: 803 application documents across the default and ten theme/mode combinations; 1,107 repository HTML documents; all 139 tests (55 application, 72 shared contracts, seven HTTP and five map tests).

- Baseline comparison against 2.4.3: 58 documents changed, comprising the five remaining venue pages and 53 remaining event pages. The other 15 documents are byte-identical, including Sunshine/Midnight, the directory, global browsing/search, Saved, Help and submission. All 54 complete event-detail fragments are byte-identical. Tracked Tide/site hashes match; the scoped count update is the only shared-tooling change.
- Chromium on Windows: checked all 60 venue/event routes at 1440×1000 for venue scope, counts, selected event, loaded images and horizontal overflow. All pass.
- Checked all six venue profiles and one event per venue in all five themes and both modes: 120 browser cases. Scope/counts, image loading and horizontal bounds pass. This is layout/DOM verification, not a fresh contrast audit.
- At 1920×1080, all six venues and six representative events match the homepage’s centered 1472px header and retain 24px below the list pane. At 1200×800 and 960×800, all six venue summaries remain 56px high and list panes end 24px above the viewport bottom, including the longest venue names.
- The homepage, six venue pages and six representative event pages have no horizontal overflow at 320×568, 390×844 and 768×900. Desktop and mobile screenshots were visually inspected.
- Followed Barelas Print Studio → Ink After Dark → Venue details. The event retains its ten-event list and selection. Submitting the native search form keeps the event path and venue parameter; Reset removes the query and retains the selected event. On mobile, the event’s Barelas link returns to its ten-event venue page.
- At 320×568, the venue filter drawer body scrolls, its footer remains at the viewport bottom, and Escape closes it and returns focus to Filters.
- Application CSS is 21,603 bytes raw / 3,965 bytes gzip, within the unchanged 22,000 / 5,000 budgets. Existing CSS declaration-parity and map boundary checks pass.

Ignored evidence is in `build/qa/venue-context-rollout/`: baseline and parity JSON, all-route and theme records, responsive measurements, native-interaction results, screenshots and the full check log. These are evidence files, not alternate application sources.

## Limits

All 54 events remain authored samples. Sunshine’s existing venue facts were preserved, not re-researched; the other profiles contain only their existing name/type/photo content. Native search/date/category inputs remain UI specimens: query strings do not perform live filtering. Existing authored category/empty result documents remain available. Firefox, Safari, physical devices and screen readers were not tested.

Review [Sister](http://127.0.0.1:4187/events/app/sister.html) and select [Desert Frequencies](http://127.0.0.1:4187/events/app/desert-frequencies.html) to see the same nine-event venue context on both pages.
