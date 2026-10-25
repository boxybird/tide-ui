# Accepted changes for the next app release

These records preserve accepted behavior without modifying the approved app baseline or UI kit. Both items are now integrated in the separate [app release 1.1.0](../app-release-1.1.0/README.md), with ownership and new verification evidence. The approved baseline remains frozen; the successor awaits user review.

| Accepted | Item | Status |
| --- | --- | --- |
| 2026-10-24 | [Sticky event-list heading hierarchy](STICKY-HEADINGS.md) | Integrated 2026-10-25 in app1.1.0 as private complete-feed isolation; Chromium handoff/hit tests, measured wrapping and responsive checks pass. Original fix and baseline unchanged. |
| 2026-10-24 | [Venue page and scoped navigation](VENUE-DISCOVERY.md) | Integrated 2026-10-25 in app1.1.0: guide, exact venue scope, native entry/return/exit and scoped filters. All six theme/modes plus tablet/phone verified. Original study, baseline and kit unchanged. |

Accepting an item here does not approve all other pressure-test examples or select a new visual baseline. Check venue preservation from this directory's parent with `python -B release-handoffs/check_venue_preservation.py`; its report stays in `release-handoffs/qa/`.

Successor evidence: [ownership](../app-release-1.1.0/docs/COMPONENT-OWNERSHIP.md), [verification](../app-release-1.1.0/qa/VERIFICATION.md), [source/preservation](../app-release-1.1.0/qa/checks.json), [browser observations](../app-release-1.1.0/qa/browser-checks.json). Native Firefox/Safari and browser zoom remain unverified; these limits are explicit in the new release.

Versioned successor snapshot: [burque-app-1.1.0.zip](../app-release-1.1.0/dist/burque-app-1.1.0.zip), SHA256 `db2f3635ecedaaee63224c1117f27eed7c1ed569f89d29d53763ebfe90e4e975`. The 732-entry archive includes the exact frozen kit dependency and validates generated app references internally. This snapshot remains immutable; it does not replace the approved baseline.
