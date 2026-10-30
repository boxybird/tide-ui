# Lineup source of truth · 2.4.0

The current checkpoint is **2.4.6**, preserving the accepted 50/50 Find Events homepage, visible search and native Filters drawer as `lineup-v2.4.6` ([scope and verification](HOME-SPLIT-REVIEW.md)). Version 2.4.5 preserves the accepted Sunshine Theater photo hero and the shared 52rem preferred height for Sunshine and its six event pages as `lineup-v2.4.5`. See [changes and verification limits](CHANGELOG.md#245--2026-10-30). Version 2.4.4 applies [venue context](VENUE-CONTEXT.md) to all six venues and 54 events. The accepted Sunshine / Midnight pair is separately preserved in `lineup-v2.4.3` ([record](SUNSHINE-REVIEW.md)). Versions 2.4.1–2.4.2 preserve [compact map previews and marker highlighting](MOBILE-MAP-PREVIEW.md). All work continues on the same `main` branch; the original `lineup-v2.4.0` consolidation tag remains unchanged.

The user approved consolidation on October 29, 2026: one repository, one `main` branch, one current application and an incremental commit after each accepted change. The previous two-repository workflow caused visible regressions because the map preview used an older immutable application snapshot. This checkpoint removes that split.

## Current application

- Repository: `Burque Events Designs`.
- Canonical application: `application-kits/lineup/`.
- UI dependency: `packages/tide/`, Tide 1.12.0, unchanged.
- Preview: [venues](http://127.0.0.1:4187/events/app/venues.html) and [Find Events](http://127.0.0.1:4187/events/app/index.html).
- Commands from the repository root: `npm run build`, `npm run check`, `npm run dev`.
- Generated output: `build/events/`. Never edit it as source; never use a frozen snapshot to supply current routes.
- Current checkpoint: `lineup-v2.4.6`; consolidation baseline: `lineup-v2.4.0`. Subsequent accepted changes are committed directly on `main`; release tags are immutable.

The map is built from `src/map/` alongside the current templates, fixtures and styles. Its relative asset paths work on the default route and every generated theme route. There is no adapter server, HTML response rewriting, alternate map URL, copied Tide tree, `snapshot/` or `map-snapshot/` in the maintained application. The former port 4198 Consumer Lab is retired.

## Combined work

| Preserved work | Origin | Current owner |
| --- | --- | --- |
| Seven audit corrections | `3fd08d1`, Lineup 2.3.2 | Current templates, fixtures, styles and contracts |
| Matching mobile venue summary spacing | `1753b69` | `src/styles/venue.css` |
| Compact cards open venue/events; split cards select adjacent map | `4154f89` | Current row template and responsive CSS |
| Dark MapLibre/OpenFreeMap map, square markers and geographic camera | `98f4683`, Consumer Lab 0.4.2 | `src/map/venue-map.mjs`, styles, pinned vendor and map data |
| Fixed outer directory, list-owned footer, aligned map bottom and overlaid selection actions | Consumer Lab 0.4.1–0.4.2 | Current venue template and map stylesheet |

The current marker label classes and both responsive card links are used by the map. Native List/Map fragment state and browser Back remain authoritative; the old focus-based panel override is not restored. The footer stays within the venue-list scroller. Event and individual venue documents retain their natural scrolling. All 54 events and geographic venue positions remain authored demonstration data; consolidation does not turn them into verified live listings.

## Runtime and dependencies

Only `venues.html` loads `venue-map.mjs` and the pinned MapLibre 6.16.0 modules. This narrow exception supersedes the earlier all-application zero-browser-JavaScript rule. Tide, the reference site and every other application route remain script-free. No HTMX, search engine, new navigation router or service is introduced.

The local MapLibre distribution and licenses are preserved byte-for-byte, with hashes in `data/map-dependencies.json`. The approved dark style and coordinate fixture are unchanged. Public OpenFreeMap tiles and glyphs require network access. The illustrated map and native links remain the fallback when the map fails or scripts are unavailable; `?map=off` and `?map=fail` are diagnostic states. Camera/list restoration is scoped to the map module. Reduced-motion preferences are retained.

The native application CSS budget is 25,000 raw / 5,000 gzip bytes. The user explicitly approved the raw-only increase from 22,000 bytes for the two-column homepage in 2.4.6. Map-only CSS, application module and pinned dependency budgets are separately recorded; they are requested only on the directory. No dependency installation is required.

## Recovery and retired work

`archive/consumer-v0.4.2` preserves the old Consumer Lab Git commit in this repository, including its historical HTMX experiment, immutable snapshots, manifests, docs and retained evidence. It is archival history, not a branch or active source tree. Earlier Lineup tags remain untouched. No existing published history is rewritten.

`archive/lineup-venue-prototype-2026-10-29` preserves all 150 authored files from the earlier standalone React/raster-map study, including its source, lockfile, copied assets, design evidence and hosting fixtures. Regenerable `node_modules`, build output and runtime logs are omitted. That separate working folder is retired too; it is not an alternative implementation to continue editing.

The old consumer ZIP checkpoints are retained as recovery artifacts under `.git/retired-consumer-checkpoints/`. They are not executable source folders or an alternate preview. This is the complete inventory of retired consumer material; do not restore it into the current application while making incremental fixes.

## Verification

- Build/check gate: 1,107 generated HTML documents and 138 tests (72 Tide contracts, 54 application contracts, seven preview HTTP checks and five map integration checks). The map tests verify all 73 current routes, module MIME types, local references, dependency hashes, exact venue IDs, current card destinations and footer ownership. The Markdown checker now recognizes angle-bracket link destinations in the preserved upstream license without changing the license text.
- Parity: all 792 non-directory application documents remain byte-identical to the pre-consolidation build. All 122 sampled Tide/reference-site source files remain byte-identical. The native application stylesheet is unchanged at 21,996 bytes. MapLibre, the approved style and demonstration coordinates are preserved.
- Chromium desktop at 1280×720: the approved and consolidated list/map geometry is identical. Both pane bottoms are 696px, map right edge equals directory right edge, and root scroll height is 720px. All six card/map selections expose their correct labels and keep the document stationary.
- Chromium phone at 390×844: the map ends at 844px, root scroll height stays 844px, Sister opens its current nine-event document by keyboard, and native Back restores the directory/List state. List/Map current state remains truthful.
- Ten theme/mode pairs at both 1280×720 and 390×844 load the real map with aligned bottoms and no horizontal overflow. Eight responsive/short-window cases cover 320, 390, 543, 544, 959, 960, 1440 and landscape 844px widths; one primary card link is exposed at the correct breakpoint. Below 34rem the summary starts directly after the header, preserving the approved spacing fix. Short windows scroll internally.
- A forced map-provider failure restores all six native illustration markers and announces the fallback. No copied app or external checkout is needed by the active server.
- Retired source tags and all three original ZIP checkpoints were verified before moving the duplicate folders to the Recycle Bin. Ports 4198 and 4201 are inactive. Port 4187 serves the canonical build.

Current browser coverage is Chromium on Windows; Firefox, Safari, physical devices and screen readers remain unverified. The screenshots and detailed measurement records are under ignored `build/qa/consolidation/`. Verification establishes this checkpoint, not a guarantee against future regressions; each accepted change still needs its relevant checks and a new commit.
