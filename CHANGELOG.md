# Changelog

## Repository · Lineup application-kit home and audit · 2026-10-27

- Named the current application kit **Lineup**, layout family **option 1**, and moved its complete maintained sources from `examples/events/` to `application-kits/lineup/`. Preserved application version 2.0.4, all 64 native routes, `/events/` preview URLs and the generated `build/events/` home. Future application layouts get named sibling homes and independent versions; release history stays in tags/artifacts.
- Made the UI-kit/application-kit ownership boundary explicit in the index, starter, architecture, contributor and agent notes. Tide 1.10.0 remains the source of truth and its component sources/distribution are unchanged. Corrected the stale application dependency record from Tide 1.5.3 to 1.10.0. Two integration-test path references follow the move; no UI-kit API/version change.
- Updated build/check/package paths and documentation evidence copying. Verified byte parity for 73 application `src/` files, 704 generated application documents, 18 generated kit files and 323 reference-site files.
- Added the [current application audit](application-kits/lineup/docs/AUDIT.md): 20 inspected screenshots and 264 responsive/theme/event geometry cases. Recorded the Saved desktop grid defect, public/private class typography drift, hidden narrow-screen browse heading, venue scope/recovery gaps, historical titles and reuse opportunities. Layout repairs remain separate application work; testing limits are explicit.

## Tide kit 1.10.0 · 2026-10-27

- Completed ownership contracts for all 26 components, 26 supporting blocks and 13 compositions. Normal checks now reject missing ownership/recipe/behavior metadata, duplicate owners and fixtures omitting their registered block. Existing consumer geometry exceptions are constrained to documented property/value choices; grouped selectors cannot conceal type or spacing overrides.
- Normalized remaining organizer, sponsorship, fallback, photographic opening/details and extension-panel type and spacing. Named intentional optical values, aligned details with page-heading leading, and prevented generic paragraph/heading rules from changing named component text roles. Removed narrow-screen fact-gap and admission-type density changes.
- Added an explicit inline-padding variant for venue profiles nested in padded pages, preserving standalone/application defaults. Added all-theme normal/context/hidden specimens, ownership/type contracts and regression checks. Application sources/layouts and resolved palettes are unchanged.
- Kept existing byte budgets by removing ordinary comments, indentation and separator padding from generated combined CSS while preserving protected text, rule/value sequence and canonical source formatting. Recorded Chromium evidence and deferred engine/assistive-technology limits separately.

## Tide kit 1.9.0 · 2026-10-27

- Normalized card/category/metadata, date-block, calendar and result typography independently of surrounding context. Retained 24px card insets and fixed metadata gaps; suppressed legacy decorative metadata dividers to avoid orphan lines on wrapping. Date columns reserve font-relative space for single-/two-digit alignment. Removed the narrow-screen metadata-gap override.
- Added covering-link keyboard/active treatment, visible-card separators across hidden entries, wrapping result-order labels and an explicit sticky offset input. Preserved neutral preview markers, unframed panes and native link/action layers.
- Added canonical card/date/listing recipes, all-theme state specimens and regression checks. Registered card ownership with only existing consumer preview visibility/outline choices permitted. Application sources/layouts and resolved palettes are unchanged.

## Tide kit 1.8.0 · 2026-10-27

- Normalized badges to 12px/20px labels and messages to 14px/24px, with explicit type/case independent of reading context. Notices now have even 16px padding and 8px flow gaps; every notice state retains the same neutral border.
- Added reusable title/body/action slots, native feedback link states and wrapping toast actions. Toasts reserve a stable minimum action row; message-only specimens retain that shell. Empty-state titles are heading-level independent, with consistent 16px gaps and an explicit compact spacing option. Legacy markup remains supported.
- Added shared all-theme feedback specimens, ownership/behavior docs and portable/rendered regression checks. Generated combined CSS omits ordinary source comments while preserving strings, URLs, licenses and rule/value order, keeping existing byte budgets unchanged. Application sources/layouts and palette values are unchanged.

## Tide kit 1.7.1 · 2026-10-27

- Aligned fields and disclosures to a shared 48px regular box, 11px vertical / 16px horizontal padding and the same centered 18px source chevron. Field values retain 16px type; disclosure labels retain 14px type with a shared 24px line box.
- Replaced only collapsed native select chrome; browser menus, selection and keyboard behavior remain native. Added logical trailing space, muted disabled indicators and native listbox/size-one comparisons. Updated all-theme specimens, contracts and checks. Application sources/layouts remain unchanged.

## Tide kit 1.7.0 · 2026-10-27

- Normalized field values, labels, hints, legends and choice typography so reading contexts cannot alter control type. Retained 48px fields and 44px minimum choice targets; aligned chips, disclosure summaries and native file buttons with the compact action rhythm.
- Completed hover/active, checked, invalid and disabled precedence, including inherited fieldset disabling. Added interaction-based native invalid styling without marking untouched required fields invalid. Upload errors now use the same danger boundary as text fields; summaries retain neutral Notice borders.
- Restored disclosure indicators when no explicit icon is authored, using the existing distributed chevron. Added a shared all-theme form matrix, ownership/state contracts, portable regression checks and a read-only browser measurement probe. Application source/layout files are unchanged.

## Tide kit 1.6.0 · 2026-10-27

- Standardized regular button geometry and explicit Manrope typography across primary, secondary, quiet and trailing-arrow actions. Removed viewport density changes and geometry overrides from the legacy plan variant; event composition retains its action gap.
- Added explicit compact/spread options and regular legacy icon/photo sizes, with one 18px action glyph. Existing plan/icon/photo classes remain compatible; deprecated the display-only focus-sample alias.
- Completed hover, distinct active, native focus, authored pressed, disabled and combined-state presentation for button/icon/photo families. Added audited active color roles without changing existing palette roles or theme inputs.
- Added a shared all-theme button matrix, a state/ownership contract, portable regression guards and a development-only browser measurement probe. Reconciled native/static demonstration claims. Application layout and template sources are unchanged.

## Events example 2.0.4 · 2026-10-26

- Gave Saved separate intrinsic intro/summary rows and a bounded feed row, preventing a stretched or collapsed count row.
- Corrected native month fragments to align the selected month at the feed top and preserve the outer desktop reading position. Phone month targets have no leftover heading gap; no browser JavaScript is added.
- Restored the mobile/tablet filter drawer with native popover buttons and CSS entry/exit motion from the left, Close/Escape/outside-click dismissal, native focus return, reduced motion and a scrolling body above the pinned footer. No browser JavaScript is added.
- Kept one original form/control set and the permanent desktop filter column. An open drawer resized to desktop fits the reserved column through CSS anchors with a shared-geometry fallback. Added native invoker-target association checks and recorded browser coverage in the [drawer contract](application-kits/lineup/docs/FILTER-DRAWER.md).

## Tide kit 1.5.3 / Events example 2.0.3 · 2026-10-26

- Restored the compact native Reset button at the left of the events filter footer and the page event count at the right, using app-scoped CSS grid and shorter labels without browser JavaScript.
- Switched the shared card texture and kit printmaking photo to verified lossless WebP derivatives, saving 1,434,124 requested bytes with identical decoded pixels. Preserved PNG sources/URLs, image dimensions, styles and existing app photos.
- Added representation-specific ETags, Last-Modified, conditional GET/HEAD and negotiated Brotli/gzip to the local preview tool. Editable assets still revalidate; fonts keep one-day freshness. No browser JavaScript is added.
- Added HTTP integration tests, lossless conversion provenance, asset/document byte budgets, intrinsic image size checks and shared font-preload checks. Included the missing preload on the app review entry. See the loading/performance contract.

## Tide kit 1.5.2 / Events example 2.0.2 · 2026-10-26

- Changed the shared local Manrope face to `font-display: block`. Text waits for the font during the browser's bounded block period instead of immediately painting fallback text. Existing font preload/caching remain; no browser JavaScript or document-hiding gate is added. A font delayed beyond the browser's block period can still fall back and later swap.

## Events example 2.0.1 · 2026-10-26

- Preloaded the existing local 24.8 KB Manrope font before app stylesheets on every route and theme/mode. No CDN or browser script is involved; the preload and kit CSS share the same font URL.
- Changed the local preview server to keep WOFF2 fonts fresh for one day with content-based ETag revalidation. Editable HTML/CSS still revalidate on refresh. The existing `font-display: swap` remains so text stays readable if a font fails or is slow.

## Tide kit 1.5.1 / Events example 2.0.0 · 2026-10-26

- Enforced zero browser JavaScript across the kit, canonical specimens, reference site and events example. Removed all nine app scripts, the site demo script, executable HTML dependencies and obsolete modal/preview script partials. Node/Python remain development tooling only.
- Replaced browser-created heading spans with build-time HTML. The fixed results summary now sits outside the native scrolling feed; CSS handles sticky month headings, native gutter reservation and bounded panels without height observers or viewport scripts.
- Replaced scripted drawer behavior with native disclosures and reset controls. Added four authored category/empty result pages; removed live text/date matching, fetched previews, custom history/storage and photo-message hooks. Native event URLs and the 54 sample records remain. These behavior changes require the app major version.
- Removed demo-script references accidentally included in kit HTML specimens. Native validation, checkbox/radio state, file selection and authored error-summary presentation remain available. Checks reject browser script files and executable HTML/SVG hooks in deliverables.

## Events example 1.2.2 · 2026-10-26

- Removed desktop layout assembly from JavaScript. Shared HTML now authors the browse grid, filter panel, heading, original controls and footer in their permanent positions; CSS Grid/subgrid supplies the existing centered 20/35/45 layout immediately.
- Reduced `rail.js` to sticky-summary measurement and retained preview-parameter compatibility. Native scrollbar clearance remains measured; only the responsive drawer relocates controls below 75rem.
- Added placement and no-assembly regression contracts. Verified desktop headings and columns with all app scripts omitted, repeated refreshes and responsive filtering/cancellation; see the desktop-layout verification and its browser limits.

## Events example 1.2.1 · 2026-10-26

- Changed desktop column proportions to 20% filters, 35% event list and 45% detail, dividing available space after gaps inside the existing centered 92rem maximum. Matching browse and startup tracks retain alignment; tablet/mobile layouts are unchanged.

## Events example 1.2.0 · 2026-10-26

- Replaced the desktop margin-reveal layout with a centered three-column composition: permanent filters, bounded events list and naturally scrolling event/venue detail. The container caps at 92rem, with 16rem filters, a 390px list and a flexible right column.
- Removed desktop collapse/reveal behavior and its animated geometry. The same three tracks and header inset exist before mounting; the original form/control set still moves into the responsive drawer below 75rem.
- Preserved native routes, search/reset/validation, measured sticky/gutter clearance, Back restoration, photo/inspection hooks and saved-page composition. Historical rail keys remain available; stored collapsed preferences do not hide the permanent desktop column. See the example's desktop-layout contract and verification.

## Events example 1.1.9 · 2026-10-26

- Fixed the desktop startup grid reserving an empty first column and placing event details in an implicit third column before the filter rail mounted. Rail-bearing workspaces now start with the same centered two-pane geometry as the mounted layout, including wider breakpoints.
- Preserved saved-page composition, responsive controls, filter motion, native scrolling and runtime timing. Chromium comparison measured zero horizontal pane drift between startup and mounted layouts at five desktop widths; see the example's performance verification.

## Events example 1.1.8 · 2026-10-26

- Disabled the cross-document title-transition experiment, removing its opt-in, title names and snapshot styling after unrelated titles visibly overlapped event details.
- Switched event photos and the rough-upload preview to same-size WebP derivatives: four served images total 384 KB instead of 8.72 MB. Original PNG sources and the kit remain unchanged.
- Kept real event photos eager/high priority; made list/saved preview images lazy/normal priority. Filtered first-result HTML previews now wait for the existing split breakpoint and load once if a narrow window is widened.
- Recorded Back/filter-flash isolation and browser limits in the example's performance notes. Filter mounting, native navigation, reading restoration and existing panel animations are unchanged.

## Events example 1.1.7 · 2026-10-26

- Added a CSS-only native cross-document title transition experiment: stable event identities pair list titles with event detail headings and reverse on return. Preview headings and the detail route's duplicate list title are excluded.
- Kept motion in app composition, gated by reduced-motion preference and CSS feature support. Native URLs, nine runtime scripts, filters, focus and reading restoration are preserved. See the example's title-transition contract for verification and limits; Tide remains 1.5.0.

## Tide kit 1.5.0 / Events example 1.1.6 · 2026-10-26

- Added registered Venue profile/card, Site header and Form error summary compositions with shared CSS, native markup and behavior contracts. Adopted venue-profile rhythm in the existing example and removed duplicated app styles.
- Added seven all-theme specimens covering populated/empty venue schedules and directory items, linked multi-field validation, five event conditions, wrapping navigation and native control states.
- Added documentation-only demonstrations for validation/focus/reset, a pressed button and actual local file selection/replacement/removal with type/size feedback. The CSS package remains script-free; app runtime, native routes, sample data, themes and primitives are preserved.

## Tide kit 1.4.0 · 2026-10-26

- Replaced Bumble Light's broad yellow surfaces with warm paper, retained ink-blue actions and introduced localized pale-honey selections. Bumble Dark is unchanged.
- Added Slate, Grove and Iris, each with restrained neutral surfaces and separately tuned light/dark accents; retained Tide. Removed Summer Light and Summer Dark at the user's request, including their generated specimens; the extension entry now uses Tide Light.
- Documented source-grounded color design policy, role allocation, accessibility criteria and review limits. Updated the theme-authoring recipe to use a neutral canvas.
- Made event theme specimens and theme-count reporting follow the canonical registry. All ten maintained modes use the existing shared kit, markup and runtime.

## Repository scope · 2026-10-26

- Defined maintained deliverables as the UI kit, its documentation/best practices and example pages, with UI completion criteria and guidance for next-work recommendations.
- Replaced the reference-site product roadmap and screen map with an inventory of UI coverage. Removed service-operation milestones and eventual-service language from active guidance.
- Preserved sample content, venue-fact attribution, component APIs and example behavior.

## Events example 1.1.5 · 2026-10-25

- Consolidated app-only storage/media/state/URL/count helpers and refinement counting, preserving URL/form ownership, session keys and deferred execution.
- Removed the duplicate desktop month-jump listener; one navigation handler retains measured summary clearance, focus and pending-navigation cancellation.
- Replaced the mixed media helper with an explicit preview home for accepted photo/inspection hooks and readiness. Kept preview parameters, guarded parent messages, native links, filters, resize/Back behavior and all kit/style/content inputs unchanged.
- Registered and syntax-checked all runtime sources; added storage-denial, native-navigation, breakpoint, count/state and preview-message contracts plus responsive browser comparisons.

## Events example 1.1.4 · 2026-10-25

- Reviewed remaining venue/help/submission/saved/list sources and extracted one document shell, skip links, site footer, results/detail workspace and preview state. All 60 native routes remain; only three unique content fragments need authored page HTML.
- Extracted eleven standard submission fields into registered input/textarea/select/label/hint partials backed by sample definitions. Retained native validation/reset, bespoke upload/permission controls and the existing back icon.
- Preserved kit1.3.0, reference site, app CSS/browser runtime, all route-specific script/state/skip/filter differences and verbatim venue/help content. Added utility-page, field-escaping and native-control regression contracts, source guards and before/after evidence.

## Events example 1.1.3 · 2026-10-25

- Replaced 54 individual event source documents with shared event-page/detail templates, preserving every native route. Index/search/saved previews reuse the same detail content.
- Extended the canonical sample catalog to structured event details in `data/events.json`; registered existing full/concise presentation defaults, typed content blocks and shared inline icons. No raw event HTML is stored in data.
- Preserved kit1.3.0, app CSS/browser runtime, exact content/attributes, photo behavior, heading levels, fragment targets and venue/search navigation. Added detail rendering/escaping contracts and guards against duplicated event markup.

## Events example 1.1.2 · 2026-10-25

- Extracted shared build-time app header, filters/rail/dialog, lineup summary, month groups, event card and empty/footer markup. All 60 routes consume named partials; unique event and content-page details remain local.
- Added a canonical 54-card fixture and explicit non-event route contexts. All-events, Sunshine Theater and saved collections reuse the same card recipe and data.
- Preserved kit1.3.0, all app CSS/browser runtime, public markup/content, native URLs and selected/scoped states. Added escaping/include/route contracts and source checks against duplicated shared markup.

## Events example 1.1.1 · 2026-10-25

- Consolidated inherited app styles into five registered, ordered CSS modules and one generated app stylesheet. Removed inactive layout variants and study-era class aliases from all 60 authored pages and runtime helpers.
- Retained kit1.3.0 inputs, app content, native routes, scoped search, responsive controls, sticky geometry and existing session preferences. Simplified the single selected lineup heading helper.
- Added app selector/module ownership checks and recorded before/after responsive verification. Reference ZIP names now include the independently versioned example.

## Repository migration · 2026-10-25

- Established permanent `packages/tide/`, `site/` and `examples/events/` homes with one shared CSS distribution.
- Separated the kit compiler, reference-site builder and event example. Removed archive imports and machine-specific paths from normal checks.
- Moved generated theme copies, reports and release ZIPs to ignored build/artifact directories. Added root build/check/dev/package commands and contributor guidance.
- Preserved complete earlier studies at `design-history/2026-10-25`; the active branch contains maintained sources. Retained kit1.3.0/example1.1.0 component appearance and behavior.

## Tide kit 1.3.0

Shared Filter panel with scrolling body, pinned actions, documented draft/reset/apply behavior and six theme/mode specimens. Existing primitives and components retained.

## Events example 1.1.0

Approved responsive composition plus accepted sticky month-heading layering and scoped Sunshine Theater venue discovery. Fifty-four authored sample events; existing UI kit reused.
