# Feedback normalization verification · 2026-10-27

The [feedback contract](FEEDBACK.md) defines the type, spacing and native/static state boundaries for kit 1.8.0. All 99 existing files under `examples/events/` match their pre-pass SHA-256 hashes, including existing user edits. Theme inputs and all resolved palette values are unchanged, preserving Bumble Dark. The application remains 2.0.4 and `main` is the only branch.

## Portable verification

Root `npm run build` and `npm run check` cover the distribution, all 978 HTML documents and local references, zero browser JavaScript, existing asset/document budgets and 600 contrast pairs. The suite contains 48 kit tests, 28 application template tests and seven local HTTP tests. New guards cover feedback geometry/type drift, status-only color variants, uniform Notice borders, heading-independent empty titles and explicit density, static badge semantics, native hidden/unavailable-link behavior, Button composition and all-theme shared specimens. The Button override guard distinguishes a selector that explicitly excludes Button from a selector that styles it.

Three distribution checks cover comment compaction: preservation of quoted text, escapes, URLs and license/preserve comments; identical rule/declaration sequences for every canonical CSS module; and generated header/layer boundaries. Ordinary source comments are omitted only from the combined generated stylesheet; no CSS value minifier is introduced and canonical comments remain intact.

The combined stylesheet measures 98,370 raw bytes / 12,586 gzip bytes against the existing 100,000 / 14,000 limits. The largest library is 17,951 gzip bytes against the existing 18,000 document limit. The main library extracts seven overview cases directly from the canonical HTML and links to the full matrix. Missing/duplicate cases fail the build; preview HTML is not copied into another source. No budget was raised.

## Rendered matrix

In-app Chromium: all ten modes at 1280×900, 430×900 and 320×900. All 30 runs pass. Each measures 30 cases, including four authored hidden cases. Checks cover explicit family/style/size/weight/leading/tracking/case, Badge geometry across statuses, optional icon dimensions, even Notice padding and neutral borders, toast wrapping/minimum shell/action targets, empty regular/compact spacing, context isolation, Button composition, error-summary type and zero document overflow.

Reviewed screenshots: Bumble Dark wide badges/notices/toasts and empty states, Bumble Dark 320px long/wrapped toasts, and Tide Light 320px empty states. Long status references wrap; toast actions move to another row when needed; empty-state headings/actions remain readable and unframed. Hidden examples have no rendered box and are absent from the accessibility-tree observation.

Native checks verified link navigation to the actual fragment destination, keyboard focus with the shared 2px outline and declared 3px gap, and Tab skipping the unavailable action. The engine quantizes the computed gap to 2.66667px; the rendered check allows fractional pixel rounding. Pointer hover produces the audited foreground and 2px underline. A held Enter did not expose `:active` on the native anchor in this engine; active double-underline behavior is covered by source contracts rather than claimed as a passed pointer-held observation. No toast engine or simulated Badge interaction was added.

## Adjacent regression checks

Existing Button and Form browser probes pass in Bumble Dark at 1280px and 320px after the compiler change. The application desktop smoke retains one filter/control set, no horizontal overflow, zero scripts and the bounded left pane ending 24px above the 900px viewport bottom. At 430px the native drawer opens with Close focus, closes and returns focus to Filters. These are smoke observations, not a renewed application-layout audit.

## Evidence and limits

Ignored local artifacts live in `build/reports/feedback-normalization/`: baseline/source-parity hashes, thirty matrix measurements, native link observations, prior-component/application smoke checks and inspected screenshots. `tools/feedback-browser-probe.js` is development-only and read-only; it is never served or shipped as browser code.

Firefox/Safari, physical devices, screen readers and an actual OS forced-colors session were not run. Forced colors and native link active declarations are source-reviewed. Dynamic announcement timing, focus management, queueing, persistence and dismissal remain consumer responsibilities and are not implemented by the static specimens. Targeted contracts and measurements do not establish whole-product accessibility conformance.
