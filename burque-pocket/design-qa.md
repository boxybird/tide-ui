# Pocket Nights / Pocket Texture — design QA

final result: passed

## Target and evidence

- Selected source: `../research/concepts/pocket-nights/03-pocket-texture.png`.
- User-requested refinement: less information on mobile cards; full event listings must add substantial information. Refined visual source: `../research/concepts/pocket-nights/03-pocket-texture-refined.png` (1327 × 1185, two states).
- Browser implementation: http://127.0.0.1:4174/. In-app browser, actual rendered interface.
- Native comparison viewport: browser1400 ×1200; phone screen393 ×852 CSS px, scale1, captured393 ×852 PNG. Android checked at427 ×952 CSS px, with904px app viewport above48px runtime navigation region.
- `qa/comparison.png` places source and implementation together for list and opened workshop. Source panel aspect ratios preserved while scaled to393px width; generated mock has no OS chrome and is shorter than the actual phone. Its shorter vertical shape was not stretched into a false pixel match. Runtime status bar/safe area accounted for as intentional additional height.
- Rendered evidence: `qa/list.png`, `qa/detail.png`, `qa/story.png`, `qa/android-detail.png`. Source/implementation headings, metadata, photo crops, and controls are legible in the same comparison input, so no separate tiny-region enlargement was needed.

## Findings and comparison history

1. [P1, fixed] Phone wrapper could scroll programmatically during locator/focus navigation, revealing its parked keyboard below the viewport. Earlier comparison showed the photo/control content displaced upward and keyboard exposed. App-scoped `overflow:clip` prevents that wrapper scroll; protected runtime source files are intact. After reload and repeated open/close/scroll interactions, wrapper scrollTop remained0, the photo filled the viewport, controls and status bar stayed visible, and no parked keyboard appeared. Final evidence: `qa/detail.png` and revised `qa/comparison.png`.
2. No remaining actionable P0/P1/P2 findings after the fix and recapture.

## Required fidelity surfaces

- Typography: restrained system sans;24px summary titles,34px detail titles,13–15px summary data. Smaller category labels preserve the reference hierarchy. Inter is preferred with platform-system fallback. Windows rendering differs slightly from the generated mock; this is P3 font refinement, not a clipped or unreadable layout.
- Spacing: full-width square-edged cards,22px internal padding,8px separators, fixed safe-area header, no imagery or description on the cards. Full viewport photo followed by scrollable description and details. Native status/navigation bars and slightly taller native device account for intentional reference differences.
- Colors: graphite background, quiet dotted image texture, off-white titles, cool gray secondary text, muted apricot price/action. Text protected by dark image scrim. Controls have44px or larger targets and keyboard focus outlines.
- Images: separately generated candid-style workshop/concert/comedy photos, no UI baked into assets. Portrait object-fit crop fills every hero viewport. Generated dot texture used for cards. Radix outline icons, no handcrafted icon substitutes. Photo subjects and crops align with the selected direction; generated photos remain fictional.
- Copy: cards only show category/title/venue/date/time/price. Detail adds introductory description, lineup or included materials, timeline, admission/experience guidance and arrival information. Comedy category corrected from the initial mock's erroneous music label. Fake venue addresses omitted. All events and photo subjects disclosed as demo content. Details live below the immersive hero rather than repeating only the summary.

## Interaction verification

- Opened all three events; native document View Transition ready and finished, `data-transition-result=animated`. Shared surface/title/date/time/venue/price move between states.
- Close and browser Back animate back; Escape returns focus to source card. Closing after deep scrolling works. Source list remains mounted to preserve its scroll position. Hash detail reload resolves the correct event.
- Workshop scroll affordance reveals longer content and schedule. Actual browser scroll confirmed; content exists beyond the photo and remains reachable.
- Planning sheet, save, unsave, saved-only list and empty-state recovery exercised. Temporary test save removed afterward.
- Calendar action downloaded `ink-demo.ics`; inspected valid VCALENDAR/VEVENT, correct UTC6–8PM local workshop interval, fictional-event description, no reservation.
- `?motion=off` exercises immediate update path and Escape return. System prefers-reduced-motion uses the same path; OS preference itself was not changed.
- iPhone393px and Pixel427px variants checked; full hero equals app viewport, horizontal overflow false, runtime camera/status/navigation retained.
- Console reviewed: one earlier development HMR missing-module error while files were being written; no new runtime errors during final interaction passes after reload.
- TypeScript compile, production Vite build and Sites packaging preparation pass. Runtime integrity check passes28 protected files. No publish or upload performed.

## Implementation checklist

- [x] Simplified cards and richer listing.
- [x] Native bidirectional transition and immediate fallback.
- [x] Real generated photos, useful detail content, working saves and calendar demo.
- [x] Fix phone scrolling issue, recapture, compare.
- [x] Keep local server running and preview available.

## Follow-up polish / limits

- P3: choose and bundle a final brand font instead of relying on platform fallback.
- Device previews are browser simulations, not physical iOS/Safari or Android hardware tests. Native API fallback is provided; production media failure, very long submission content, and real checkout are outside this prototype.
