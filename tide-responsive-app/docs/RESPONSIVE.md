# Responsive composition contract

## The same kit, at three scales

No card, type, spacing or corner primitives were redesigned. The app owns the space around components. Desktop width is capped at 70rem (1120px at the default root size). A reading route uses at most 42rem; the submission form is capped at 44rem.

Under 45rem, browse is a full-width, single-column list with touching cards. An event opens a full-height photographed page followed by richer information. The header is omitted on that event page because the photo toolbar supplies back and saved navigation.

At 45rem, a portrait tablet gains comfortable outer space and additional header links, but keeps one centered reading column. The individual event still has its own page. There is no squeezed two-pane layout at 834px.

At 60rem (960px), there is enough room for a 390px result pane, 24px gap and useful event detail pane. Both appear together. The list remains near the reader as the document scrolls down the event. Its own scrollbar is visible and keyboard accessible. The detail pane uses ordinary document scrolling.

The results pane fits fully on arrival, with at least 24px beneath it. Its maximum height is the current dynamic viewport height minus the actual shared header geometry, the 24px workspace top gap and the 24px bottom gap. Header control height, padding and border come from the kit tokens; one composition variable sizes the header and the available space together. No laptop-specific height or JavaScript measurement is used. Short desktop windows keep the same bounded pane. Its height remains stable while the event document scrolls; it does not expand as the header leaves the screen. At narrower/mobile widths, results return to normal document flow.

At 74rem, outer insets are no longer needed because the max-width itself supplies the margins. Wider displays stay contained. At 1920px the application is still 1120px wide.

These are content-fit decisions, not device detection. A landscape tablet can use the paired view; an enlarged desktop page can reflow to the single-column view.

The form uses an inline-size container query at 32rem so date/time and admission/age pairs sit side by side only when their own container has room. Other fields retain their full width. See MDN's [size container query guidance](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries). The base layout remains a usable single column if a browser ignores the enhancement.

## CSS and naming

App 1.3.1 removes decorative outer borders and corner clipping from the results and individual-event panes, including the empty/unavailable preview surface. The panes remain unframed at every width. Their widths, 24px gap, bounded list scrolling and natural event-document height keep the existing contracts. This was an app-composition correction; kit 1.2.1 documents the unframed rule without changing component CSS.

The 1.1.0 UX fixture adds calendar groups around the unchanged card component. Each group has a quiet sticky month/year heading and count. The Oct/Nov links remain in that heading while you browse deep in the feed. Desktop month jumps scroll only `#results` and focus the target heading without moving the right-hand document. The normal single-column/HTML-anchor fallback remains intact. See `STRESS-TEST.md`.

The 1.2.0 enhancement filters those same cards in place after a GET navigation. Native date fields stack to remain usable at 320px and in the narrow desktop pane. The filter disclosure remains within the existing bounded list. Count, month headings and jump links reflect only matches; hidden cards do not add extra separators before the first visible card. Search/event routes share the same filtered footer geometry to retain list scroll even at the bottom. A single matching event uses the existing full-height preview; no matches use the kit empty state. See `SEARCH-FILTERS.md`.

Native smooth scrolling is enabled on the document and the results pane only when `prefers-reduced-motion: no-preference` matches. In-page event links glide to their destinations; reduced-motion users retain immediate scrolling. Wheel, trackpad and touch movement keep the browser's native behavior. No custom easing loop or scroll interception is introduced.

Event cards link to separate HTML pages. The 1.0.3 desktop enhancement makes a selection from a scrolled event glide to the top of the current document before following that real link. `scrollTo({behavior: 'auto'})` uses the root's existing CSS `scroll-behavior`; a frame observer detects arrival rather than driving a custom animation. The next event opens at the top. A short-lived session entry carries the left pane's scroll position to the destination, and history state restores the reading/list position on Back. Storage failures do not block links.

Reduced-motion and mobile users navigate directly. Modified clicks retain native new-tab behavior. Escape or a deliberate new page-scroll gesture cancels a pending return. Without JavaScript the same HTML links still work. The photo, width, bounded left pane and normal document-scrolling right detail remain unchanged. See `qa/EVENT-SELECTION.md` for the actual browser sequence and limits.

API references: MDN [scrollTo](https://developer.mozilla.org/en-US/docs/Web/API/Window/scrollTo), [pageshow](https://developer.mozilla.org/en-US/docs/Web/API/Window/pageshow_event) and [sessionStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage).

`tide-app` owns page composition: header, results, detail and form rows. `tide-review` is solely the review gallery. Existing kit components remain `tide-event-card`, `tide-event-hero`, `tide-field`, etc. Modifiers require the base class on the same element. States use native attributes (`open`, `checked`, `aria-current`) where possible. `data-preview` is a visual relationship between the static desktop list and detail.

When adding a new reusable component, use the kit's documented extension layer and manifest. Use an app composition class for a one-off arrangement. Don't reach into private palette primitives, add per-theme component selectors or change global spacing to fix one screen. Give headings their semantic level and the public title class independently.

The app uses semantic tokens for every color, including borders and selected states. All six theme modes render the same source. Photo-context roles keep the hero legible independently of the page mode.

## PWA next steps

This study is responsive and has safe-area-aware layout (`viewport-fit=cover` and `env(safe-area-inset-*)`), small-viewport height units and explicit in-app back navigation. It is not an installable PWA yet.

Once the real application is defined: provide a secure origin and manifest, tested icons and standalone navigation; define what can be read offline and when cached event dates are stale; add update/retry states; restore scroll position and active event on navigation; confirm keyboard and touch behavior on actual devices. Decide which data is persistent and how removal, privacy and storage failure work. Request notification permissions only in a deliberate user flow.

Installation availability and criteria vary by browser. A service worker is useful for the chosen offline strategy; do not treat it as a universal installation requirement.

MDN references: [standalone app](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/How_to/Create_a_standalone_app), [installability](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable), [safe-area environment values](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/env).
