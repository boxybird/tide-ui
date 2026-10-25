# Lineup · Filter Spaces

Open <http://127.0.0.1:4187/lineup-filter-spaces/index.html>.

Three desktop interaction alternatives preserve the cleaner 40/60 list/detail composition without a permanent tools column or a control bar above both panes:

1. **Pocket** leaves search in the list header. Filters open a native, nonmodal popover over the list, with light dismiss, Escape and a visible Close action. The event stays available.
2. **Focus** uses one Search & filter action. A native modal dialog groups search, dates and categories. Escape or Close returns focus to the launcher. This prioritizes uninterrupted browsing between searches, at the cost of temporarily covering the event.
3. **Refine** replaces the left-hand list with the controls. Back to lineup or Escape restores the list's reading position. The right event stays visible and interactive. This prioritizes generous filter space without overlaying content, at the cost of temporarily hiding the results.

Only Apply or search submission changes results. Closing retains unapplied drafts for the next opening. Applied date/category counts stay on the launcher; dates, category names and query context remain visible in the list. Clear all restores the full 48-event feed. The same original GET form, IDs, inputs, explicit form associations and search/navigation helpers are retained. No cloned controls or second filter-state model is introduced.

At 1200px and above the header remains sticky, the list ends 48px above the viewport bottom and the right event scrolls in the document. Below that breakpoint the original Lineup composition, disclosure and control order return. Draft values persist across resizing. No outer border boxes are added to the two event panes. Only temporary popover/dialog surfaces have a neutral boundary.

This is a private interaction experiment, not a registered kit extension. Existing controls retain kit CSS. `filter-spaces.css` owns composition and the temporary editor shell using existing semantic/type/space tokens; `filter-spaces.js` owns open/close/focus, original-node relocation and responsive restoration. If a pattern is accepted, its behavior contract and all-theme specimens should be reviewed before any future kit adoption. The maintained kit and app remain frozen now.

The implementation uses the [native Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API) and [HTML dialog](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog). Unsupported native APIs leave the original controls available. No animation library, framework, service or publication is required.

Build and check this folder only, with Python `-B`:

```text
python -B tools/build.py
python -B tools/check.py
node --check filter-spaces.js
```

`tools/space_context.py` verifies the entire earlier preservation chain and the previous Control Bars release. Never run app/kit/parent generators. This source collection depends on the preserved sibling studies and adjacent app through the existing port4187 server's read-only `/base/` mount.

## Verification · 2026-10-23

All 160 generated documents pass markup/reference checks (12,364 local references). Removing only the declared private wrapper additions leaves 159 product documents identical to the preserved Lineup generator. JavaScript syntax passes. Hash guards verify 980 app files, 180 kit files, 185 original desktop-study files, 177 width-study files, 177 earlier refinement files, 182 Lineup files and 176 previous Control Bars files. No maintained kit component was added or modified.

In-app Chromium checks cover 1200 × 600, 1440 × 900 and 1920 × 1080. The two event panes start at y=117; the list ends 48px above the viewport bottom at each size. Temporary editors fit within the viewport, scroll internally when needed and retain a visible Apply action. The event remains natural document scrolling; at the document end the sticky header stays at y=0 and the list retains its full frame. The header's flat canvas paint closes the 24px gap beneath it during scrolling.

All three flows produce one workshop for November 1, zero results for a nonmatching query and all 48 events after clearing. Reversed dates show the existing inline error and native invalid focus without navigating. Escape dismisses each editor and returns focus to its launcher; reopening retains date drafts. Focus uses the browser's native modal dialog semantics; Pocket is deliberately nonmodal. This is not a complete accessibility certification.

The persistent list heading has its own measured height. Month jumps account for it: November's header settles at y=249 and the first title remains visible. Direct pointer activation of Refine restores the exact list offset (3066px) after closing. A locator-driven click initially scrolled the sticky launcher before dispatching the click; the direct pointer test distinguishes that automation effect from the actual flow.

At 1024 × 768 and 390 × 844, header, introduction, summary, first card and list dimensions match the preserved Lineup. Six original inputs remain; query/date drafts survive responsive restoration. Raw resize observations may include an existing small document reading offset after a native control was focused; document-relative geometry is unchanged. The native disclosure remains the narrow-screen control container.

`qa/` contains the raw observations and inspected screenshots for open/closed desktop states. Firefox and Safari were not physically run in this pass. The current native API references above informed the behavior choices; support guards retain the original form if an API is absent.

The versioned source archive is `dist/lineup-filter-spaces-1.0.0.zip`, with an internal manifest and adjacent SHA-256 checksum. It references the preserved dependencies and is not a standalone app package.
