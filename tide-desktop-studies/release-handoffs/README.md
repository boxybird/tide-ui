# Accepted changes for the next app release

These records preserve accepted behavior without modifying the approved app baseline or UI kit. Apply them in a successor app, document its ownership, and verify the acceptance checks before marking an item integrated.

| Accepted | Item | Status |
| --- | --- | --- |
| 2026-10-24 | [Sticky event-list heading hierarchy](STICKY-HEADINGS.md) | Accepted and preserved in pressure-test 0.1.1; required in the next app release. Not applied to the frozen baseline. |
| 2026-10-24 | [Venue page and scoped navigation](VENUE-DISCOVERY.md) | Accepted and preserved as venue-discovery 0.1.0; required in the next app release. Complete study remains frozen; baseline and UI kit unchanged. |

Accepting an item here does not approve all other pressure-test examples or select a new visual baseline. Check venue preservation from this directory's parent with `python -B release-handoffs/check_venue_preservation.py`; its report stays in `release-handoffs/qa/`.
