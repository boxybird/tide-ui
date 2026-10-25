# Contained · Width & Search

An additive comparison of the user's preferred **Reading Widths / Contained**. The current Contained, Left, all preceding studies, maintained app and UI kit are preserved. Local review: [Width & Search](http://127.0.0.1:4187/contained-widths-search/index.html).

## Comparison

Three maximum widths: **76rem / 1216px**, **80rem / 1280px**, **84rem / 1344px** at the unchanged 16px root. Each step adds 64px overall. The composition keeps equal list/event halves; opening filters splits the left half equally. At maximum width, each step adds 16px to each left column and 32px to the individual event. At small desktop widths, all frames fit the available space and may converge.

The review's search-position selector changes all three live frames independently of their maximum width: **Below / full width**, **Below / compact**, and **Beside / original**. This gives nine combinations without duplicating controls or changing the palette. Preview frames open with filters visible on load; standalone pages retain the original closed-by-default behavior and user-controlled reveal. The existing rough/original/no-image review selector is retained.

Only desktop (75rem and above) changes. Tablet/mobile retain Contained's original search layout and icon button. Below desktop, the original filter disclosure and node positions return. The header, bounded independent left scrollers, 48px bottom clearance, pinned Apply, natural right document scroll and unframed panes remain unchanged.

## Component ownership

No new kit primitive is needed: this composes the existing **Search line**, **Field** and **Button**. The below arrangements use the normal text-button variant, including its original control height, padding, font, radius, focus and color roles. The label is visible as “Search events”; its accessible name remains the existing “Search events”. The field's explicit label is retained. Enter submits the same GET form. Apply still submits the same complete query/date/category form, from its existing pinned dock.

`widths-search.css` uses private BEM block `tide-width-study`, layer `tide.width-study`. It changes only maximum composition width, search grid tracks/gap, label visibility and button alignment. It sets the previous study's private maximum-width variable, never a shared kit token. `search-layout.js` selects the existing `tide-button--icon` modifier for the inline/mobile arrangement and removes it for the existing normal text button. There is one real field and one real submit button; neither is cloned or replaced.

This remains a private layout candidate, documented here, while the arrangement is being compared. Promoting an accepted search-layout pattern would require its kit HTML/CSS/state/behavior contract, registration and all-theme specimens. The maintained kit remains untouched during this comparison.

## Behavior and fallback

`slide-adapter.js` is generated from the frozen Left helper with its own session namespace and an optional `preview-filters=open` initial-state hint used by the gallery. The gallery mounts open without programmatic focus changes or synthetic button activation; changing search arrangement does not reopen a manually closed panel. All original focus/keyboard/restoration behavior remains. `search-layout.js` remembers the selected arrangement per width within the browser tab and restores it across real event/search navigation. Direct links may use `?search-layout=below`, `compact`, or `inline`. Review messages require the same origin, the parent frame, a known type and an enumerated layout.

Without the optional layout script, the existing inline form remains usable. Without the slide helper, controls remain in the preserved native layout. Photo handling reuses the previous study's script and byte-identical fixture directly; no new media asset is generated. The original helper still owns GET search, inclusive dates, category combinations, clearing, scroll restoration and event navigation.

## Source and preservation

Use Python `-B`: `tools/build.py`, `tools/check.py`, then `tools/package.py`. The build emits 160 HTML documents and one namespaced adapter. All 159 product documents are compared with the preserved Contained generator after removing only declared private additions. Source checks cover labels, IDs, BEM, references, tokens and generated adapter parity.

The preservation guard extends the entire preceding chain with all **188 Reading Widths release files**. New QA and archives belong only to this sibling. The source package depends on the adjacent preserved studies and app, served by the existing port4187 server; no publication or service integration is introduced.
