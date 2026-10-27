# App loading and performance

Kit 1.5.3 / app 2.0.3 adds lossless shared kit assets, validators for all local file responses, negotiated text compression and regression budgets. See the current [loading contracts](../../../docs/LOADING-PERFORMANCE.md). Layout, markup presentation and app photo derivatives are unchanged.

## Local font loading · kit 1.5.2 / app 2.0.2

Manrope is a local 24,836-byte variable WOFF2 at `packages/tide/assets/fonts/manrope-latin-wght-normal.woff2`; no remote font service is used. Every app document now preloads the same URL used by the shared kit CSS, with `as="font"`, WOFF2 type and anonymous CORS mode. The reference site already preloaded this asset. This removes late font discovery through app stylesheet loading.

The local preview server previously sent `Cache-Control: no-cache` on every resource, which requires revalidation even for cached fonts. Fonts now use `public, max-age=86400` and a content ETag; a matching conditional request returns 304. HTML/CSS remain `no-cache` for source iteration. A replacement font should use a new filename to avoid the one-day freshness window.

The kit uses `font-display: block`: text waits invisibly for local Manrope during the browser's bounded block period (typically about three seconds). This avoids the immediate fallback flash. A font that exceeds that period can still fall back and later swap, so this is not an absolute no-swap guarantee for failed/very slow loads. Preload and caching remain. No document-hiding or JavaScript readiness gate is introduced.

Verification on 2026-10-26: build and contract checks pass, including preload coverage for every document. The font endpoint returns 200, 24,836 bytes and the one-day cache header; a matching ETag returns 304 while app CSS retains `no-cache`. Chromium resolved the shared local preload URL with zero scripts; three desktop refresh observations had identical filter/result heading geometry. These settled observations do not measure intermediate paint frames or prove the intermittent flash absent. Cold/throttled, Firefox and Safari checks remain deferred.

## Historical image cleanup · 1.1.8

App 2.0.0 removes every browser script and replaces dynamic behavior with native controls and authored states. The historical measurements below describe earlier iterations; the current contracts are [runtime boundary](RUNTIME.md) and [desktop layout](DESKTOP-LAYOUT.md).

The title transition experiment is disabled. This pass reduces image loading and isolates Back/filter behavior without changing native navigation, filter mount/close/resize timing or reading restoration. Tide remains 1.5.0.

## Asset and loading ownership

`data/events.json` references three WebP derivatives in `src/runtime/assets/images/`. `preview.js` uses `src/runtime/js/assets/organizer-upload.webp` for its existing rough-photo mode. All four derivatives use WebP quality 82/method 6, retaining 1024×1536 dimensions. They were encoded with Pillow as a one-time asset preparation step; normal builds still need no installed dependencies. Original PNG sources remain at their existing app/kit paths, and original URLs remain available. Only the WebP derivatives are requested by current app photo markup/hooks.

| Served app photo | PNG source bytes | WebP bytes | Reduction |
| --- | ---: | ---: | ---: |
| Comedy / The Late Set | 2,011,408 | 65,706 | 96.7% |
| Concert | 2,059,555 | 84,222 | 95.9% |
| Ink After Dark | 2,536,968 | 172,406 | 93.2% |
| Rough organizer upload | 2,114,033 | 61,978 | 97.1% |
| Total | 8,721,964 | 384,312 | 95.6% |

These are file-size measurements, not navigation timing or frame-rate benchmarks. The original Ink After Dark PNG remains kit-owned; the app derivative does not change kit specimens or their photos. The shared kit texture and the local preview server's cache policy are unchanged.

`tools/event_details.py` and `src/templates/event-detail.html` render real detail photos with `loading="eager" fetchpriority="high"`; index/search/saved previews use `loading="lazy" fetchpriority="auto"`. Intrinsic dimensions and existing alt text remain. Native lazy loading prevents a CSS-hidden preview photo from loading just because its HTML exists.

`event-search.js` still owns the first matching local-document preview. If the selected fixture no longer matches, it waits for `TideApp.media('split')` before fetching the first result. The same one-shot loader responds if a narrow window later widens; shrinking/widening again does not duplicate the fetch or control set. Imported photos are demoted to preview loading priority. Real event routes remain immediately readable, and empty/venue contexts keep their existing behavior. Narrow browsing does not set `previewLoading` while an invisible request is deferred.

## Back and filter-flash isolation

Before cleanup, Chromium visibly carried unrelated outgoing card titles over The Late Set and back onto the list. All 54 titles had transition identities. The removed `@view-transition` opt-in and root snapshot overrides could expose an unsettled destination; this was an inference about the reported flash, not a confirmed capture of the actual filter panel opening.

With transitions removed, the tested Back frames showed a mounted drawer/rail layout, one original control set, a closed dialog and no fallback form visible in the results. A fast desktop close → keyboard event activation → Back test returned a closed rail with zero width, zero opacity and hidden clipping. A filtered tablet close/Escape → event → Back test retained `q=comedy` and the correct preview without reopening the drawer. The exact original filter flash was not reproduced in this baseline. No additional filter lifecycle listeners, render-blocking scripts or startup hiding rules were added.

Existing desktop navigation may still wait for smooth scrolling before following an event URL, with its existing three-second safety ceiling. Existing history restoration may adjust the reading position after preview readiness. Those intentional behaviors are unchanged and should be distinguished from image transfer or a filter reopening. If the flash returns, record viewport, browser Back versus the authored return link, filter state and whether the page was still scrolling/closing.

## Verification · 2026-10-26

- Root build/check cover all 660 app documents, all ten theme/mode combinations, palette/ownership, templates, search and runtime contracts. A regression contract distinguishes preview versus real-detail loading priority across all 54 events and preserves dimensions. The rough-photo compatibility test retains message/mode behavior with the new derivative URL.
- Chromium on Windows at 671px: index preview computed lazy/auto with `naturalWidth: 0` while hidden; no named card transitions remained. The Late Set opened with the WebP and eager/high priority. Browser Back returned to the list without a visible fallback form or open dialog.
- Chromium at 671px on `search.html?q=comedy`: no preview request/loading state and no decoded hidden image; widening to 1024px loaded The Late Set as a lazy/auto preview with one detail and one form. Filter close/Escape, event activation and Back retained the query and closed drawer; no warning/error logs were observed in that journey.
- Chromium at 1280/1440px: desktop open/close, ordinary event navigation and Back, plus fast close/keyboard departure/Back. The returned rail was closed in the captured frame. These observations do not prove the reported intermittent flash cannot recur.
- Native Firefox/Safari, physical devices, screen readers, reduced-motion preference emulation, network/CPU throttling, a full performance trace and exhaustive history scenarios remain untested. The change establishes lower asset bytes and observed behavior, not a measured overall speed-up.

## Desktop startup grid fix · 1.1.9

The later report of a rightward snap had a reproducible CSS cause independent of title transitions and photo loading. Before `rail.js` mounts, the desktop workspace declared two columns but placed results in column 2 and detail/placeholder in column 3. The hidden rail did not occupy column 1, yet that empty track remained reserved and an implicit third track was created. The 90rem rule further widened the empty leading track. Mounting then replaced this with the accepted centered two-column subgrid.

In a local diagnostic copy of The Late Set with only `rail.js` omitted, Chromium at 1440px computed three tracks (`390px 319.573px 603.094px`): results began at x=446 and the detail at x=789.573. The normal mounted route put results at x=104.333 and detail at x=724.333. This reproduces the two layouts responsible for the snap; it is not a claim about how often a browser paints the intermediate frame.

`desktop.css` now scopes the unmounted fallback to workspaces with a direct filter-rail child, uses the same content inset and equal columns as the mounted body, and assigns results/detail to columns 1/2. The rule follows all wider-breakpoint overrides. Saved lacks that rail and retains its previous composition. No DOM, script order, mount/resize timing, scrollbar measurement, filter animation or sticky geometry changed.

Chromium on Windows compared the same diagnostic pre-mount document with the normal mounted event route after the fix:

| Viewport width | Startup list x | Mounted list x | Largest pane x/width difference |
| --- | ---: | ---: | ---: |
| 1200 | 32 | 32 | 0px |
| 1280 | 32 | 32 | 0px |
| 1440 | 104.333 | 104.333 | 0px |
| 1920 | 344.333 | 344.333 | 0px |
| 2240 | 504.333 | 504.333 | 0px |

The last column compares both x and width for both results and detail panes, using DOM rectangle measurements. At 1440px opening the rail, navigating between The Late Set and Desert Frequencies with open/closed filters, and browser Back retained detail x=724.333. All ten theme/mode event routes also measured list x=104.333 and detail x=724.333. Generated diagnostic files and screenshots remain ignored under `build/qa/layout/`; they are not additional maintained app routes. Root build/check and theme/browser limits above still apply.
