# Desktop composition · App 2.0.0

The entire app is native HTML/CSS with no browser scripts. At 75rem and above, authored filter/list/detail columns use CSS Grid/subgrid in 20/35/45 proportions after gaps, inside a centered 92rem maximum. The heading and controls start in their final column; no node moves during load.

`workspace-browse.html`, `workspace-results.html`, `filter-rail.html`, `filter-status.html` and `filter-actions.html` own the complete structure. The result summary is outside `.tide-app__feed-scroll`, which contains the complete isolated feed, empty state and footer. CSS grid rows reserve the summary naturally; month headings stick at the feed top without measuring its height. Native gutter reservation replaces JavaScript scrollbar measurement. Left panes remain bounded with a minimum 24px bottom clearance; the right document scrolls naturally.

Below 75rem, the same authored native panel/disclosures stay in the document. There is no scripted flyout or control movement. Native disclosures are available at every width, so a closed narrow-screen disclosure remains operable after widening. Saved keeps its separate layout; event details retain full-screen reading at phone widths.

The filter footer keeps the compact quiet Reset button on the left and the authored page event count on the right in two CSS grid tracks at every width. The button retains the shared hover/focus styling and native form reset; changing controls does not update the authored count. Longer count text can wrap inside its right track without moving below Reset.

Native links, browser history, controls and reset remain. Result matching and previews are authored build-time states as described in [runtime boundary](RUNTIME.md). The original JavaScript geometry/behavior compatibility requirements are superseded by the explicit zero-browser-JavaScript policy.

The earlier 1.2.2 script-free diagnostic proved the desktop grid and heading positions did not need scripts. App 2.0.0 extends that boundary to the entire app and reference specimens. Current checks scan every generated route/theme and canonical HTML for script dependencies. Browser evidence is Chromium on Windows; Firefox/Safari, devices and screen readers remain deferred.
