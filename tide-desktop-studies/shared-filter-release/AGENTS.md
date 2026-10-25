# Shared filter release

This is the additive successor kit 1.3.0 and an independent consumer copy. The approved `../margin-reveal-unified-search/` prototype, `../../tide-responsive-app/` and original `../../tide-ui-kit/` are frozen dependencies. Do not write to them, including QA or Python bytecode.

Edit kit named CSS/templates/docs/manifest, then build. Preserve primitive and theme inputs. `kit/css/filter-panel.css` owns panel internals; app CSS owns placement, dimensions and responsive composition. Never restore the extracted private panel/status/count/footer styles. The kit stays HTML/CSS; host scripts own data and dialog lifecycle.

Run Python with `-B`. Run kit build --check, structural checks, tests, release check and browser behavior/geometry checks before packaging. Browser evidence must distinguish actual Chromium tests from deferred Firefox/Safari/device checks. Existing release archives are immutable.
