# Margin Reveal · Desktop filters · verification

2026-10-23; live local HTML in the ChatGPT in-app Chromium browser. Firefox/Safari were not separately runtime tested. The change is one standard desktop-only display rule; all interaction scripts are reused.

- At1440×900, the inner Filters summary has `display:none`, zero layout height and no accessible button matching “Filters”. The original details stays open, with all six original input nodes present. Header, browsing wrapper, list, event, rail and pinned dock geometry matches the selected Margin Reveal within0.1px. Only the redundant44px summary row is removed.
- At1200×600, the sidebar scrolls to its lower category options while Apply stays pinned at552px, matching the list bottom and48px viewport clearance. Root document scroll remains zero.
- Live resize to1024×768 and390×844 restores the visible native summary, with focus correctly returned to it when a focused desktop field would otherwise be hidden. Enter opens and closes it at both sizes. Date fields become available when open; the existing workshop draft remains checked and there is exactly one query input.
- Returning to1440px opens the desktop details and hides the inner summary again. Focus falls to the body rather than remaining on an invisible control. The sidebar's outer reveal interaction is unchanged.
- Query “Ink After Dark”, inclusive October24 dates and Workshops still submit through pinned Apply, returning one result. The summary stays hidden after the real GET navigation. Pinned Clear all restores48 results while date/category contents stay open.
- Source checks pass for54 HTML files,4446 local references and53 original component-document comparisons. There is no new JavaScript or kit component. Every preserved release passes its hash guard, including all73 selected Margin Reveal files, the maintained980-file app and180-file kit.

`browser-evidence.json` records these observations; `browser-check.json` records assertions. `desktop.png` shows the desktop sidebar without its redundant Filters row. The user preference record now names Margin Reveal as the preferred desktop layout. The original selected study and all earlier versions remain preserved.
