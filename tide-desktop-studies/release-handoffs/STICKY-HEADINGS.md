# Accepted carry-forward: sticky event-list headings

Accepted by the user on 2026-10-24. Required in the **next app release**, not a change to the approved Shared Filters baseline or its UI kit. Acceptance covers this layering correction only; the other pressure-test compositions remain under review.

## Preserved implementation

- Source: `../event-pressure-test/css/pressure.css`, `.tide-pressure__feed { isolation: isolate; }`.
- Markup owner: `../event-pressure-test/tools/build.py`, which places that private class on the existing `#pressure-feed` wrapper around all date groups/cards.
- Exact snapshot: `../event-pressure-test/dist/event-pressure-test-0.1.1.zip`.
- Snapshot SHA256: `b0a0ff76ccde6dd85d501e8715a6de629cbec7f1b3126de68268df647f595d21`.
- Preservation inventory: `../locks/event-pressure-test-sticky-0.1.1.json` locks the implementation, snapshot and captured evidence. The study's existing source checker verifies it along with the approved 283-file baseline.
- Before/after evidence and observations: [focused audit](../event-pressure-test/qa/sticky-handoff/README.md).

The archive is a preserved study snapshot with the existing sibling kit as its runtime dependency. It is not a new approved app baseline or standalone deployment package.

## Behavior contract

| Surface | Required behavior |
| --- | --- |
| Desktop, at the current 75rem breakpoint and above | The permanent lineup summary, including label, event count, order and filter control, remains legible and clickable above the complete feed. Sticky date-group headings sit below its measured height. |
| Date-group handoff | As the following group arrives, its heading pushes the outgoing heading upward. The outgoing heading passes behind the permanent summary; it never paints over that summary or its controls. Cards remain below calendar headings. The same rule applies in either scroll direction and to every group, including undated/archive groups. |
| Tablet, current 60–75rem range | Retain the approved bounded list and adjacent event, with existing month-heading behavior under the app header. Do not make the lineup summary permanently sticky as part of this fix. |
| Phone, below the current 60rem breakpoint | Retain natural document scrolling and separate list/event destinations. Calendar labels pass behind the persistent app header, using the existing header offset. Do not add the desktop summary or an inner scrolling window. |
| App navigation and filter dialog | The app header and modal retain their existing precedence above feed contents. Opening/closing filters, focus restoration and keyboard access remain host-owned and unchanged. |

Desktop visual order, from front to back: **app navigation/dialog → permanent lineup summary → feed's sticky group headings → feed cards**. These are local relationships, not a new global z-index scale.

The summary and the complete feed must be sibling layers in the same list composition. Their surfaces stay opaque through the existing semantic canvas colors. Keep the existing measured summary offset responsive to font loading, wrapping, resizing and zoom; do not hardcode its observed 132px height.

## Integration into the next app release

1. Create a successor app copy; consume the approved kit unchanged. Do not edit `shared-filter-release/` to apply this fix.
2. Give the complete feed wrapper a stacking context using `isolation: isolate`, preserving the summary as the sibling above it. Map the study's private class to the successor's documented app composition owner. This is host layout behavior, not a new kit component or a global change to every Event list.
3. Keep existing sticky positions and local token values. Do not solve this by raising month headings, escalating global z-index numbers, adding clipping/overflow to ancestors, translating content, or replacing native stickiness with a scroll listener.
4. Preserve the scroll owners and geometry: bounded left list, natural right document, current widths/gaps, native scrollbar measurement, `24px + occupied gutter` desktop bottom clearance, and Show events aligned with the list bottom. Preserve phone/tablet filter placement and controls.
5. Register the accepted host rule and its verification evidence in the successor's ownership/release documentation. Close this carry-forward item only when the successor contains the fix and passes the checks below.

## Release acceptance checks

- Slowly scroll both ways across October → November and every later group boundary. Inspect the beginning, partial push-off and completed handoff. The lineup label/count/control must remain above the outgoing month; a pointer hit test in those areas must resolve to the summary, not the month or a card.
- Confirm month jumps still reveal the intended group without hiding its heading under the summary or app header. Repeat after narrowing results, when a month disappears or the feed has one group, and after restoring all results.
- Resize through the existing desktop/tablet/phone breakpoints and a short desktop window. Check title wrapping and browser zoom so the offset follows the measured summary rather than a fixed height.
- Verify filter controls and focus, the header, list bottom allowance, Show events alignment and natural event-detail document scroll. Opening the mobile/tablet dialog must not expose feed content above it.
- Review all three themes in light and dark mode when integrating the next release; retain semantic surfaces and existing tokens. Run the successor's source/ownership/preservation checks. Never run a QA writer inside a frozen release.

Actual current evidence is Chromium on Windows: exact matching desktop before/after geometry, four handoff samples in both directions, tablet 1024 × 768 and phone 390 × 844, plus modal open/Escape verification. Firefox/Safari, physical-device and screen-reader checks remain deferred; this document does not mark them passed.
