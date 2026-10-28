# Header navigation · Lineup 2.2.1

Lineup composes Tide 1.12.0's Site header shell and reviewed navigation actions inside a private CSS Grid. The opt-in `extensions/navigation.css` remains loaded after the core stylesheet for navigation action states. Tide sources, recipes, tokens, registry and documentation site are unchanged.

Below 34rem, the [native Menu popover](MOBILE-NAVIGATION.md) replaces the inline presentation. Brand/Saved remain in row one and Menu/Filters occupy row two. Above that breakpoint, the existing inline header geometry is preserved. Shared link items are authored once, with one exposed Main navigation at a time; popup appearance comes from Tide's unchanged Panel extension.

## Composition

`header.html` owns the private `tide-app__header-layout` wrapper. Its flexible leading track leaves Burque at the start while Find Events, Venues and Add an Event sit beside the separate Saved utility on the right. The 24px external column gap separates primary navigation from Saved; the link list keeps Tide's 8px action gap. The original Filters control follows the utility on split tablet, and remains hidden with the permanent desktop filters. The [directory contract](VENUES-NAVIGATION.md) records native destinations and migration.

Below 60rem, the grid places Burque and Saved on row one. The primary presentation occupies the start of row two and Filters aligns to its far right. From 34rem the links remain inline and can wrap naturally; below 34rem the Menu trigger opens ordinary navigation links in a native popover. Header height grows in normal flow; no fixed phone height, layout script or positive tabindex is used. Routes without filters give the primary presentation the full second row. Native event documents retain their established header omission below 60rem.

The private wrapper owns its tracks, gap and placement. It does not alias or override the interior of Tide's centered header modifier; that modifier is no longer consumed. The shared shell retains its padding and border. Buttons retain canonical type, padding, colors, radius, target sizes, hover, held, current-page and focus appearance. Saved keeps the source Bookmark icon. Only the actual index, directory, submission or Saved destination receives `aria-current="page"`. A venue profile does not mark the directory as the current page.

## Historical 2.1.7 layout and verification

The following baseline predates the third primary item and new directory. Current responsive behavior retains the same wrapping/grid rules; the expanded menu is the starting point for a separate responsiveness review. The new directory and shared footer Help link are recorded in the current [directory contract](VENUES-NAVIGATION.md).

Desktop retains its 93px single row, and split tablet retains the existing 48px Filters allowance and 97px header. All main content and non-header templates are unchanged from `86636a9`; all four non-header application stylesheets and data remain unchanged. The two left panes, summary, feed, right document, footer, native scrollbar gutters and at least 24px bottom clearance retain their geometry from 60rem upwards. Narrow content moves only with the header's normal-flow height.

Links, browser Back, drawer opening/dismissal/focus return, native fields and Reset remain browser-owned. There is one original control set and zero browser JavaScript.

## Verification

Thirty before/after cases cover index, venue, Saved, Help, submission and an event at 390, 768, 1024, 1200 and 1440px. All measured pane rectangles from 960px upwards are identical. A further 120 cases cover index/venue/Saved across all ten theme/mode pairs at 320, 390, 768 and 1440px, with no control overlaps, horizontal overflow or scripts. Eight breakpoint-edge cases cover 479/480, 703/704, 959/960 and 1199/1200px.

Native Close and Escape return focus to Filters. An entered query survives an open-drawer resize from 390 to 1440px; the panel exactly fits its reserved desktop column. Reset clears the query. Native venue/Saved navigation and Back retain correct current-page states. Keyboard focus retains Tide's 2px outline and nominal 3px offset. Browser warnings/errors: none. Dependency fingerprints and all 737 generated route main sections retain parity. The [design QA](../design-qa.md) records the evidence.

Root build/check and all 121 tests pass, including strict component ownership and unchanged performance budgets. Coverage is in-app Chromium on Windows with viewport emulation. Firefox/Safari, physical devices, screen readers, actual text zoom and changed system motion/forced-color preferences remain unverified. The previous centered integration and Tide promotion are preserved in the 2.1.6 changelog and design-QA history.
