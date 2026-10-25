# Burque app release 1.1.0

A separate successor combining the approved Shared Filters consumer 1.0.0, the accepted sticky-heading correction and the accepted Sunshine Theater venue journey. This is a local release for review, not a replacement approval or a live-data launch.

Open `http://127.0.0.1:4187/app-release-1.1.0/index.html` for the review or `app/index.html?preview-filters=open` for Bumble Dark. The existing local server requires an explicit filename. All three themes have complete light/dark app routes under `themes/` and share one runtime and one page source. Native relative event links keep navigation in the chosen mode.

## Included

- All 48 baseline authored samples plus the six fictional Sunshine Theater shows, across October and November 2026. No pressure-test fixture expansion or recovery compositions were imported.
- Existing Margin Reveal desktop geometry, native scrollbars, measured bottom clearance, aligned Show events, bounded left panes and natural right document scroll. Tablet/phone retain the approved flyout, native controls and separate event destination.
- The complete feed is isolated beneath the permanent desktop lineup summary. Month headings retain native sticky push-off and responsive measured offsets.
- Linked venue name and More events action; Sunshine Theater identity, visitor guide and six-event schedule; exact venue scope through query/date/category filters, Reset, apply, refresh and return navigation. All events explicitly exits the venue.
- Existing help/prose, saved and submission sample destinations. These remain demonstrations, without persistence, accounts, submission services or booking.

## Source and build

Run from this directory, using Python with `-B`:

```text
python -B tools/build.py
python -B tools/build.py --check
python -B tools/check.py
node tools/test-search.cjs
python -B tools/package.py
```

`src/pages/` contains the accepted static HTML, imported losslessly from the preserved venue study apart from private-owner/session-key naming and study wording. `src/runtime/` owns the copied host JS/CSS/assets. Edit these sources, then build; never edit generated `app/`, `themes/` or `runtime/` directly. These are intentional full HTML destinations, not a CMS template engine. `data/` retains fixture provenance; changing JSON alone does not regenerate authored HTML. The one-time import tool refuses to overwrite existing sources and is not part of normal builds.

The live dependency is the **unchanged** sibling `../shared-filter-release/kit/`, version 1.3.0. No kit files or registries are edited or forked here. The archive includes an exact read-only dependency snapshot in that same relative position so it can be served independently. Unzip into a new folder, serve that folder with a local static HTTP server, then open `app-release-1.1.0/index.html`. Preservation checks require the original workspace references; serving the packaged app does not. Source/preservation checks read frozen references without running their writers. The versioned ZIP is immutable: changed content requires a new version rather than overwriting it.

See [ownership](docs/COMPONENT-OWNERSHIP.md), [venue data provenance](docs/SAMPLE-DATA.md), [verification](qa/VERIFICATION.md) and [machine checks](qa/checks.json). Firefox/Safari and physical-device/screen-reader checks remain deferred, not passed.
