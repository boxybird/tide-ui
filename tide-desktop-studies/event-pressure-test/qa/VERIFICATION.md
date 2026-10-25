# Pressure-test verification — 2026-10-24

This covers the independent `event-pressure-test/` study. The approved Shared Filters baseline remains the reference.

## Checks performed

- Source checks pass for 74 HTML pages and 5,061 local references: one H1/main, unique IDs, linked labels/descriptions, registered/private BEM classes, valid date/time attributes and real local destinations.
- All 283 files in the approved Shared Filters release match its exact hash inventory. Its preservation checks also verify earlier prototype, app and kit inventories. The copied `app/css/host.css` is byte-identical to the baseline. No kit file was edited.
- Fifteen search assertions pass: inclusive overnight/multi-day overlap; one recurring occurrence; rescheduled/current dates; unknown dates; category intersection; empty results; invalid dates and inverted ranges.
- Connected Chromium on Windows: all 14 event pages inspected at 1440 × 900. Selected-card case links expose their matching card in the bounded list. No horizontal overflow, broken photo or Show events/list misalignment was found.
- Eighteen responsive samples cover index, long copy, missing details, postponement, detail failure and feed loading at 320 × 740, 390 × 844 and 1024 × 768. All fit horizontally, with one H1 and no broken images. Phone event pages retain the full-height opening and natural document scroll; the list is a separate destination. Tablet retains the list/detail composition.
- Desktop geometry checked at 1366 × 650, 1440 × 900 and 1920 × 1080. The list/detail gap is 24px, the occupied native list gutter is 10px on this environment, and both bounded panels finish 34px above the viewport bottom. Show events and the list bottom align to the pixel. This remains an actual measurement, not a cross-browser width assumption.
- Ten browser interaction checks pass: feed retry retains the draft and restores count focus; detail retry retains the draft and a 540px list offset and focuses the new H1; cached refresh removes both stale notices while retaining the draft; both automatic loading demos clear busy state without stealing search focus; a Nov 1 date search returns the multi-day and all-day samples; no matches offers recovery; Reset/apply restores all 14 cases; phone/tablet failed-feed drawers expose a disabled unknown count and Escape returns focus to the trigger.

Observed values are in [browser-checks.json](browser-checks.json); source results are in [checks.json](checks.json). Screenshots are viewport captures, not artificially expanded full-page hero captures.

## What the exercise exposes

1. Long content needs room. Title and venue wrap at the existing type size, making a taller card and longer opening. A future title-length or summary policy would be a separate editorial/product decision.
2. No photo needs an honest composition. Existing Fallback and Summary show known facts and explicit unknowns. No substitute stock photo or invented information fills the gap. The spacious opening is a review candidate.
3. A date can describe a span or changed plan. Filters use interval overlap and the current date. All-day text, daily hours, one recurrence occurrence and a pending replacement date remain distinct.
4. Status affects the detail and action, not just the badge. Inactive cases have explanatory notices and no attendance action. Removed details disclose no obsolete schedule.
5. Unknown differs from zero. Loading/failed feeds have no numeric match claim. A known empty source has no filters to clear. A filtered empty result does.
6. Recovery keeps context. Draft choices remain separate from applied results; retry updates the failed surface rather than resetting both panes.

## Boundaries and adoption

All content is authored sample data, anchored to October 24, 2026, noon in Albuquerque. Loading/retry/cached examples are controlled local demonstrations. No actual network detection, offline cache, submission, booking or recurrence expansion is implemented.

Candidates for later acceptance are documented in the study README: status/action contracts, no-photo opening, wrapped status heading, unknown/empty/error compositions and date-span matching. Existing kit blocks are reused. This exercise promotes no component into the frozen kit.

Firefox and Safari remain deferred at the user's request. Physical-device and screen-reader checks were not performed. Chromium viewport testing and source semantics are the actual verification scope.
