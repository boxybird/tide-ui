# App playground and kit ownership

The maintained system is `kit/` (kit 1.2.0). This app consumes `kit/css/tide.css` directly. The original `../tide-ui-kit/` is a frozen reference, not a second implementation to edit in parallel. The complete pre-adoption app/kit remains preserved in `dist/tide-responsive-app-1.2.0.zip`.

## Current ownership map

App 1.3.0 consumes Prose and Content page from kit 1.2.0. `kit/css/content.css` owns the reading/layout rules; `kit/templates/content/help.html` is shared by the app and the kit fixtures through `kit/tools/content.py`. The app supplies its existing header, real local destinations and review gallery. No prose or content-page selectors are redefined in app CSS. See `kit/docs/CONTENT.md`.

| What appears in the app | Reusable home | What remains app-owned |
| --- | --- | --- |
| In view label | Existing `tide-badge` in `tide-event-card__status`; no new badge component | Which event is previewed; suppressing the label in single-column layouts |
| Previewed card outline | `tide-event-card--in-view`, `kit/css/patterns.css` | State updates and the single-column visibility decision |
| Filter disclosure | `tide-expandable` summary/icon/body, `kit/css/patterns.css` | External inset, selected filter count and date/category form arrangement |
| Date fields, errors, category choices, clear/apply actions | Existing Field, Fieldset, Choice, Button, Link | Matching, inclusive dates, draft/applied state, validation and GET URLs |
| Month header, counts, jumps and separators | `tide-event-group`, optional `--sticky`, `kit/css/patterns.css` | Calendar grouping from data, hidden states, desktop list-only scrolling/focus |
| Result count/order | Existing `tide-results` composition, documented `__count` / `__order` | Accurate count wording, live-region updates and data ordering |
| No results or preview unavailable | Existing `tide-empty` and text/action components | Cause, recovery destination, loading/failure state |
| Left/right workspace and viewport fit | Explicit `tide-app` composition in `css/app.css` | Width/breakpoint, header geometry, 24px bottom gap, natural detail scrolling |
| Event content | Existing Card, Date, Hero, Details, Inclusions, Schedule and Place | Event data and native HTML routes |

The full registry is `kit/component-manifest.json`; visual/HTML specimens are in the kit Components section and `templates/adopted-patterns.html`. Supporting typography/layout helpers have recorded CSS homes too. Public class names use `tide-`; application composition uses `tide-app`. Review presentation uses `tide-review`.

## Rule for future iterations

Experiment in the app, then decide what is worth keeping. Reuse first. If it is a reusable unit, adopt it into the kit with a name, CSS/HTML source, state/behavior contract, all-theme specimens and verification; switch the app to that source and remove duplicates in the same change. If it is a composition of existing parts, document the composition and its owner. App data and orchestration do not become fake CSS behavior. See `kit/docs/ADOPTION.md` for the checklist.

`tools/check.py` verifies that shared blocks used by the app have a registry home, permits the two private composition families, and rejects redefinitions of kit-owned disclosure/calendar/result-summary selectors. It still verifies the original 176-file kit lock and frozen 263-file baseline. Component/host ownership helpers live in `kit/tools/contracts.py` and have regression tests.

## Useful next UX states

Cancelled/postponed or changed-time events, a missing event URL, connection loss/retry and a saved event changing after it was saved are the next useful cases. Most can begin with existing Badge, Notice, Empty state and Button. Do not add a new component solely for new wording. Live search remains optional later work; its loading, stale-response, keyboard and announcement rules should be specified before it is added.

## Release 1.2.1

This is an ownership/refinement release, with the same event data and app behavior. Kit 1.1.0 adopts two blocks, the preview modifier/status slot and result-summary elements. Repeated app CSS was removed. Heading margin reset now includes H5/H6, keeping class-based type independent of semantic level. Calendar and result-summary compositions can wrap under enlarged text. Before/after browser measurements preserve the app's normal desktop, open-filter and 320px layouts exactly. See `qa/KIT-ADOPTION.md` for verification.
