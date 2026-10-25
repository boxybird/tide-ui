# Design QA — Tide palette studies

final result: passed

Reviewed 2026-10-22 in the in-app browser. Source: the selected Tide UI kit at port4183. Output: Tide, Mist, Slate and Deep at port4184. Tide remains the favorite; no replacement palette selection is inferred.

## Requested changes and findings

No unresolved P0/P1/P2 findings. The deliberate changes are the removal of colored callout stripes, a paired light palette and two further dark palette variations. All four kits keep Tide's square corners and flat surfaces.

The selected Tide skin at port4183 was also corrected, as requested. Its previous stylesheet is saved in qa/tide-before.css. The generator now retains this correction when rebuilt. Other old kit appearances and the original Date Line frames are unchanged.

`qa/callouts-before-after.png` places the old and corrected Tide status screens together at native 390×844 pixels. Inspected the combined capture. The callouts have a uniform neutral outline on all sides; headings retain the existing status meaning. No new colored ornament or icon was introduced. `qa/stripe-removal.json`: identical text, no change in callout bounds or heading positions. Removed border width is compensated inside padding so the text and wrapping stay fixed.

## Controlled comparison

`qa/compare-search.png`, `compare-states.png`, `compare-01-event.png` and `compare-submit.png` place Tide and its three variants together in matching 390×844 CSS/image-pixel captures. Inspected source and implementations together. The changed palette is intentional; dimensions, structure and content are the comparison controls.

`qa/layout-390.json`: selected source plus four generated kits × eleven screen/state pages (55 views). `qa/invariance.json`: zero text or measured geometry/typography differences. `qa/fixture-lock.json`: all 44 frame bodies match the preserved source markup after asset-path normalization. All six inherited source stylesheets are byte-identical copies. Eleven screen/state pages and the Foundations / Components / Screens / Coverage inventory remain consistent.

Required fidelity review:

- Typography: Manrope, original sizes, weights, leading, tracking, hierarchy and wrapping. No font substitutions or new type treatment.
- Spacing/layout: original 24px insets, touching cards and 44/48px controls. Every kit retains Tide's 2px control corners / 4px documentation corners, with no new shadows. Callout geometry and text alignment preserved.
- Color/tokens: semantic roles for surface, text, accent/on-accent, selection, borders and status. Mist is a cool light counterpart; Slate reduces saturation; Deep lowers the blue surfaces and shifts the accent toward cyan. The plain callout boundary uses the neutral strong-border role, independent of status.
- Images/icons: same local font files, dot texture, Radix icon assets and event photograph. Photo crop, scrim and hero geometry unchanged. The photo opening keeps a readable dark contextual surface in light mode. Mist's ordinary icons are darkened; the photograph is not recolored.
- Copy/content: same dates, titles, venues, prices, forms, saved states, review/confirmation fixtures and coverage. Only kit names, palette documentation and comparison navigation labels vary.

## Checks

- 390px: 55 views with no horizontal overflow. Every measured callout has the same color and width on all four borders.
- 320px: 44 app/state pages plus four library views (48 total), with no horizontal overflow or unlabelled form controls. Callout borders remain uniform.
- Palette navigation retains selected #components and #screens sections. Mist checkbox selection and Reset preserve the existing native form behavior.
- Targeted color checks: Mist tertiary text on canvas 4.75:1, secondary 5.98:1, accent 5.62:1, button text 6.12:1 and field boundary 3.51:1. Status text on its badge surfaces is at least 5.38:1. The dark palettes have higher sampled text/boundary contrast. These are targeted token checks, not a full accessibility conformance claim.
- 52 HTML files and 996 local references checked; no missing local resources; zero browser scripts. Library and standalone-screen browser error logs were empty. Temporary viewport override reset.

## Limits

Desktop in-app browser verification only; no physical-device or screen-reader run. Native controls may differ by browser. Static fixtures do not perform live search, persistence, upload, submission or email delivery. No new product functionality, motion or publication was added. Colors can be swapped through palettes.json and generated semantic roles; geometry stays in the unchanged shared CSS.
