# Date Line — In Practice

Date Line (Quiet Assembly 01) is the user's current favorite layout overall. Its original files remain unchanged. This collection adds two realistic conditions around that selected design:

1. **Local Partner** — a labelled ad between the second and third events, plus a labelled partner ad after the expanded event's introduction. The first event viewport remains unchanged.
2. **Rough Upload** — the original list, with an intentionally poor organizer photograph in the event opening. Foreground layout, type, controls, colors and spacing remain fixed. The image is deliberately not improved.

Open `index.html` for both pairs. `baseline.html` shows the preserved Date Line. Standalone frame HTML is in `frames/`. The original favorite is still in `../quiet-assembly/01-date-line.html`.

The app frame styles are exact copies of the approved styles. Additions live in `reality.css`; presentation-only changes live in `presentation.css`. `source/` holds the approved frame source. `baseline-lock.json` records source hashes. `node build.mjs` emits the standalone static documents using only Node built-ins.

All fonts, images and Radix icons are local. No package install, framework, browser JavaScript, tracking or real ad network is included. Ad links use a fictional local landing page. Workshop links, return links and detail scroll links work. Other cards and Saved/bookmarks remain visual-only, as in the approved prototype.

Optional local preview: `node server.cjs`, then http://127.0.0.1:4178/.

`assets/images/organizer-upload.png` is a newly generated 1024×1536 poor-photo fixture, produced by the built-in ImageGen tool. The exact prompt and provenance are in `assets/images/provenance.json`. It tests poor framing, lighting and focus, not a claimed low-resolution file size.

QA includes comparisons against the approved pixels, isolated ad-card crops, source hashes, foreground geometry, phone widths, contrast and link behavior. See `design-qa.md`. Large screenshots remain in the workspace `qa/` folder; reports and the preservation manifest are bundled in the archive.
