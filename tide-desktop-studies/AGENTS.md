# Wide Open · isolated desktop layout studies

The user explicitly freezes the maintained UI kit and current app for this exercise. Do not write to `../tide-responsive-app/` or `../tide-ui-kit/`, including docs, generated files, QA, archives or Python bytecode. `locks/kit-1.2.1.json` and `locks/app-1.3.1.json` record every existing file. Read the shared kit and app sources; run Python with `-B`.

These are app-composition studies, not kit extensions. Use Bumble Dark and the same 48 events. Keep Manrope, tokens, card/field/button/badge styles, neutral callouts and unframed event panes. No new kit component is needed. Composition belongs in `css/studies.css` under `tide.study`; review UI belongs in `css/review.css`. Use private BEM blocks `tide-study` and `tide-study-review`. Never redefine kit components or introduce raw colors/type scales.

Panorama is a wide master/detail composition. Workbench separates existing search/filter controls into a desktop tools column; the small adapter moves the original nodes only after the existing search script has initialized, restoring them below the desktop breakpoint. Open Book places the existing photo opening and details next to each other. Below 75rem, the approved mobile/tablet composition remains unchanged. Keep native controls, focus and all existing search/navigation behavior.

Serve locally on 127.0.0.1:4187. `/base/` is a read-only mount of the preserved app (or an exact packaged dependency snapshot); no new app/kit server modifications. Do not publish. Build/check with `python -B tools/build.py` and `python -B tools/check.py`. Test browser widths, scrolling, selection, search and responsive restoration; save evidence in this study only. No permissions or approval are needed for routine local iteration.
