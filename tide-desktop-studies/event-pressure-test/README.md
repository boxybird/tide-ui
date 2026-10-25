# Event pressure test — priorities 1–3

Open [case review](http://127.0.0.1:4187/event-pressure-test/index.html) or [browse the copied app](http://127.0.0.1:4187/event-pressure-test/app/index.html?preview-filters=open).

Start with the long-copy case, then missing details, a changed event and a retry scene. Each case link opens the same feed with its matching detail; desktop review links bring the selected card into view. On a phone, the list and event are separate pages as in the approved app. Actual checks and findings are recorded in [qa/VERIFICATION.md](qa/VERIFICATION.md).

Refinement 0.1.1 corrects the inherited sticky month overlap: the scrolling feed has its own stacking context beneath the permanent desktop lineup summary. Calendar headers still push each other away normally. The user accepted this fix on 2026-10-24; it is preserved and required in the next app release. See the [behavior and integration contract](../release-handoffs/STICKY-HEADINGS.md) and [before/after audit](qa/sticky-handoff/README.md). Both original 0.1.0 and accepted-fix 0.1.1 archives remain unchanged.

This is authored sample data in a separate app copy. No real submissions, event API, booking, service worker or PWA cache is introduced. Reference clock: October 24, 2026, noon in Albuquerque. All 283 Shared Filters baseline files remain frozen; the app uses that kit's CSS/assets read-only. Type, palette, spacing inputs, controls and base desktop/mobile/tablet shell are preserved.

## What to inspect

| Priority | Cases | List / detail treatment |
| --- | --- | --- |
|1 · Messy metadata|Very long title/venue, poor phone photo, overnight, multi-day across months, all day, one recurring occurrence, online/donation, unknown end and missing time/venue/price/photo|Unclipped wrapping with existing type; explicit date span; no invented duration, price or address; existing no-photo surface with a complete facts summary.|
|2 · Lifecycle|Cancelled, postponed/new date unknown, rescheduled, sold out, ended and removed|Existing status Badge in card; Notice before detail opening; current schedule is consistent; inactive attendance actions lead back to the lineup; removed listing exposes no old attendance data.|
|3 · Waiting/recovery|Initial loading, first-load failure, no upcoming events, detail loading/failure, stale cached-content illustration|Existing Empty/Notice/Button compositions; unknown counts are not zero; retry preserves original controls/list; no-upcoming differs from no matches; cached wording appears with the retained details.|

Loading specimens are held for inspection. The review's **Play loading → ready** links complete the local sample after a short delay. **Try again** in failed scenes resolves local sample HTML. This demonstrates the UI state contract, not measured network or offline availability.

The feed intentionally includes upcoming, changed, undated and archived examples together. Their grouping is study coverage, not a proposed public-feed inclusion policy. The copied Saved/submission/help and earlier event pages remain baseline samples; new scope is the 14 authored cases and 6 recovery scenes.

## Data and behavior rules

- Inclusive date filtering uses overlap: an event starting October 30 and ending November 2 matches November 1. An overnight event matches both local dates. Unknown dates are excluded whenever a date bound is applied. Undated listings remain reachable without a date restriction.
- Recurrence is one explicit dated occurrence, not a range that makes every date match. The rescheduled sample matches its new date, not the superseded one.
- Missing price is “Price TBA”/“Price not announced,” never Free. All day is text, not an invented midnight interval. A known start without an end has no made-up duration. Online and unknown locations do not acquire fictional street addresses.
- Cancellation/postponement/ended states retain labelled original facts where useful; removed details do not show an old schedule. No purchase, RSVP, calendar or real contact workflow is implied by the sample actions.
- Applied results remain separate from the filter draft. Feed requests with unknown results disable applying and show “Match count unavailable”; zero results remain valid once data is known. Host input/GET logic is reused.
- Detail retry updates only the detail and returns keyboard focus to its title. Feed retry retains controls, then focuses the result count. Automatic demonstrations do not move focus. Busy states clear on completion/failure; polite status feedback communicates recovery. Cached retry leaves existing content readable while checking.

## Component ownership

The frozen kit supplies Card, Date, Badge, Notice, Empty, Button, Hero, Details, Summary, Field/Choice and the Filter panel. No kit module, primitive, theme or registry is edited.

Private `tide-pressure` composition styles live in `css/pressure.css`: card-heading wrapping/status placement, notice placement, no-photo opening composition and empty-panel sizing/semantic title. `app/js/pressure.js` owns fixture lifecycle, focus, recovery and busy state. The copied `filters.js` reads the scene's known/unknown state; the copied search core adds interval overlap. Base `app/css/host.css` remains byte-identical.

`tide-pressure__feed` owns only local stacking isolation. The persistent summary must paint above the entire feed, whose sticky group headings paint above its cards. A group heading leaving its containing section must never cover the summary count or controls. This host contract is accepted for the next app release; the frozen baseline and kit remain untouched.

These are documented candidates, not new public kit components. Once accepted, any reusable variant/composition can move into a subsequent kit release with shared HTML, states and all-theme specimens.

| Discovery | Current home | Possible future kit adoption |
| --- | --- | --- |
| Status and In view wrap independently of category | `tide-pressure__card-heading` plus existing Badge/Card | A Card status-slot composition with unchanged type/control inputs. |
| No uploaded photo still needs a full opening | Existing Fallback + Summary, private no-photo composition | An optional Event opening composition using existing roles. |
| Changed plans affect the available action | Fixture data + existing Badge, Notice and Empty | State/action contracts with canonical examples. |
| Loading, failed, stale, empty-source and empty-search differ | Existing Empty/Notice/Button + host `pressure.js` | Markup/state examples; loading, routing and retry remain host behavior. |
| Match count may be unknown; calendar matches may span dates | Copied filter coordinator and search core | Unknown-count contract; interval matching stays application logic. |

## Build and verify

```text
python -B tools/build.py
python -B tools/build.py --check
node tools/test-search.cjs
python -B tools/check.py
```

Builders write only this study. Source checks verify current baseline/prior hashes, the accepted sticky-fix inventory, real HTML links, one H1/main, accessible labels and described IDs, BEM ownership and date/unknown-value contracts. Browser evidence belongs in `qa/`; distinguish actual Chromium checks from deferred Firefox/Safari and assistive-technology/device checks. No builders or QA writers run inside the frozen baseline.
