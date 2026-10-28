# Compact utility headers · Lineup 2.2.3

The selected visual target is [option three](design/compact-headers-target.png). The implementation starts from the clean 2.1.4 commit `8239327`. The user reviewed and accepted the Tide 1.11.0 recipe and Lineup 2.1.5 integration on 2026-10-27, then requested preservation on main.

## Composition

Desktop uses two aligned compact utility rows: Search & Filters over the left controls, and the authored count with Soonest first over the event feed. The Coming up intro, general tagline and The lineup kicker are removed. The right detail document and original 20/35/45 composition remain. The Search Events label and first month title align below the utility headers.

Lineup 2.2.3 uses an 8px external utility-summary gap (`--tide-lineup-summary-gap`, `space-2`) at every width, extending the accepted 2.2.2 desktop treatment to mobile and tablet. Tide's unchanged month header contributes another 8px top padding, placing the first month title 16px below the divider on unscoped browse pages. Desktop first labels align; venue pages retain their additional information-jump allowance. Native fragment reservation uses the same private gap input. Search controls, shared header/calendar recipes and Saved retain their existing placement; the filter drawer keeps its separate 24px heading-to-search clearance. The right document stays fixed in split/desktop composition; phone venue information follows the shorter feed in ordinary flow.

Both rows consume the canonical `tide-results--utility` variant. The application does not override their type, colors, padding or divider. Private Grid rows and external gaps compose them. The static left utility label is a paragraph; the result count is the page h1, or a secondary h2 on native event documents whose event title remains h1. An inline screen-reader-only prefix supplies Albuquerque or venue context without another visible heading. Results keeps its original focusable region, labels and IDs; controls remain in the original aside.

Below 75rem the desktop-only utility label is hidden and the original native drawer supplies its own title. The count stays visible outside the closed drawer. Split tablet retains its bounded list alongside the natural detail document. Phone uses the count above the feed. Saved keeps its own intro and default Results recipe; Help and submission retain their layouts. Venue pages keep useful information and a visible About this venue jump below their count.

The permanent summary remains outside the isolated complete feed. Native month targets reserve the utility row and external gap; venue pages also reserve the information jump. CSS anchors continue to fit an open drawer to the desktop column when the viewport widens. Shared CSS fallback geometry reserves the same compact row and gap, plus the venue information allowance where present. No browser JavaScript, copied form, live matching or service behavior is added.

## Ownership

The user separately authorized the small Tide extension required for the selected 20px header treatment. Tide owns the additive Results variant, registration, fixtures, tests and contract. Default Results, filter-panel internals, palettes, primitive tokens, fonts and image assets remain unchanged. Lineup owns template composition, region/heading semantics, viewport geometry and count data. See the [kit contract](../../../packages/tide/docs/RESULTS-UTILITY.md).

The image mock is a header-layout target. The implementation preserves canonical 44px choice targets, original card/calendar typography and the supplied photographic asset rather than copying incidental generative changes to those existing components.

## Historical 2.1.5 verification

In-app Chromium on Windows, using viewport emulation:

- Index, venue and Saved at 320, 390, 768, 959, 960, 1024, 1199, 1200, 1440 and 1920 by 900. Seven other route families at 390, 1024 and 1440. Every case has one visible h1, no horizontal document overflow and zero scripts; utility counts compute to 20px.
- All ten theme/mode combinations at 390, 1024 and 1440. Nine short-window cases cover index/venue/Saved at 1024, 1200 and 1440 by 500. Bounded pane bottoms retain at least 24px clearance.
- At desktop widths the Search events body and month-feed top align, including the venue's information-jump allowance. Default Saved typography/composition remains separate.

Native interaction, visual-comparison and final build/check results are recorded in the [design QA report](../design-qa.md). Routine captures and expanded measurements live under ignored `build/qa/lineup-compact-headers/`. Firefox/Safari, physical devices, screen readers and changed system motion preferences remain unverified.
