# Native responsive filter drawer · Lineup 2.1.9

**Accepted 2.4.6 homepage behavior:** on Find Events (`index` and `search`), search and the Filters launcher appear above the list, and the panel remains a drawer even on desktop. The original form is outside the panel; date/category controls, submit and Reset retain native form association. Other routes keep the behavior below. See [the two-column review](HOME-SPLIT-REVIEW.md).

The current [filter-panel spacing contract](FILTER-PANEL-SPACING.md) adds a private content wrapper with `space-6` top clearance below 75rem and adopts Tide's compact Category grouping. The public rail body/footer, native lifecycle and desktop search placement retain their existing contracts. Earlier behavior verification below remains historical evidence.

The same `filter-rail.html` aside and original form/control set serve both layouts. `filter-trigger.html` is rendered by the shared header only on routes with a filter panel. The kit owns Filter panel internals, Button, Icon, fields and native Expandable; app-owned `filters.css` owns responsive placement and motion. `consumer-manifest.json` registers the templates and stylesheet. No browser JavaScript is shipped or needed.

## Behavior

- Below 75rem, Filters opens `#lineup-filters` through `popovertarget`. Its `popover="auto"` state supplies native toggling, explicit Close, Escape and outside-click dismissal. The close button receives native autofocus; dismissal returns focus to the launcher when appropriate.
- The drawer occupies the left edge, at most 24rem wide with at least a 2rem outside-dismissal area. Its `100dvh` grid keeps the header and footer visible while the body scrolls. Private child wrappers reserve the drawer's start gutter and bottom safe area around the status/actions. The canonical rail footer remains a direct child of its panel; its own padding, grid gap, status flex layout and text flow stay in Tide. CSS prevents background page scrolling while the narrow drawer is open.
- Entry and exit translate horizontally over 240ms. `@starting-style`, discrete `display` and `overlay` transitions preserve the visible exit. With reduced motion, opening and closing are immediate.
- This is a non-modal popover: the page is not inert and there is no focus trap or modal claim. Close, Escape and outside dismissal preserve entered values. Native search inputs can consume the first Escape to clear their text. Reset restores authored defaults; result counts remain authored samples.
- At 75rem and above the original 20/35/45 desktop composition remains. The launcher and drawer header are hidden; the panel is always displayed in its original column. If resized while open, CSS anchors fit the top-layer panel to `.tide-app__filter-clip`, with the existing grid geometry as a fallback. Dismissal leaves the desktop panel visible. Returning to a narrow width preserves the browser's open/closed state and the original input values.
- Saved/help/submission have no filter launcher or panel. Event detail pages retain their full-screen phone reading layout; filters remain available in the split layout from 60rem upwards.

## Current verification · Lineup 2.1.5

The [compact-header implementation](COMPACT-HEADERS.md) aligns the desktop utility label with the count header; the original drawer title, form, footer and native lifecycle remain.

## Product-copy verification · Lineup 2.1.4

The drawer's HTML/CSS mechanism is unchanged. The [handoff verification](HANDOFF.md) covers the simplified controls, native dismissal/reset, responsive placement and current testing limits. Tutorial result links, example labels and duplicate sample counts have been removed from the panel. Integration explanations remain in kit documentation.

## Alignment verification · Lineup 2.1.3

[Strict Tide alignment](TIDE-ALIGNMENT.md) covers canonical field/fieldset markup, unmodified component interiors, outward focus rings with private external clearance, all themes, bounded panes, native controls and drawer journeys. The [footer/tablet record](FILTER-FOOTER-TABLET.md) and earlier evidence below remain historical.

## Verification · 2026-10-26

Microsoft Edge 156.0.4314.42 (Chromium, Windows), with page JavaScript disabled:

- At 320, 390, 768, 1024 and 1199 CSS pixels: native pointer and keyboard opening, Close, Escape, outside-click dismissal, focus return, native Reset, a bounded scrolling body and visible footer passed. No document horizontal overflow or browser scripts were present.
- At 1200, 1440 and 1920 pixels: filter, input, footer, results and detail geometry matched the pre-change baseline within 0.1px. The 1440 × 1000 desktop screenshot had zero changed pixels.
- Widening an open 390px drawer through all three desktop widths fit the original reserved column within 0.1px and retained entered text. Dismissal kept the desktop column visible; narrowing a closed panel hid it until invoked again.
- All ten theme/mode combinations opened and closed at 390px. Reduced motion removed transitions. Venue scope, the authored empty route and the absence of dangling launchers on saved/help/submission passed.
- Measured entry and exit transforms confirmed the 240ms left slide and retained top-layer exit. Keyboard checkbox changes scrolled the body while preserving the footer; a 500px-tall viewport kept its footer in view. The open desktop resize state stayed aligned while scrolling the outer page.

Generated output, the detailed browser report and routine screenshots stay in ignored `build/qa/`; they are not canonical sources. Firefox, Safari, physical touch devices/software keyboards, screen readers and forced-colors interaction remain unverified. Native popovers and discrete/starting-style transitions are browser features; CSS anchor positioning improves the already-open desktop resize state, with a shared-geometry fallback for older engines.

## Lineup 2.1.0

The page heading now belongs to the ordinary browse layout outside the popover; the drawer contains controls and its own Search & filters title. The desktop anchor follows the filter clip below the heading when an open drawer is widened. Venue Reset navigates to that venue’s unfiltered sample document; the global Reset remains native form reset. Current [heading/venue verification](HEADINGS-VENUE-SCOPE.md) records resize, focus and scoped recovery evidence.
