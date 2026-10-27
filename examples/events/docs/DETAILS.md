# Individual event content and templates

All 54 event documents use `src/templates/document.html`, `workspace.html` and `event-detail.html`. Their native `<sample-id>.html` URLs are unchanged. `src/pages/` contains only three unique venue/help/submission content fragments; ten non-event routes are registered in `data/pages.json`. The app builder renders all 64 routes before emitting the default app and ten theme/mode examples. The browser receives HTML and CSS with no JavaScript.

## Content ownership

`data/events.json` is the canonical sample catalog. Existing card fields supply shared title, category, venue identity/label, date and price. Each record's `detail` object contains its document title, image metadata, subtitle, authored timestamps/range labels, admission note, cue, story label/title/lead and ordered sections. Times retain their original timezone offsets and display labels rather than being reconstructed from a browser or build-machine locale.

App 1.1.8 references app-owned WebP photos. The renderer keeps real event photos eager/high priority and preview photos lazy/normal priority, preserving authored dimensions and alt text. See [asset ownership and performance verification](PERFORMANCE.md).

Each section has a title, optional stable fragment ID and ordered blocks:

| Block | Data | Existing markup |
| --- | --- | --- |
| `paragraph` | Plain `text` | Paragraph |
| `place` | `lines` with text and optional `wrapped` flag | Existing Place paragraph, line breaks and optional span |
| `inclusions` | Plain-text `items` | Inclusions list with existing decorative check icons |
| `schedule` | Label/text pairs in `items` | Existing Schedule definition list |
| `attendance` | Plain-text `paragraphs` | Existing app attendance wrapper |
| `link` | `href` and plain `label` | Existing secondary venue action |

No raw HTML blocks are supported. Plain text, photo alternatives and quoted attributes are escaped. Links reject unsupported schemes and control characters; sample image references remain local. Unknown block types, invalid heading levels and unsupported image sources fail the build. A future content capability should have an explicit typed block and markup contract, rather than bypassing escaping.

`data/detail-presentations.json` preserves the two existing compositions. Full listings retain saved controls, age/year/duration notes, per-person label, richer sections and icon back link. Concise listings retain their focused title, separate start/end times, venue links and simpler controls. These are app structure defaults, not themes: kit colors, type, spacing and primitives remain unchanged.

## Rendering and navigation contracts

`tools/event_details.py` composes registered `detail-*.html` partials; `tools/template_engine.py` owns escaped values and includes. Existing inline SVG shapes and root attributes are retained in shared icon partials. `consumer-manifest.json` registers all template/data homes. Normal checks prevent restoring event hero/story markup in route sources, and the route registry rejects per-event source-document copies.

An individual event uses heading levels 1/2/3 for hero, story and sections. Index/search/saved previews reuse the same record at levels 2/3/4, preserving one page-level heading. Existing `event-detail`, `event-title`, `event-story`, `story-title`, `attendance` and venue fragment targets remain stable, including their original focus attributes.

List selection, scoped venue links, back links, photo modes, browser Back/refresh, smooth event selection and the original responsive filter controls remain owned by the existing browser runtime. Its behavior remains unchanged; current shared-service ownership is documented in [runtime contracts](RUNTIME.md). The venue guide and help/submission content stay in their unique non-event documents. All event entries remain authored samples; this refactor does not add live ingestion or booking.
