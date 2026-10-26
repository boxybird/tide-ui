# Page recipes · Tide 1.5.0

These recipes cover venue, event, navigation and form compositions. Reuse the existing primitives, semantic roles and native HTML. Composition CSS home: `css/page-patterns.css`; additive control states stay with their existing owners in `css/components.css`. Page recipes are bundled in `tide.components.extensions`. The registry records each reusable block and behavior boundary. Every specimen is generated from the same HTML in every registered theme and both modes.

The CSS package ships no browser JavaScript. `site/scripts/recipe-demos.js` in the repository provides local documentation demonstrations for form validation, a pressed button and file selection. It is outside the kit distribution and does not submit, upload or persist data. The events example retains its nine registered scripts.

## Venues

Specimens: `frames/venue.html`, `venue-empty.html` and `venues.html`.

`tide-venue-profile` supplies internal padding and section rhythm; `__header` supplies heading/intro rhythm. Compose it with Page intro, Summary, Button, Notice and ordinary sections. The Sunshine Theater example consumes these shared styles; its private stylesheet retains viewport placement, responsive transitions and measured fragment clearance. Do not transfer the example's split-pane geometry into the kit component.

Use a page H1 for the venue name, then a labelled article or section for practical information. Supply known address/contact information as real text and links. Separate confirmed facts from unknown access information. Event age limits, admission and times belong to the event. A real venue's source attribution remains authored content; these fictional kit specimens establish no venue facts.

`tide-venue-card` is an unframed directory item with a heading link, optional description, location and accurately worded schedule context. `__title` owns title typography. Keep other actions outside the heading link; a stretched whole-card link is unnecessary. Omit unavailable information rather than inventing it. A directory can reuse an ordinary list or labelled article sequence.

| Schedule condition | Wording and recovery |
| --- | --- |
| Venue has events | Show its event list using Event card and the existing feed recipe. |
| Venue has no upcoming entries | Say “No upcoming events listed”; retain the profile and offer other events. No reset action is needed. |
| Venue events exist but filters match none | Say “No events match these filters”; retain the profile and offer a scoped reset. Keep the venue context. |

## Form validation

Specimen: `frames/form-validation.html`. `tide-error-summary` composes with `tide-notice`; `__title` and `__list` supply the summary heading and linked errors. The neutral Notice border stays uniform. No error stripe or extra palette is needed.

1. Start with labelled native controls, applicable constraints and persistent hints. Do not mark untouched fields invalid. Keep native validation enabled until an enhancement is ready.
2. On an unsuccessful submit, preserve every value. Set `aria-invalid="true"` on failed controls; append their error IDs to `aria-describedby` alongside existing hint IDs. Do not replace useful hints.
3. Reveal any containing disclosure before moving focus. Populate summary links in field order, reveal the summary and focus it with `tabindex="-1"`. The heading names the summary. Do not combine this focus move with `role="alert"` or a duplicate summary announcement.
4. An error link focuses its actual field. Native fragment URLs remain useful; enhanced plain clicks may reveal and focus the target. Retain modified-link behavior.
5. After validation, update affected errors as values are corrected without moving focus or repeatedly announcing the entire summary. Remove invalid semantics when a field is valid. Hide the summary when no errors remain.
6. On successful validation, use one polite status message. Reset restores the specimen's initial values and clears error state, descriptions, summary and result text.

The demonstration opens Contact details by default so native validation can focus the email without JavaScript. If a consumer initially closes a disclosure, its enhancement must open it when a contained field becomes invalid. The demo checks native constraints only; operational validation is outside this project. Errors are associated through `aria-describedby`; they are not communicated through color alone.

## Event conditions

Specimen: `frames/event-states.html`. These are compositions of Event details, Summary, Badge, Notice, Button and Missing photo; they do not introduce competing event components.

| Condition | Facts and action |
| --- | --- |
| Cancelled | State cancellation prominently; retain the original date, venue and advertised price for recognition. Replace the attendance action with useful contact or alternative-event links. |
| Sold out | Keep date, venue and price, and explicitly state availability. Show a waitlist only when a real destination exists; otherwise offer other events. |
| Time changed | The current time is the main fact and the list time. Label the previous time as historical context; explain what changed. |
| Multi-day | Give the date span and each day's hours. Explain overnight closure and whether admission covers one session or the span. Use valid `time` values and explicit local-time wording. |
| No photo | Keep the title, facts and next action. Reuse Fallback; do not add an unrelated image, an empty image tag or a second H1. |

The specimens use H2 for each event within a page that has one H1. On a standalone event page, use an H1 for that event; class-based typography remains the same. Status badges are text, not controls. A static notice is not automatically an alert. All five conditions remain legible without an image or status hue.

## Navigation

Specimen: `frames/navigation.html`; the venue specimens reuse the header. `tide-site-header` contains a Brand link and native `nav`/`ul`/`li`/`a` markup. `__links` supplies wrapping layout; `__link` supplies the target, underline and current-page appearance.

Use one accurately named main navigation landmark. Mark only the link to the actual current page with `aria-current="page"`. A venue detail page does not mark the directory as the current page. Give footer navigation a distinct label such as “Related pages”. Pair the header with Skip link and a focusable main target.

Links wrap on narrow screens and with larger text; do not hide destinations, clip labels or force a fixed header height. The header remains in document flow. Browser link behavior, Tab order and focus remain native. There are no menu roles or arrow-key requirements. This recipe does not introduce a menu, breadcrumbs or a site-wide router.

## Control states

Specimen: `frames/control-states.html`.

| Control | Supported demonstration |
| --- | --- |
| Text field | Editable, native read-only, disabled, and invalid with both hint and error. Read-only values can be focused/copied; disabled controls are unavailable and omitted from submission. |
| Select | Normal and disabled. Native select has no read-only state. |
| Checkbox/radio | Checked/unchecked, disabled checked/unchecked, native keyboard selection. Do not apply simulated selected classes to native inputs. |
| Button | Enabled/disabled and `aria-pressed` toggle. The toggle keeps a stable accessible name; its state and visible pressed treatment update together. |
| Date/time | Native controls with local-date/time wording. Picker chrome follows the browser; no custom calendar is introduced. |
| File input | Native chooser, actual local selection/replacement, removal, disabled, and explicit rejected type/size feedback. Preserve the chooser and associate the error with it. |

The file demo accepts JPEG, PNG and WebP up to 10 MiB (labelled 10 MB). It reads the browser-provided type and size only; it does not validate file contents. A rejected selection remains available for replacement or removal and never appears accepted. Filenames enter the DOM through text content. Nothing is uploaded, and no fake preselected filename is placed in an input. Without scripts, the ordinary native chooser remains usable and its accept list remains a browser hint.

## Verification

Run `npm run build` and `npm run check` from the root. Check every registered theme in both modes, keyboard and focus, 320px/phone/desktop widths, enlarged text, long labels, invalid/corrected/reset forms and selected/replaced/rejected files. The documentation demo is syntax-checked as a registered site script. Actual observations and limits are in the [coverage verification record](../../../docs/ui-pages/VERIFICATION.md); source checks alone do not establish screen-reader behavior.
