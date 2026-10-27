# Page recipes · Tide 1.10.0

The kit and canonical specimens use only HTML/CSS and native browser behavior. There are no script imports, event handlers or required browser modules. Shared composition CSS lives in `css/page-patterns.css`; component states remain with their existing owners. All registered specimens are generated in every theme and both modes. See [browser policy](BROWSER-POLICY.md).

## Venues

`tide-venue-profile` owns internal padding and section/header rhythm, composed with Page intro, Summary, Button, Notice and ordinary sections. The app owns viewport placement and responsive layout. `tide-venue-card` is an unframed directory item with a real heading link and separate secondary actions. Known venue facts and attribution remain authored; event age/admission conditions do not become blanket venue facts.

Inside a page that already supplies inline padding, explicitly add `tide-venue-profile--flush-inline`. It removes only the profile's inline padding, retaining 24px block padding and section/header rhythm. The populated and empty venue specimens use this variant to align profile information with the following schedule. Standalone/default profiles and application layout sources are unchanged. See [closeout type/spacing](KIT-CLOSEOUT.md) and [ownership](OWNERSHIP.md).

A populated venue shows sample events. A venue with no entries retains its information and an explicit empty state. An authored filtered-empty state explains recovery without hiding useful venue information. The kit supplies presentation and semantics, not matching or sourcing.

## Form validation

The current [form control contract](FORMS.md) and `frames/form-states.html` matrix cover shared typography/geometry, native and authored invalid states, disabled precedence, linked summaries and file/reset behavior in all ten modes. The earlier `form-validation.html` remains a native usage example; its contact disclosure now receives the shared fallback chevron when no explicit icon is authored.

Use associated labels, supported native input types, required constraints and visible hints. The form specimen uses ordinary native submission and reset. A successful submission reloads its static local page; no service receives or stores a listing.

`tide-error-summary` supplies a labelled section, title, list and native links to fields. The visible summary in the specimen is explicitly an authored appearance example, separate from browser validation. CSS does not compute error lists, mutate `aria-invalid`, announce changing validation results or enforce cross-field date relationships. Render a real summary as part of a consuming native/server response when appropriate.

Keep contact disclosure open when required fields live inside it, so native validation can reach them. Use document-appropriate heading levels and unique IDs. Do not mark every static summary as an urgent alert.

## Event conditions

Use existing hero/details, Notice, Badge and button/link recipes for populated, free, sold-out, cancelled and changed-time specimens. States are authored content. Unavailable actions are disabled or omitted; useful event and venue facts remain visible. Native links keep their real destinations and expected modified-click/history behavior.

## Navigation

`tide-site-header` composes Brand and ordinary navigation links. Use `aria-current` only for the actual current page. Links wrap at narrow widths and enlarged text. This recipe introduces no menu widget, arrow-key controller or router.

## Control states

Readonly text remains focusable/selectable. Disabled native controls are unavailable and omitted from submission. Selection uses native radio/checkbox state; the save-state example is a checkbox and does not imply persistence. Static reviewed-error fields are labelled authored fixtures.

The file specimen uses the native chooser, filename display and replacement behavior. `accept` is a chooser hint. It does not enforce custom file size/content checks, preview an image or upload anything. The consuming application must handle any operational validation outside this kit. Browser-native reset works for controls associated with a form.

## Verification

Run the root build/check commands. Checks reject executable dependencies in canonical kit HTML and browser output, including script files/imports, inline handlers and JavaScript URLs. Native validation and checkbox/file state replace the former site-only demonstrations. Current browser observations cover Chromium on Windows; Firefox/Safari, physical devices and screen readers remain deferred.
