# Lineup application kit · 2.1.3

**Tide HTML/CSS alignment is complete.** Lineup 2.1.3 uses Tide's canonical component recipes without private typography, decoration or interior-spacing overrides. The search label, fieldsets, links, captions, hero, focus rings and current card/footer markup are aligned. See the [completion boundary and verification](docs/TIDE-ALIGNMENT.md). Personalization is a separate future task. Tide remains unchanged.

Lineup is layout family **option 1**, an independently versioned HTML/CSS application kit derived from **Tide UI 1.10.0**. Burque Events is its authored sample website. The application version is **2.1.3**; option 1 does not reset its release history. All 54 events are authored samples. The original 60 routes remain, plus the four global result specimens and three scoped venue empty views: 67 documents in the default app and each of ten theme/mode combinations.

The UI kit at `packages/tide/` is the source of truth for public components, type, spacing, colors and recipes. This directory owns application composition and sample content. Application work does not modify the UI kit. See the [ownership contract](docs/COMPONENT-OWNERSHIP.md), [audit](docs/AUDIT.md) and [consumer starting point](docs/STARTER.md).

Desktop keeps the centered 92rem maximum and 20/35/45 filters/list/detail proportions. CSS Grid/subgrid, native scrolling, sticky month headers and viewport units supply layout. The result summary sits outside the feed scroller, so no height observer is needed. The single page heading stays outside the filter panel at every width. Below 75rem, Filters opens the same control set in a native popover drawer that slides in from the left. Close, Escape and outside-click dismissal are browser-owned; reduced motion removes the slide. The body scrolls above a pinned footer. No browser scripts or duplicated form are required. See the [drawer contract and verification](docs/FILTER-DRAWER.md).

Native links, fragments, browser Back, input controls, reset, required/type validation and file selection remain. Free-text/date matching, live result counts, fetched previews, session state and photo/inspection message hooks are removed. Controls are explicitly labelled examples. Use the authored result-state links to review populated/category/empty layouts; URL query values are not evaluated. No backend or service is introduced.

The header and skip links use Tide's canonical recipes. Main links wrap at narrow widths; current-page styling follows the actual native destination. Saved, Help, Add an event and native event pages have descriptive titles without retired study names. See [navigation/title verification](docs/NAVIGATION-TITLES.md).

Venue result links, Reset and empty-state recovery stay at the venue; “All events across Albuquerque” is the explicit city-wide exit. See [heading/venue verification](docs/HEADINGS-VENUE-SCOPE.md).

Saved uses two populated desktop columns and reserves separate intro, canonical summary and scrolling-feed rows. Lineup adopts Tide's result, calendar and page-intro typography without private type aliases. See the [application changes](docs/CHANGELOG.md) and [verification](docs/SAVED-TYPOGRAPHY.md). Native month links align the selected heading at the feed top; desktop summary clearance comes from named type/spacing inputs. See the [desktop contract and browser coverage](docs/DESKTOP-LAYOUT.md).

Run `npm run build`, `npm run check`, `npm run dev` from the root. Open `/events/app/index.html`; `/events/index.html` links to all modes. Canonical sources moved from `examples/events/` to `application-kits/lineup/`; generated `build/events/` output and native preview URLs remain unchanged. Node/Python are development tools only. See [zero-browser-JavaScript policy](../../docs/NO-BROWSER-JAVASCRIPT.md).

Canonical sources are `src/templates/`, three unique fragments in `src/pages/`, the five `src/styles/` modules and structured `data/` fixtures. `data/events.json` owns events, `data/pages.json` owns thirteen non-event routes and typed authored result states, and `data/submission-fields.json` owns eleven submission fields. The renderer escapes text and rejects unknown/missing/cyclic includes. Never edit generated copies.

See [runtime boundary](docs/RUNTIME.md), [desktop composition](docs/DESKTOP-LAYOUT.md), [template ownership](docs/TEMPLATES.md), [document composition](docs/PAGES.md) and [performance observations](docs/PERFORMANCE.md). Browser evidence remains Chromium; other browser/device/assistive-technology checks are deferred.
