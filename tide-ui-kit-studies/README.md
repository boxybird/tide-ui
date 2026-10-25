# Tide — palette studies

Tide is the user's current favorite UI kit appearance. These four complete static kits keep its square edges, flat surfaces and exact component/screen inventory:

- Tide: the selected teal/navy palette, with the requested callout stripe removal.
- Mist: cool light mode, with a darker teal action color for readable light surfaces.
- Slate: a quieter charcoal and blue-gray palette.
- Deep: darker blue surfaces with a clearer cyan accent.

Run `node server.cjs`, then open http://127.0.0.1:4184/. Or open index.html directly. Use the sidebar to change palettes while retaining the selected section. All images, icons and fonts are local. No browser JavaScript or animation was added.

## Semantic colors

Edit palettes.json and run `python build.py` from this folder (or run the script from the workspace root). The same source produces every kit. theme_engine.py translates palette values into shared roles; components consume those roles through the existing style contracts.

Examples of the actual CSS variables:

| Role | CSS name |
| --- | --- |
| Page canvas | --color-surface-canvas |
| Event/panel surface | --color-surface-card |
| Input surface | --color-surface-field |
| Main text | --color-text-primary |
| Supporting text | --color-text-secondary |
| Primary accent | --color-accent |
| Text on an accent | --color-on-accent |
| Success / warning / danger text | --color-status-success / --color-status-warning / --color-status-danger |

Status surface and border roles are also defined for the existing badges. A palette swap does not change the component HTML, type sizes, spacing or geometry. tokens.json in each kit records the roles and fixed structural values.

## Callouts

Announcements, recovery messages, cancellation notices and documentation callouts now use a uniform neutral 1px outline. There is no colored left-hand stripe or replacement side marker. Existing headings state the meaning. The removed border width is compensated inside the existing padding so text alignment, line wrapping and component dimensions stay fixed. The same correction was applied to the existing Tide skin at port4183; its earlier stylesheet is saved in qa/tide-before.css.

## Fixed comparison

All four kits have the same Foundations / Components / Screens / Coverage presentation, eleven screen/state pages, content, Manrope family, type scale, 24px insets, touching cards and 44/48px controls. All corners remain Tide's 2px controls / 4px documentation panels. No elevation variants in this round. The photographed opening remains a distinct dark reading surface even in Mist; the event details below it use the selected palette.

These are static design fixtures. Native controls, reset, required-field validation and ordinary navigation work. Filtering, saving, uploads, submissions and confirmation content are not live services; nothing is sent, stored or published. The original disclosure and fictional sample details remain in the screens. Asset provenance and licenses are retained in assets/ and licenses/.

See design-qa.md and qa/ for source comparisons, layout/content invariance and targeted contrast checks.
