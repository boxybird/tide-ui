# Venue directory · Lineup 2.3.0

The reviewed venue concept is now a native Lineup composition. Tide UI remains 1.12.0 with no source, token, recipe, registry, theme or distribution change.

## Preserved foundation · 2026-10-29

The user approved the current photo-free list, compact heading/search and list/map composition as the foundation for continued iteration. Git tag `lineup-v2.3.0` preserves this Lineup 2.3.0 checkpoint. The individual venue pages remain available for further refinement, and the tall-tablet map clipping finding in [the audit](AUDIT.md) remains open. The map is still illustrative and live matching/provider behavior remains consumer-owned. This checkpoint does not claim those future refinements are complete.

Earlier review notes below describe their measurement-time state; this checkpoint supersedes their pending-review and uncommitted status.

## Existing kit and application ownership

| Surface | Existing Tide recipe | Lineup composition |
| --- | --- | --- |
| Venues heading | Results utility, 20px/28px/580 | Native h1, directory region and adjacent city label |
| Venue entries | Event list/card category, title, support, metadata, accent and independent-action slots; Link | Venue type/name/city, fixture-derived event count and native venue/map destinations; no list photos |
| Map point | 44px Photo control, Icon, photo-accent token | Standard filled Phosphor Square glyph, label placement, illustration-relative positions |
| Map information | Panel/title, Caption, Button, Link | Native popover IDs, external width/placement and close-control wrapper |
| Mobile menu | Existing shared header and Panel | Unchanged menu composition |
| Venue documents | Content page, Results utility, Event list/card | Venue-specific fixture selection and native routes |

No private component type, color, border, background, internal padding/gap or focus override is added. The photo-free venue rows consume the unchanged Event card recipe: 24px padding, 12px uppercase category, 24px/32px title, 14px supporting text and metadata, texture and inter-card separators. The existing accent metadata slot displays the count, not a fabricated price or date. The existing independent-control layer (`tide-event-card__save`) keeps the plain Show on map anchor above the card's covering venue link; there is no save behavior or save claim. Map controls retain Tide's photo-control backing and 44px targets. The map callout and mobile Menu compute identically for Panel surface, border, radius, padding (24px), gap (12px) and body type. Ordinary underlined links retain canonical 14px regular type and have no added arrows.

`src/styles/venue.css` owns external grid placement, sizes, scrolling, profile-image crops, marker positions and responsive availability. The other four registered style modules, shared header and original event/filter templates stay unchanged. From 75rem the list track uses the same 35% calculation after two pane gaps as Find Events' middle track; its native thin scrollbar and canonical card insets leave the same usable card width. A directory-only viewport wrapper uses native CSS Grid for the natural header and bounded main, with the existing footer below the viewport as on Find Events. It does not measure header height. The directory reuses the same content-width/inset calculation and native root scrollbar gutter as Find Events; both panes retain at least 24px bottom clearance. Short-height windows use normal document scrolling with a usable directory minimum.

## Native interaction and integration boundary

- Desktop (60rem and above): venue list and map remain beside each other. The illustration is centered and fitted inside a non-scrolling frame, with no X/Y map scrollbars. Desktop uses a centered cover fit; the single-column view fits the complete illustration inside its available frame so markers remain reachable. There are no inactive zoom or pan controls.
- Below 60rem: List/Map are native fragment links. Each row's Map link targets its exact `map-{venue-id}` point, exposes the map and lets the browser scroll/focus that point. Marker buttons open one native auto popover per venue. Escape, light dismissal and focus return belong to the browser. Focus within the map keeps it available when an open desktop map is resized to phone.
- Popovers consume the unchanged Panel. CSS anchor positioning places them near points in the current Chromium preview, clamped to the viewport. Browsers without anchor positioning keep the native centered-popover fallback. Cross-browser behavior has not been verified.
- The full venue row and View events are real document/fragment links. The five new venue pages list the matching authored event records, sorted soonest first; individual links retain the existing event URLs. Sunshine Theater keeps its original information page, fact attribution, `#results` and `#venue-information`.
- The left-column Search venues form consumes the existing Tide Field recipe and uses a native GET to `venues.html` with `q`, matching the event search integration pattern. The static preview does not evaluate arbitrary query strings, so all six entries remain on a text query; a consumer supplies actual matching. The kit does not import React state, provider map pan/zoom, dialogs or routing. Consumers may integrate real matching, a map provider, geographic data and enhanced navigation using [the existing integration boundary](CONSUMER-INTEGRATION.md).

There is no new required Tide component or kit extension. A future reusable media-card or provider-neutral place-marker API would require its own separately authorized Tide task; this composition does not advertise either API.

## Photo-free list refinement · 2026-10-29

The user replaced the earlier photo-row direction with the existing home-page listing treatment. Directory entries now use venue type as the category, the venue name as a level-two title, the authored Albuquerque scope as supporting text, and the derived listed-event count beside Show on map as metadata. No event date or admission value is inferred for a venue. Profile photos and individual venue documents are unchanged; the map image, points and popover templates are unchanged. The map's available width follows the wider list track.

Chromium verification compares all six card roles against Find Events in all ten theme/mode pairs at phone and desktop sizes, with no computed-style differences. At 1488px the desktop list and event feed widths differ by less than 0.02px of browser track rounding. Seven responsive cases from 320 to 1920px retain all six rows and have no horizontal document overflow or list photos. Native keyboard card navigation, the separate map fragment, and marker Escape/focus return pass. Evidence: ignored `build/qa/lineup-venues/list-refactor/`; current desktop image below. Root build/check passes all 130 tests. The user accepted this list treatment before the foundation checkpoint.

## Data, assets and routes

### Compact directory header · 2026-10-29

The accepted Venues / Albuquerque utility heading is unchanged. Its only supporting UI is the native labelled Search venues field and, below 60rem, the existing List/Map controls. The filler tagline and separate six-venue count are removed. The private intro wrapper uses `space-4` (16px) block spacing: the divider-to-label distance matches Search events on the home page, and the search area has 16px clearance before the list surface. Card padding remains unchanged. On phone the view controls have their normal Stack gap and 16px clearance before the content; switching views no longer changes the header height.

At 1488x1058 the intro shrinks from 228.67px to 168.67px, while its title coordinates and list width remain unchanged. Five responsive cases (320, 390, 768, 1024, 1488px) retain all six rows without horizontal document overflow; all ten desktop theme/mode pairs have the same 16px gaps. Phone List/Map switching keeps the search available and the header at 228.67px. Root build/check passes all 130 tests. The approved row template, map templates/assets and all individual venue documents remain unchanged. Evidence: ignored `build/qa/lineup-venues/compact-intro/`. Tide remains read-only; this treatment is included in the accepted foundation.

`data/venues.json` owns six stable IDs/names, category descriptions and concept-photo metadata. Counts are derived from the unchanged 54 event fixtures at build time. It contains no raw HTML or newly claimed venue facts. Sunshine Theater remains the only separately attributed visitor-information page; the other venue documents make no address, facilities, accessibility or operational claims.

`venue-directory*.html`, `venue-map-point.html` and `venue-icon-square.html` are registered partials. `src/pages/venues.html` remains the registered content slot for directory and generic venue documents. The 65 workspace routes are unchanged; eight content routes bring the total to 73 per mode and 803 rendered application documents. Exact original event/venue IDs and all previous native paths survive.

`src/runtime/assets/venues/` contains seven generated illustrations, not documentary venue photography or geographic survey data. The map is an illustration with approximate points. `data/venue-images.json` records generation image IDs, source/served hashes, served dimensions and explicit lossy WebP encoding. All images remain below 200,000 bytes; no existing lossless asset is replaced. The standard filled Square glyph comes from Phosphor Icons 2.1.10; its MIT license is retained beside these assets.

The application CSS build removes ordinary comments and separator whitespace outside protected strings/URLs. Tests compare every canonical CSS selector/declaration before and after compaction and protect quoted whitespace, escaped newlines, URLs and license comments. This keeps the existing shared performance budgets unchanged without changing shared build tools or Tide.

## Verification · Chromium on Windows

- Root build/check: 803 app documents; 72 Tide, 51 application and 7 HTTP tests. HTTP tests require loopback permission; the restricted run failed to connect, then the approved loopback-enabled run passed.
- 30 theme/state cases: all five themes in light/dark, phone list, phone map/callout and desktop/callout. One visible h1, zero scripts, no horizontal document overflow and bounded callouts.
- 16 responsive cases span 320x500 through 1920x1080 and both native views below 60rem; long Barelas name included. Short-height pages intentionally scroll naturally.
- All five new venue documents expose correct event counts (9/13/10/8/8), no scripts and no phone overflow. Native directory → Sister → Desert Frequencies → browser Back returns to the nine-event venue document. Phone fragment focus, marker Escape/focus return and mobile Menu Panel parity are recorded.
- Source hashes protect all 133 Tide/reference-site/shared-tool files; comparison of previous rendered routes confirms the 67 non-directory documents are byte-identical. Browser console errors/warnings are checked separately.

Detailed measurements and current screenshots are ignored under `build/qa/lineup-venues/`. The retained desktop evidence is [the reviewed native layout](verification/venue-directory-desktop.jpg). Physical devices, Firefox/Safari, screen readers, text zoom, and changed system forced-colors/reduced-motion settings remain untested. Generated illustration coordinates are not a real map-provider contract.

## Refinement after user review · 2026-10-28

The first native translation was rejected for mismatched application width/header insets, omitted search UI and two-axis map scrolling. Its earlier visual acceptance is superseded. These three issues are now corrected, with broader user review still pending and no commit/push.

- Seven direct Find Events ↔ Venues comparisons at 390, 768, 1024, 1200, 1488, 1920 and 2560 CSS pixels have exactly zero difference in header left/width, brand left and main left/width. The viewport wrapper keeps the native footer outside the initial frame; no duplicate header inset or independent 92rem wrapper remains.
- Search venues is restored in the left intro, before the scrollable rows, with a visible native label, canonical 48px control and `q` GET contract. It is available in both native phone views. Enter submits the expected query; fixture matching remains consumer-owned, as with Find Events.
- Container queries separate close map labels on smaller illustrations without moving the points. Nineteen responsive list/map states have no document horizontal overflow, zero horizontal/vertical map scrollbar dimensions, no clipped 44px marker controls and at least 24px bottom clearance. Thirty fresh theme/state cases cover the same properties across all ten theme/mode combinations. A phone marker popover returns focus to its visible native control on Escape.
- The illustration remains a concept image with approximate positions. A live map/provider is a separate integration choice, not a workaround for the corrected frame geometry.

Current measurements: ignored `build/qa/lineup-venues/refinement-{widths,responsive,themes,search,anchor}.json`. Current screenshots use the same `refinement-` prefix; the retained desktop screenshot is refreshed. This is a scoped refinement, not a claim of final user approval for the complete venue experience.
