# App JavaScript ownership

App 1.1.5 retains progressive enhancement of native HTML documents. The UI kit, app CSS, sample content and native URLs are unchanged. There is no framework, new router, wheel interception or content service. The existing first-result preview still fetches another local event document when needed.

## Execution and ownership

`consumer-manifest.json` registers all nine scripts in execution order. Every route loads search-core → app-runtime → optional venue-context → event-search → event-navigation → headings → filters → rail → preview, using classic deferred scripts. Saved/help/submission retain their omission of venue-context. No additional dependencies are required.

| Script | Responsibility |
| --- | --- |
| `search-core.js` / `TideSearch` | DOM-independent normalization, inclusive local date ranges, exact venue/category matching, canonical URL serialization and refinement count |
| `app-runtime.js` / `TideApp` | Shared breakpoint/reduced-motion queries, optional session storage, compatible key strings, applied/form state reads, destination URLs, event-count labels and primary-click predicate |
| `venue-context.js` | Exact venue context, visible labels, navigation and scoped recovery links |
| `event-search.js` | Applied controls and native validation, filtered cards/month counts, selected preview/placeholder, scoped back links and first-result preview readiness |
| `event-navigation.js` | Optional smooth return before a real event link, list/Back reading restoration, cancellation and the single month-jump handler |
| `headings.js` | Existing count/month label spans and measured month-heading height |
| `filters.js` | One original form/control set, draft counter, Show/Reset, responsive modal lifecycle/focus, visual viewport and occupied native scrollbar measurement |
| `rail.js` | Desktop control relocation, open/close/focus/session preference and measured permanent summary height |
| `preview.js` | Existing sample photo choices, inspection positioning and post-mount transition readiness; replaces the mixed `media.js` home |

The shared services do not own DOM rendering, component styles or a second applied-state store. Applied choices still come from the URL. Drafts still come from the original associated controls through native `FormData`. Session storage is an optional enhancement; denied storage must not prevent browsing. `TideSearch.refinementCount` counts the date range once plus selected categories, retaining the existing exclusion of venue context and text query from that badge count.

The five media queries retain their distinct thresholds: 75rem desktop/under-75rem drawer, 60rem split navigation, under-48rem phone launcher and the system reduced-motion preference. Consumers share cached MediaQueryList objects. Breakpoint listeners and original mount timing remain owned by the feature scripts.

## Calendar and navigation

Month jumps previously ran overlapping listeners in navigation and the desktop rail. Navigation now handles each jump once, preserving focus and cancellation of pending event selection. Tablet jumps retain their prior list offset. While the desktop rail is mounted, the permanent summary's measured height is subtracted. The calendar heading meets the same summary edge as before; no new hardcoded geometry is introduced.

Native link semantics remain: modified/middle clicks, downloads, other targets, foreign origins/directories and phone navigation bypass the enhancement. Reduced motion retains immediate event links. A pending smooth return remains interruptible by a new page-scroll gesture, keyboard input or month jump. Back restoration still waits for asynchronous preview height before restoring the document/list reading position.

## Compatibility that remains intentional

The accepted preview controls are active behavior, not dead code. `photo=original|rough|none`, `inspect`, and `preview-filters=open` retain their effects. Photo/inspection behavior now has an explicit `preview.js` home. The desktop rail still reads its existing startup override. The `tide:preview-ready` event continues to coordinate photo application and reading restoration.

Existing key strings are centralized in `TideApp.keys`: `tide:margin-filters:…`, `tide:reading-widths:photo:…`, `tide:event-navigation:…` and `tide:app-release-1.1.0:applied`. Existing per-theme `data-state-key` values remain unchanged. The parent message `tide:reading-widths:photo` is retained with the same origin/source/mode guards. Renaming these identifiers would silently reset accepted session/review behavior.

The fallback clear link still uses its established app CSS modifier; the JavaScript variable now describes that fallback role. The no-script native disclosure/submit markup remains. Desktop collapse, modal close motion, focus restoration, date errors, gutter measurement, Show events alignment, empty states and venue information are preserved.

## Checks and extension

Build checks require every script to have one registered source home. Node contracts parse all registered scripts, exercise search/state/URL/storage/media compatibility and native navigation guards, and prevent direct storage/breakpoint logic spreading back into feature scripts. Month-jump handling must not be duplicated in the rail again. Browser verification covers complete runtime behavior separately from these lightweight tests.

Keep a new app behavior in its feature owner; use the small shared services only where the same logic is needed by multiple owners. Reusable visual components still follow the kit adoption process. Do not put app JavaScript in the kit or remove working review hooks solely because their compatibility names mention an older study.
