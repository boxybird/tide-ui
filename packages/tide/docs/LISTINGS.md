# Listing components · Tide 1.9.0

Event cards, prominent dates, calendar groups and result summaries own reusable presentation. Native links own navigation. Consumers render actual event/status/count/hidden state and own routing, matching, announcements and viewport placement. The kit ships no browser JavaScript and consumes no live event source.

Canonical recipes: `templates/listing-card.html`, `listing-date.html` and `listings.html`. The build-time authored renderer is `tools/listing_specimens.py`; it escapes text and derives known date labels from fixed specimen dates. `frames/listing-states.html` is generated in all ten theme/modes. Existing library/list/adopted specimens remain compatibility usages and link to the full matrix. Documentation-only scrolling/context CSS stays in `site/css/docs.css`.

## Type and geometry

| Element | Manrope at the default root | Spacing / geometry |
| --- | --- | --- |
| Card | 14px / 24px, weight 400 | 24px block / inline insets; unframed surface and existing texture |
| Category | 12px / 20px, weight 550, label tracking, uppercase | Heading row minimum 24px; 16px wrapping gap |
| Card title | 24px / 32px, weight 580, title tracking | 8px after heading; independent of heading level |
| Venue | 14px / 24px, weight 400 | 4px after title |
| Metadata | 14px / 24px, weight 400; price weight 550 | 16px after copy; 16px column / 12px row gaps at every viewport |
| Date day | 26px / 32px, weight 500, event tracking | Minimum 2ch day column; 8px gap to parts |
| Date parts | 12px / 16px, weight 400 | Two lines; minimum 4ch width; longer localized labels can grow |
| Calendar heading | 14px / 24px, weight 550 | Header 8px / 24px padding; 12px wrapping gap |
| Calendar count | 12px / 20px, weight 400 | Block below heading |
| Month jump | 14px / 24px, weight 550 | Minimum 44px square target; 8px navigation gap |
| Result count and order | 14px / 24px, weight 400 | 16px / 24px insets; 12px wrapping gap |

Values use named rem-based type/spacing inputs. Date columns use font-relative minimums, not clipping widths. Family, style, weight, tracking and case are explicit on component roots; intentional category/title/date styles are explicit on slots. There is no viewport-driven density change. Useful long content wraps and can increase height.

Fixed gaps delimit metadata fields. The legacy decorative `__separator` nodes are hidden and omitted from new recipes, so wrapping cannot leave orphan divider lines. Existing markup remains valid; visible inter-card separators retain their separate list contract.

## Event cards

Use an article labelled from its heading. `__category` is the explicit category slot; legacy `tide-eyebrow` inside `__heading` receives the same recipe. Existing content/copy/title/venue/meta/price/status slots remain supported. List and event panes gain no outer decorative frame, radius or clipping shell.

An optional sibling `a.tide-event-card__link` covers the article and needs a meaningful label and real href. Do not wrap card contents in that anchor or nest controls inside it. The optional `__save` slot sits above the covering link and reuses Icon button. Its matrix link opens a saved-page specimen; it does not save an event. A consumer needing a true save control supplies its actual native control/state behavior.

Cover-link hover and keyboard focus use an audited accent title. Held active uses audited accent-hover and an underline. These states do not change type or spacing. Focus retains the shared 2px outline with an inset 3px gap. Independent actions keep their own focus/hover treatment and destination.

`--in-view` composes a neutral Badge in `__status` with a 1px inset outline for a paired preview. It is not a tab, toggle or aria-selected article. `aria-current="page"` belongs on a link only for the actual current event document. Hosts keep preview class/status visibility consistent. Cancelled, sold-out and changed-time examples reuse Badge words/colors with the same geometry. A cancelled event may retain useful detail navigation; unavailable details omit the covering link while retaining useful status/context.

Native hidden cards have no rendered box. Separators follow preceding visible siblings, including hidden entries between visible cards. The first visible card has no top separator; later visible cards have one. This works inside and outside calendar groups. Do not add a border around whole panes.

## Known and unknown dates

Known dates use one native time element with a valid ISO date and full accessible date label. Day/parts fragments are aria-hidden to avoid repeating them in the accessible name. The English specimens include single-/two-digit days and a year boundary. Include the year in the full label even when the compact block shows day/month only.

Minimum columns align ordinary metadata and allow longer localized labels to grow. Do not fabricate dates, use `00`, put an interval into an invalid datetime, or turn “to be confirmed” into a fake time. Unknown dates/times remain ordinary text. Multi-day detail needs truthful start/end time elements and wording; a compact start date alone does not describe duration.

## Calendar and results

Use a labelled group section, header/title/count, and optional labelled navigation with real fragments. Destinations have unique IDs and tabindex -1 where fragment focus is needed. Month jumps keep 44px targets. Hover uses audited accent-hover and a thicker underline; active uses a double underline; keyboard focus uses the shared outline. Counts describe visible entries with correct singular/plural wording. Hide empty groups and omit unavailable month links.

`--sticky` pins the header inside its nearest scrolling ancestor. `--tide-event-group-offset` defaults to zero and accepts a consumer's measured occupied-header offset. Group scroll margin combines it with the existing 24px clearance. Wrapping headings/counts/navigation may increase header height. The matrix uses a documentation-only bounded scroller with a sibling result summary above it; application panes, occupied scrollbar/gutter measurements and private sticky geometry remain application-owned.

Result count may be a heading or paragraph with the same component type. Order is ordinary text that can shrink/wrap. “Soonest first” is not a sort control. Zero/one/many/long/hidden/context examples are authored results, not live regions on page load. Consumers own real count updates and appropriate announcements. Empty/recovery explanations compose [Empty state or Notice](FEEDBACK.md).

## Ownership and verification

CSS homes: `components.css` for card/date and root type, `patterns.css` for calendar/preview/result slots, and `layout.css` for the result shell. Event card now has explicit kit ownership. Two existing consumer choices remain allowed: display none/inline-flex on `__status`, and outline none on `--in-view` when no paired pane is visible. Those exceptions permit no type, padding, border or metadata overrides. Application sources remain intact.

The portable ownership guard checks registered target/property/value exceptions and rejects broader redefinitions. Other owned blocks retain strict guards. Checks also cover type/geometry mutations, date labels, escaped specimen text, native link layering, authored counts, hidden separators and all-theme fixtures. Existing 600 contrast pairs cover the text/action roles; palette values are unchanged.

Run root `npm run build` and `npm run check`. The development-only, read-only `tools/listing-browser-probe.js` measures generated specimens and is never served. [Verification](LISTING-VERIFICATION.md) records actual browser coverage/limits. The main library links to the full matrix while keeping its document budget.
