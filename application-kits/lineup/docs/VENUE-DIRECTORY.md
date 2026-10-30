# Venue directory · Lineup 2.3.2

Lineup owns this composition and its native selection behavior. Tide UI remains 1.12.0 with no source, token, recipe, registry, palette or distribution change. The approved 2.3.0 foundation remains preserved at `lineup-v2.3.0`; this iteration changes which action happens first.

The user-approved selection refactor is preserved at `lineup-v2.3.1` before real-map integration work. Its map image and CSS percentage positions are illustrative, not verified geographic coordinates.

## Audit corrections · 2.3.2

The illustration still fits completely in its frame. The frame reserves at least 48rem of document height; shorter viewports scroll the document rather than compressing markers. Below a 36rem map width, three illustrative marker positions and the label placements separate the 44px targets. Overview labels wrap where needed; a compact selected marker says Selected and its caption supplies the full venue name. These are illustrative placement changes, not geographic corrections.

Below 60rem, exactly one authored List/Map navigation is exposed, with a check icon and `aria-current="location"` on the current view. The fragment selects both the panel and navigation; stale focus cannot keep Map open after Back returns to List. Native row/marker fragments and detail destinations are unchanged. The private map-label host is now named `tide-venue__label`. See [audit correction verification](AUDIT-CORRECTIONS-2026-10-29.md).

## Interaction contract

- A venue card's covering link targets `#map-{venue-id}` in the same document. It selects the corresponding point instead of opening the venue page.
- The row's separate View venue details link opens `{venue-id}.html` directly. It remains available without using the map.
- Each 44px map control is a native link to `#venue-{venue-id}`. The browser reveals and focuses the corresponding row, scrolling the bounded list when necessary.
- Both targets identify the same venue. The row uses an existing neutral Selected badge; the map label uses the Photo control's own photographic text role for Selected, including in light themes. Other labels temporarily hide while all six marker controls remain available; the selected label is positioned away from neighboring glyphs. Compact illustrations use Selected text at the marker and identify the venue in the caption, keeping neighboring glyphs clear. No selection color, private card outline or new Tide state is introduced.
- A selected map caption provides a direct venue-details link and Back to list, which targets the same row. The overview List/Map links remain available below 60rem; they show the overview without a selected venue. Map selection exposes the phone map, and a row target exposes the list.
- This selection/caption treatment replaces the former marker-information popovers. There is no map dialog, focus trap or hover-only action. Header Menu and filter popovers remain unchanged. Sunshine Theater's attributed visitor information and schedule remain on its unchanged venue document.

Fragments preserve native links, modified clicks, direct visits and browser history. Focusable target IDs stay stable. The directory reserves most of the root scrollport for its bounded panes, leaving one target-sized region for native footer focus; selecting an internal point/row does not shift the application frame. The list uses native smooth scrolling only when reduced motion is not requested.

The selected badge's private wrapper uses progressive `scroll-initial-target: nearest` with external scroll margin. Supporting browsers can reveal the selected row when the document is first rendered or restored. The current Chromium phone/desktop checks retain the entered search value and selected URL target, and reveal the selected row again after a details-page visit and Back. Exact arbitrary pixel restoration across engines is a consumer responsibility. Unsupported engines retain the native links and visible selection. See the [CSS Scroll Snap specification](https://drafts.csswg.org/css-scroll-snap-2/#scroll-initial-target) and [MDN availability notes](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-initial-target).

## Existing Tide components

| Surface | Existing recipe | Lineup responsibility |
| --- | --- | --- |
| Venues / Albuquerque | Results utility, 20px/28px | Heading semantics and directory placement |
| Search venues | Field, visible label, 48px control | Native GET/q contract, external 16px clearance |
| Venue rows | Event list/card category, title, support, metadata, accent and independent-action slots | Venue type/name/city, fixture-derived count, selection target and document link |
| Selection | Badge | Target-dependent availability in private wrappers |
| Map points | Photo control, Icon, photo-accent token | Native fragment destination, position, stacking and name label |
| Selected map actions | Link, Row | Direct details and return-to-row destinations |

Card padding, texture, typography, colors, separators and focus/hover/active states remain canonical. The independent-control layer (`tide-event-card__save`) keeps the row's details link above its covering map-selection link; it implements no saving. No public component is privately restyled or extended.

## Composition and map boundary

The directory retains Find Events' frame/header insets, the 35% desktop list-track calculation, native thin scrollbar, compact heading/search and at least 24px pane-bottom clearance. Existing CSS Grid supplies the natural header and bounded main; short-height windows use normal document scrolling around the minimum frame. The five registered application stylesheet modules remain the only style owners.

The map illustration is fitted completely inside its non-scrolling frame at every width. This prevents the formerly clipped tall-tablet marker and keeps native targets reachable. The image, approximate point coordinates and square Phosphor glyph are unchanged. This is not a geographic camera: provider panning, zoom, real coordinates, live matching and fetched content remain [consumer integrations](CONSUMER-INTEGRATION.md). No provider, browser JavaScript, HTMX or independent prototype runtime is imported.

## Data, routes and sources

Six stable venue IDs/names, kinds and concept-photo metadata live in `data/venues.json`; counts derive from the unchanged 54 authored events. The 73 native routes per mode render 803 application documents. All original paths survive. Five generic venue documents retain their photos and matching event lists; Sunshine Theater retains its authored facts, attribution, `#results` and `#venue-information`. No new venue facts are asserted.

Registered partials own the directory, rows, map points, selected caption links and generic profiles. The renderer escapes text and rejects invalid includes and image paths. Concept-image provenance, source/served hashes and explicit lossy WebP settings remain in `data/venue-images.json`; all seven served assets stay below 200KB. The Phosphor Square license remains beside the assets. Application CSS distribution compaction preserves selectors/declarations and the existing performance budgets; shared build tools and Tide are unchanged.

## Verification and limits · Chromium on Windows

- All six map selections at seven viewport sizes: 42 cases from 320x700 through 1920x1080, including 1024x1058. Exactly one selected venue/label, no clipped marker or selected label, no horizontal document overflow and zero scripts.
- All ten theme/mode combinations at phone and desktop: 20 selected-state cases without clipping, overflow or scripts.
- Native keyboard card-to-map and marker-to-row selection, offscreen-row reveal, direct details links and phone/desktop Back journeys. Entered search text and selected-row restoration are checked; source/native reduced-motion behavior is retained.
- Original non-directory documents and 133 Tide/reference-site/shared-tool source fingerprints remain unchanged. Updated source contracts cover bidirectional destinations, focusable targets and existing Badge/Photo-control adoption. Root build/check passes all 130 tests.

Current screenshot: [selected venue on desktop](verification/venue-selection-desktop.jpg). Detailed measurements/screenshots are ignored under `build/qa/lineup-venues/map-selection/`. Firefox/Safari, physical devices, screen readers, text zoom and changed system motion/forced-color settings remain unverified. No dynamic screen-reader selection-announcement or cross-browser restoration guarantee is claimed. The 2.3.0 checkpoint retains the earlier photo/list/header studies and verification history.
