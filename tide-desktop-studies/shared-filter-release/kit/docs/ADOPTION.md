# Adoption shipped in 1.3.0

The accepted shared filter shell is extracted into Filter panel. The independent app copy consumes its CSS and canonical HTML; private panel/body/footer/count/reset-row rules were removed from that consumer. Matching, routing, dialog lifecycle and viewport geometry remain host-owned. See [search/filter contract](SEARCH-FILTERS.md). The original 1.2.1 kit and approved prototype remain frozen.

# Growing Tide from the app

The app is the playground. This maintained kit is the source for reusable HTML, CSS, states and accessibility contracts. A useful discovery comes back here before we treat it as a settled pattern. The original `tide-ui-kit/` remains a preserved reference; the app consumes this maintained kit directly. Do not maintain competing implementations of the same component.

## What earns a home

First check whether an existing component already fits. New wording on a badge is a use of Badge. A recurring layout of fields, buttons and feedback is a documented composition. A new reusable visual/semantic unit gets a BEM block and component entry. App routing, dataset matching and persistence remain application behavior, with their integration expectations documented alongside the component.

Experiments may live in the app while being evaluated. Record their owner and purpose; do not silently make them public kit API. Once accepted, move the reusable CSS to its kit source, add the HTML/state specimens and make the app consume that source in the same change. App-specific viewport composition stays in app CSS.

## Selected preview

**Existing components:** `tide-event-card` and neutral `tide-badge`. **Adopted state:** `tide-event-card--in-view`, optional `tide-event-card__status` slot. CSS home: `css/patterns.css`; HTML home: `templates/adopted-patterns.html`.

```html
<article class="tide-event-card tide-event-card--in-view" aria-labelledby="event-name">
  <a class="tide-event-card__link" href="event.html" aria-label="View Ink After Dark"></a>
  <div class="tide-event-card__content">
    <div class="tide-event-card__heading">
      <span class="tide-eyebrow">Workshop</span>
      <span class="tide-badge tide-event-card__status">In view</span>
    </div>
    <h3 class="tide-event-card__title" id="event-name">Ink After Dark</h3>
    <!-- Venue, prominent date, time and admission use the existing card contract. -->
  </div>
</article>
```

The host keeps the modifier and badge visibility in sync with the displayed preview. Use `hidden` on other status slots. The badge is text, not a control, tab or live region. Do not put `aria-selected` on an article. `aria-current="page"` belongs on the link only when it points to the actual current event document; a preview on a search URL is different. The single-column app suppresses the preview outline and label because no detail pane is simultaneously visible. This visibility decision belongs to the app composition.

## Calendar feed

**Adopted component:** `tide-event-group` with `__header`, `__title`, `__count`, `__nav` and `__jump`. Add `tide-event-group--sticky` when the heading should remain inside its nearest scrolling ancestor. CSS home: `css/patterns.css`.

Choose heading levels from the document outline; classes own appearance. Give the group and title unique IDs, label the section from its heading, and use real fragment links for month jumps. The optional nav needs a meaningful label and at least two available destinations. Each jump has a 44px minimum target. Native links remain usable without JavaScript.

The host updates counts and `hidden` on groups/cards after filtering. Hide a group with no matches and omit its month jump; hide the nav when fewer than two months remain. The group's CSS places one separator between visible cards, including when hidden cards sit between them. The underlying card separator also ignores hidden neighbors.

`tide-results` remains the existing result-summary composition. Use `tide-results__count` on a heading or paragraph, and `tide-results__order` on the chronological-order label. The host owns correct singular/plural wording and whether a polite live region is appropriate. Plain “Soonest first” text does not imply an interactive sorting control.

Desktop list-only scrolling, focus on the destination heading, smooth event navigation and Back restoration belong to the host navigation helper. The CSS component does not implement a router.

## Search and filters

**Adopted component:** `tide-expandable`. The filter form itself composes existing Field, Fieldset, Choice, Button, Result summary and Empty state. The app owns matching rules, query parameters, validation and result announcements.

```html
<details class="tide-expandable">
  <summary class="tide-expandable__summary">
    Filters
    <svg class="tide-icon tide-expandable__icon" aria-hidden="true" focusable="false" viewBox="0 0 15 15">…</svg>
  </summary>
  <div class="tide-expandable__body">
    <!-- Existing labelled fields and actions. -->
  </div>
</details>
```

Use native `details`/`summary`, not a simulated button. Enter or Space toggles it; Tab reaches controls when open. Do not duplicate the browser's expanded state with manually managed ARIA. The SVG is decorative. CSS owns the 44px summary, border, chevron orientation and inner spacing; the parent owns external margins. A required invalid field in a closed disclosure must reveal its parent before focus/reporting.

Date ranges have visible From/Through labels and an inclusive/local-date hint. Multiple categories combine with OR, then intersect with text and dates. Keep draft controls distinct from applied results, preserve entered values on invalid submission, and provide a clear reset from no results. These are the current app's interaction rules, not behavior supplied by this script-free kit.

Loading, no-results and preview-failure messages reuse existing text, Empty state and Notice components. A new message alone does not justify a new CSS block.

## Adoption checklist

1. Identify reuse, a composition, a variant or a new block; record that decision.
2. Put reusable styles in the kit's component layer using existing semantic tokens. App layout stays in its documented composition file.
3. Add the component's name, purpose, classes, source, variants, states and behavior to `component-manifest.json` and `docs/COMPONENTS.md`.
4. Add shared HTML specimens to all themes and both modes. Include keyboard/focus, invalid, loading, empty or selected states when they apply.
5. Switch the app to the kit implementation and remove the duplicated styling. Verify before/after geometry and appearance.
6. Run build, ownership/markup checks, palette gates and relevant behavior tests. Review narrow screens, text enlargement and native keyboard operation.
7. Record verification limits and release notes. Preserve the previous package. Public token/required-markup breaking changes require an explicit version and migration notes.

The app's source check rejects shared blocks with no registry home and redefinitions of kit-owned disclosure/group/result styles. App-private composition blocks are explicitly allowed. These checks support review; they do not judge whether a new abstraction is useful.

## Other cases worth exploring next

Keep the same design while considering cancelled/postponed events, changed times after saving, unavailable/deleted event URLs, lost connectivity and retry, missing/poor poster images, long venue/title text, accessibility information and time-zone wording. Each accepted state should reuse existing components before introducing a new one. Live search can follow later with loading, announcement, Escape/clear and stale-response rules defined before implementation.

## Release 1.1.0

Two additive blocks, an optional selected-card modifier/status slot, and documented result-summary elements were adopted from app 1.2.0. `templates/adopted-patterns.html` is shared by the main Components section and `frames/app-patterns.html` in every theme/mode. `css/patterns.css` is bundled in `tide.components.extensions`. No palette, spacing, typography, radius, target or font primitive changed. The original kit and the complete pre-adoption app 1.2.0 ZIP remain preserved.

H5/H6 now share the existing heading-margin reset, so deeply nested semantic headings keep the same class-based spacing. Calendar navigation and result summaries wrap when space or enlarged text requires it. These refinements introduce no new sizing or color primitive.
