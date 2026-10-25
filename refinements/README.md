# Burque / Quiet Studies

Six static HTML/CSS refinements of Ink After Dark. The same event content and workshop photo are used throughout. Each study shows the event list and the opened event in two mobile frames.

## Open

The local preview is kept running at **http://127.0.0.1:4175/**.

`index.html` is the full comparison. The six numbered HTML pages show one pair at a time. `frames/` contains the twelve standalone mobile HTML screens. The reference is 390 × 844 px; the screens also adapt to narrower or wider phones. Detail frames scroll to the complete description, schedule, inclusions and practical details.

There is no browser JavaScript and no app framework. All fonts, images and icons are local. The visual bookmark marks and Saved label are static study content. The Ink After Dark card and detail links are ordinary HTML navigation.

## The six versions

1. **Soft Focus** — Manrope, balanced 24 px inset, warm apricot.
2. **Humanist** — Source Sans 3, larger optical text sizes, warm sand.
3. **Warm Editorial** — Newsreader titles with DM Sans information, warm ink.
4. **Open Form** — DM Sans, lighter weights, cool charcoal.
5. **Studio Notes** — IBM Plex Sans with Plex Mono labels, compact 20 px inset.
6. **Quiet Air** — Instrument Sans, 28 px inset, lighter typographic emphasis.

## Edit

- `screens.css`: common anatomy, spacing scale, reading hierarchy, photo treatment and focus styles.
- `themes.css`: the six semantic token sets.
- `fonts.css`: locally hosted font faces.
- `gallery.css`: the comparison canvas only.
- `design-notes.html`: rationale, decisions and comparison guidance.
- `licenses/`: open font licenses and Radix icon license.

No installation is needed to host the delivered files on a static web server. The optional local server uses Node only: run `node server.cjs` from this folder. Fonts are reliably served over HTTP; some browsers restrict local fonts when opening files through file://.

The working delivery is `quiet-studies.zip`. Its contents can be unzipped and served directly. Development-only font packages and generation/QA scripts are excluded from that archive.

## Evidence and limits

`design-qa.md` records browser review and remaining limits. `qa/` in the working folder contains screenshots at native 390 px width, full event captures, responsive metrics at 320/430 px, contrast calculations and validation results. The collection contains fictional events and generated illustrative photography. No booking, saving, or payment backend is present.

The original interactive prototypes in `../burque` and `../burque-pocket` remain unchanged.
