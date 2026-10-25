# Date Line — UI kit 0.1

Static HTML/CSS companion to the approved Date Line. No animation or browser JavaScript. This library turns the selected layout into reusable parts and explores the surrounding screens without choosing a new visual direction.

Open index.html or run `node server.cjs` and visit http://127.0.0.1:4182/. All assets and fonts are local. `build.py` regenerates the library and nine companion screens; run it from the workspace root. It does not regenerate the approved reference copies.

## What is included

- Foundations: exact Date Line palette, Manrope scales, 4px spacing base, texture usage, page insets and control proportions. tokens.json is a portable inventory, not a dependency.
- Components: primary/secondary/disabled actions, icon controls, visible focus, filter choices, fields/default/error/disabled, radio/checkbox controls, status badges, notices, feedback, organizer contact and a labelled sponsored placement.
- Nine new static compositions: search, filters, saved, empty saved, no results, event submission, review, pending-review confirmation and recovery/status examples.
- screen-map.json and the Coverage section distinguish preserved, designed and remaining flows. Next priorities are the attendance handoff and organizer editing/cancellation. Accounts and notifications are deferred design choices, not launch requirements.

## Preserve the reference

frames/01-list.html and frames/01-event.html are byte-identical to quiet-assembly's approved frames. screens.css, cards.css, themes.css and fonts.css are byte-identical copies. The reference frames do not load ui.css. The companion 01-date-line.html comparison page only updates its documentation navigation. No original collection is modified.

The app insets remain 24px. Ordinary event cards retain their exact anatomy. New form values use 16/24, body copy 14/24, form controls 48px, icon controls 44px. Borders on interactive fields use a stronger neutral than decorative card dividers. Status words communicate meaning alongside color.

## Static scope

These are design fixtures. Search/filter results and review content do not reflect edited values. Native inputs, radios, checkboxes, reset, HTML required-field validation and links work. Submission fields intentionally have no name attributes, so navigating to the fixed review page does not transmit entered field values. The received page is an example state; no event is sent, saved, reviewed or published and no email is sent. Photo selection is a native control example, with no upload or enforced file-size limit. The private-email note and pending-review language describe the intended product behavior.

Event content, organizer/address/contact information and photography are illustrative. The address is explicitly fictional. Links to hello@example.com and example.com are sample destinations. No booking or real organizer service is connected.

## Accessibility grounding

Visible labels and associated instructions follow [W3C's form-label guidance](https://www.w3.org/WAI/tutorials/forms/labels/). Status meaning is provided in text, consistent with [W3C's use-of-color guidance](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). The project's chosen 44/48px targets exceed the basic size described by [WCAG 2.2 target-size minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html); this is a design choice, not a claim that WCAG requires every control to be 44px. Native input internals and inline links have their own behavior. This is not a full accessibility conformance audit.

QA evidence lives in qa/ and design-qa.md. Licensed Manrope fonts and Radix icons reuse the existing project assets; source and licenses remain in assets/ and licenses/.
