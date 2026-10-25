# Margin Reveal · verification · 2026-10-23

Tested live at local port4187 in the ChatGPT in-app Chromium browser. Firefox/Safari were not runtime tested in this iteration. This adds standard logical size/margin and grid composition; the existing component styles and fallbacks remain inherited. Reduced motion and instant initial/restored state were source checked; OS motion settings were not changed.

## Geometry

Measured open and closed at1200×600,1280×800,1366×768,1440×900,1600×900,1920×1080 and2560×1440: fourteen endpoint states. The individual event's x-coordinate, width and height remained identical across each toggle. The browsing/list right edge also remained fixed. Open filters' outer left edge matched the wordmark's left edge at every width. No horizontal document overflow occurred.

| Viewport width | Closed list | Open filters | Open list | Event, unchanged |
| --- | --- | --- | --- | --- |
| 1200 | 548px | 256px | 268px | 548px |
| 1280 | 588px | 256px | 308px | 588px |
| 1366 | 596px | 272px | 335px | 596px |
| 1440 | 596px | 272px | 372px | 596px |
| 1600 | 596px | 272px | 436px | 596px |
| 1920 | 596px | 272px | 596px | 596px |
| 2560 | 596px | 272px | 596px | 596px |

Numbers are rounded; native scrollbar geometry and rendering scale produce small fractional values in the evidence. At1440px, the old equal split yielded about286px for the list; this reveal gives it about372px. At1920px and above it retains its original596px. Extra-wide viewports leave breathing room between the bounded filters and list instead of stretching either into an oversized control or card.

Four DOM samples during an actual native pointer reveal at1440px confirmed the event stayed at x724.333 / width596.010 while the browser wrapper grew left. Its right edge stayed at700.333. Escape restored the closed composition, returned focus to the launcher, and left collapsed filters inert. There is one original query field, not a duplicate.

At all fourteen endpoints, the list ended48px above the viewport bottom and Apply matched that bottom. After scrolling the right document900px and the list900px independently, closing filters retained both reading offsets, the header at y0 and the list at y117 with its bottom at852 in the900px window.

## Preservation and responsiveness

Compared the closed view against the preserved original Contained at1440×900 and1920×1080. Header, list, event, intro, photo and title rectangles matched within0.1px. Compared the same rectangles against the previous original-width version on390×844 (list and standalone event),1024×768 and1199×800; all matched within0.1px. The private geometry is inactive below75rem.

The live review was resized to1920×1080. Once its inherited viewport-resize transitions settled, the filters matched the48px header inset, both list and event were596px wide, and the event retained its centered original position. These measurements concern settled viewport sizes; resizing a window itself still triggers the inherited sizing transitions.

## Function

- Query “Ink After Dark”, From/Through October24 and Workshops submitted through the existing pinned Apply and returned one result with the correct GET URL and Filters · 2 badge.
- An unmatched query submitted with Enter returned zero. Clear search and filters restored all48 events.
- Selecting Desert Frequencies retained the filter-open preference and showed the correct event.
- Review compact/full search choices and the no-image/rough-image control continued to work. No console errors were recorded for this prototype tab.
- The generated adapter passed Node syntax checking. It differs from the previous helper only in its session namespace; other scripts are reused directly.

## Source checks and release

`source-check.json` verifies54 HTML documents,4393 local references,53 unchanged component-document comparisons, IDs/labels, BEM ownership, token references, reduced-motion/instant handling and all preceding hash locks. The maintained app980 files, kit180 files, Reading Widths188 files and Width & Search182 files remain byte-identical, along with the rest of the preservation chain. No kit component, primitive or theme changed.

Raw observations are in `browser-evidence.json`; assertions are in `browser-check.json`. Screenshots show open/closed1440px and1920px views, a short desktop and an extra-wide desktop. This sibling receives its own immutable source release; previous archives are never replaced.
