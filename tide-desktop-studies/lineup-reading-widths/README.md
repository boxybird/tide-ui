# Lineup · Reading Widths

Three additive desktop compositions of **Sliding Filters / Left**, using Bumble Dark and the same 48-event HTML. Left is still the selected favorite and is preserved byte for byte. The maintained app, kit and every preceding study remain read-only dependencies.

Review locally: [Reading Widths](http://127.0.0.1:4187/lineup-reading-widths/index.html). Open an individual version for normal browser testing. The existing `tide-desktop-studies/server.cjs` serves the study and its read-only `/base/` app mount.

## Compare

| Version | Closed desktop | Open filters | Photo treatment |
| --- | --- | --- | --- |
| Contained | Centered 76rem frame, equal columns | Filters and list divide the browsing half | Original photographed opening |
| Give & Take | Same 76rem frame, fixed 24.375rem list | An 18rem filter column takes space from the event | Original photographed opening |
| Reading Room | List plus event stop at 69.875rem | Frame grows toward 89.375rem, using outside margins before shrinking the event | Modest uncropped photo beside the introduction, stacked when the event is narrow |

All widths use the existing 16px root, 24px gutter, app list-width token and kit spacing roles. Track animation uses the preserved 440ms timing. In Give & Take and Reading Room, the outer browsing track and inner filter track grow by the same amount so list width stays stable during motion. The root size container makes `cqw` account for the document scrollbar, keeping outer margins symmetric. Sticky header geometry, independent bounded left scrollers, 48px bottom clearance, pinned Apply, natural event document scroll, month headings and existing selection/search behavior are retained.

Below 75rem, the filter adapter restores the original Lineup controls and geometry. Contained and Give & Take retain original tablet and mobile composition. Reading Room changes only its event photo composition at 60rem and above, using the event's own container width to decide between beside/stacked media. Below 60rem its wrapper uses `display: contents`, its caption is hidden, and the original mobile photo opening remains in place.

## Organizer images

The review-only selector shows the same **Ink After Dark** original, rough capture or no image across all versions. It never substitutes a workshop photo for unrelated events. Each variant remembers its sample choice for event navigation; `?photo=original`, `?photo=rough` and `?photo=none` override that for a direct link. The review sends a validated, same-origin message into each live frame, including lazy frames on load.

`assets/organizer-upload.png` is a byte-identical copy of the earlier illustrative organizer-upload fixture from `date-line-in-practice/assets/images/organizer-upload.png`. It is 1024 × 1536, poorly composed, softly focused and unevenly lit. This tests capture quality, **not a low-resolution file**. It was generated for the prior study; it is not a real attendee or organizer upload. Its prior provenance is recorded in `date-line-motion/assets/images/organizer-upload-provenance.json`.

Reading Room shows the entire image within a 14rem column and 20rem height limit. It does not improve the underlying photograph. [MDN's object-fit contract](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/object-fit) describes the containment/cropping distinction. Actual production asset selection must also account for display density and available source sizes; CSS width alone does not establish enough pixels. See [web.dev's responsive-image guidance](https://web.dev/learn/images/descriptive). No thumbnail pipeline, upload validation, sharpening or generated replacement photography is implied by this study.

No image leaves the same event metadata, actions and full-height introduction usable. Reading Room removes the empty photo slot. Original and rough photos share accessible descriptive alternatives; no-image removes the image from the accessibility tree.

## Ownership and extension

`reading-widths.css` is private composition in `tide.room-study`; new selectors use the `tide-room-study` BEM block. It does not change type, colors, radii, cards, fields, buttons, badges or any kit token. The media figure and its caption are private composition markup around the existing image. No kit component is proposed or registered in this experiment. A selected reusable pattern would need a separate adoption decision and its kit contracts before promotion.

`slide-adapter.js` is generated from the frozen Left adapter with only its session key namespaced to each variant. Focus return, inert collapsed filters, Escape, invalid-field opening, original node movement and breakpoint restoration remain inherited. `room.js` only selects the illustrative photo and enables layout transitions after mount. Existing app scripts retain all filtering and navigation responsibilities. There are no duplicate controls, routes to a service, or framework dependencies.

## Build and preservation

Run Python with `-B` to avoid writing bytecode into dependencies:

```text
python -B tools/build.py
python -B tools/check.py
python -B tools/package.py
```

The build emits 160 HTML files and one adapter. The source checker strips only declared private additions before comparing all 159 product documents against the preserved Left generator. It verifies references, markup, labels, BEM ownership, shared tokens, fixture identity and the complete archive/hash chain. QA evidence lives in this sibling's `qa/`. The archive is a source package requiring the adjacent preserved dependencies, rather than a standalone export.
