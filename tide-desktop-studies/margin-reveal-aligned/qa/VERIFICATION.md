# Header alignment verification · 2026-10-24

Live local preview in the in-app Chromium browser. No Firefox/Safari run was performed; this change uses established logical padding/margin and outline-offset properties without introducing a new platform dependency.

| Desktop viewport | Header / heading / search / dates / Apply start | Before content start | List bottom |
| --- | --- | --- | --- |
| 1200 × 600 | 32px | 56px | 552px |
| 1440 × 900 | 32px | 56px | 852px |
| 1920 × 1080 | 48px | 72px | 1032px |
| 2560 × 1440 | 64px | 88px | 1392px |

At each width, list/event/rail/action-dock rectangles match the previous refinement within0.1px. Apply remains aligned to the list bottom with48px viewport clearance. Original right and block insets are preserved. Search input retains12px internal start padding; Apply retains20px. The whole sidebar was not shifted.

Baseline/new measurements match at1024px tablet and390px mobile for the event page, plus the visible mobile index/list form. Native Filters disclosure remains present below75rem. Source parity confirms all53 product HTML documents retain the original component markup after stripping the declared private hook, state keys and stylesheet references.

Keyboard Tab/Shift+Tab shows a complete inset focus outline at the newly flush query edge. Existing focus color and2px width remain unchanged. Before the local outline-offset adjustment, the scroll boundary visibly clipped the external ring's left edge; `focus.png` records the corrected state.

Applied query `Ink After Dark`, From/Through2026-10-24 and Workshops through the pinned action: one matching event. Clear all restores48. Closing/reopening the sidebar leaves the event rectangle unchanged. These are UI checks of the reused behavior; no script was added or edited.

`browser-check.json` contains measurements and assertions. `desktop.png` shows the overall aligned composition; `focus.png` shows keyboard focus. `source-check.json` records markup, references, ownership and complete dependency preservation.
