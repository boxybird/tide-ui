# Borderless event panes · 22 October 2026

App 1.3.1 / kit 1.2.1. The user explicitly rejects decorative border boxes around the results-list panel and individual-event pane on desktop, tablet and mobile.

`css/app.css` previously added desktop-only borders and 4px radii around results, detail and empty-preview surfaces. Those declarations and the detail’s rounded clipping shell are removed. No replacement ornament, component or override was added. Kit component CSS already supplied unframed list/event compositions; the rule is now explicit in `kit/docs/COMPONENTS.md` and the kit README.

## Browser verification

Actual surface: local in-app Chromium. [Measurements](browser-measurements.json) and [desktop result](after-desktop.png).

- At 1280 × 720, 1024 × 768, 834 × 1112, 390 × 844 and 1280 × 600, all three pane wrappers compute zero borders, zero radius and no outline. The empty-preview wrapper is normally hidden; its computed styling is also unframed.
- At desktop, the results pane retains its 390px width, internal native scrolling and 24px bottom gap. The 1280px detail width remains 706px and its document height is natural. Tablet portrait remains a single column.
- A standalone event at 390 × 844 has no outer border or radius. No checked viewport has horizontal page overflow.
- Card separators, the In view treatment, form/control boundaries and keyboard focus are unchanged. There are no HTML or script edits.

Before/after screenshot evidence is retained in this folder. `before.png` is historical; `after-desktop.png` is the inspected final result. Native Firefox and Safari were not run for this CSS correction.

## Preservation and source checks

[preservation.json](preservation.json) compares against the previous release archives: all shared kit CSS sources are byte-identical, and all 406 app HTML documents are byte-identical. Only the generated kit bundle’s version comment changes; no kit component style changed. The kit version records documentation of the composition rule.

Kit/app generated-output and structural/ownership checks pass, including the original 176-file foundation and frozen 263-file baseline. All 40 existing tests pass. Contrast still passes all 348 checks. App 1.3.0 and kit 1.2.0 archives remain preserved; new packages use their own versioned filenames.
