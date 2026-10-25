# Desktop list viewport fit · 2026-10-22

The user wants the whole closed results container visible on arrival, with space below, regardless of desktop window height. The right event keeps natural document height and does not become a nested scrolling window.

## Correction

The prior `100svh - 48px` maximum did not account for the header and workspace top gap. At 1280 × 720, the list began at 116.67px and ended at 788.67px, 68.67px below the viewport.

The new CSS derives a shared header size from the existing control row, safe-area-aware padding and border. That size controls the desktop header and the results maximum together. Results subtract the header, 24px workspace gap and 24px bottom gap from `100dvh`. No JavaScript or device-specific height is introduced. The kit and component primitives are unchanged.

The result remains sticky with the existing 24px top inset. Its height stays stable while the header scrolls away, leaving more space below it in that state. Mobile/portrait layouts remain normal document flow. Even short desktop windows retain a bounded list.

## Browser evidence

- At 1280 × 720: list top 117px, bottom 696px, bottom gap exactly 24px.
- At desktop viewport heights 400, 600, 720, 900, 982 and 1080px: bottom gap exactly 24px in every case; no horizontal overflow.
- 1512 × 982 is an illustrative laptop viewport, not a claim about the browser chrome or configured scaling of any particular MacBook.
- Event detail width remains 706px at the default 1280px viewport. Right detail height remains over 2000px and its scrollTop stays zero while the main document scrolls.
- Keyboard End reaches the list's bottom (scrollTop 512px) without removing the closed frame. The subsequent event-details anchor moves document scroll to 720px; list scroll remains 512px, its top sticks at 24px and its bottom stays inside the viewport.
- A 390 × 844 standalone event still hides the results and uses normal document flow.
- Only Chromium was rendered here. No native Safari/Firefox/device claim is made.

Raw measurements: `viewport-fit-checks.json`, `viewport-fit-scroll-check.json`. Screenshots: `viewport-fit-before.png`, `viewport-fit-after.png`. Prior stylesheet: `before-viewport-fit/app.css`. The original portable 1.0.0 ZIP remains preserved; current source is packaged separately as 1.0.1.

Reference: MDN documents [dynamic viewport units](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length#dynamic_viewport_units) for sizing against browser interfaces as they expand or retract. The calculation still uses the kit's rem-based spacing and target sizes.
