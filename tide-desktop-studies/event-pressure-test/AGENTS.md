# Event pressure test

Separate copy of the user-approved Shared Filters baseline. Never write to `../shared-filter-release/`, its kit or earlier studies. Its complete 283-file lock must pass before/after work. Use Python `-B`; avoid bytecode in frozen imports.

This is a UI pressure test with authored sample data, not collection of real submissions or a backend/PWA implementation. Preserve baseline type, spacing, themes, controls, touching cards, unframed panes, header, Margin Reveal widths, native scrollbar measurement and responsive filter behavior. Consume the frozen kit directly. New study compositions belong to `tide-pressure`; review presentation to `tide-pressure-review`.

Priorities 1–3 only: messy event metadata, lifecycle states and simulated loading/recovery. Reuse Badge, Notice, Empty, Date, Card, Hero, Details, Summary, Field and Button. Document new compositions and conditional-data rules here; adoption into a kit release needs user acceptance later. Do not mutate the accepted kit during this experiment.

Build with tools/build.py. Checks must verify source/links/semantics, interval filtering and baseline hashes. Actual browser evidence is Chromium; Firefox/Safari remain deferred. Preserve local-only operation and all earlier releases.

Refinement 0.1.1: the generated `tide-pressure__feed` wrapper uses `isolation: isolate`, containing month/card stacking below the permanent lineup summary. Keep the native group push-off and existing scroll owners. Do not replace this with a global z-index escalation or scroll listener. Before/after and mobile/tablet evidence: qa/sticky-handoff/. Both 0.1.0 and approved baseline archives remain immutable.

Accepted 2026-10-24: preserve this sticky-heading fix and carry it into the next app release. Canonical contract: ../release-handoffs/STICKY-HEADINGS.md. Exact source/snapshot/evidence lock: ../locks/event-pressure-test-sticky-0.1.1.json, verified by tools/check.py. Keep the 0.1.1 snapshot immutable and implement later app refinements in a successor. This acceptance does not approve the remaining pressure-test compositions or permit changes to the frozen baseline/UI kit.
