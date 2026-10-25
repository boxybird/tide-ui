# Smooth return when selecting another event · 1.0.3

The user clarified that smooth scrolling should occur when selecting a different event after scrolling down the right-hand details, not only on in-page links. The CSS rule was already present; a native full-page HTML navigation reset the document immediately.

The optional deferred helper lets the existing CSS scroll return to zero before following the selected event's real href. It does not turn the right column into a scrolling container, swap content or introduce a framework. The current event stays visible during the return; the selected event opens once the top is reached.

## Actual browser sequence

Chromium, default 1280 × 720 viewport:

1. Read The Late Set down to its attendance section. Results pane scrollTop was 512px.
2. Selected Ink After Dark from the left pane. Readings immediately after the click remained on The Late Set and stepped through document positions 1545.33, 1544, 1539.33 and 1530px, confirming a return in progress rather than an immediate new-page reset.
3. The real Ink After Dark HTML route then opened at document scrollY 0. Results pane scrollTop remained 512px, its full frame still left 24px below, and its selected card was correct.
4. Browser Back returned to The Late Set at scrollY 1545.33 and list scrollTop 512px.
5. At 390 × 844, the mobile event link navigated normally to Ink After Dark at scrollY 0 with an 844px hero.
6. No console warnings/errors were recorded in the QA tab.

Raw samples: `event-selection-check.json`. Screenshot: `event-selection-after.png`. The screenshot shows the arrival state; motion evidence is in the sampled positions and the browser interaction.

## Regression checks

Seven dependency-free Node behavior tests pass: wait until top; modified clicks; direct mobile/reduced-motion navigation; disabled storage; Escape cancellation; latest rapid selection wins; Back restores position. These tests use a controlled DOM/window harness and do not replace native engine testing.

Run `node --test tools/test-event-navigation.cjs`. The HTML checker now allows exactly the registered deferred navigation helper and continues to reject inline scripts, unregistered scripts, inline styles and event attributes. The underlying kit remains script-free and the original 176-file lock still passes.

Native Firefox/Safari and operating-system reduced-motion rendering were not exercised here. Browser-native easing determines the motion duration. A three-second fallback prevents a suspended or interrupted animation from indefinitely holding navigation; a new page-scroll gesture or Escape explicitly cancels it. No storage or history access is required for ordinary links to remain usable.
