# Loading without changing the interface

Tide 1.5.3 / events 2.0.3 keeps browser deliverables HTML/CSS only. This cleanup changes image encoding and local HTTP delivery, with the same layout, colors, type, content and native behaviors.

## Lossless kit assets

| Asset | Original PNG bytes | Served lossless WebP bytes |
| --- | ---: | ---: |
| Shared card texture | 1,178,092 | 625,044 |
| Kit printmaking photograph | 2,536,968 | 1,655,892 |
| Total | 3,715,060 | 2,280,936 |

Both derivatives were encoded once with Pillow using WebP `lossless=True, method=6`. Source and decoded derivative dimensions and RGBA bytes were compared exactly, including transparency. Neither original has a color profile requiring transfer. Original PNGs and their URLs remain available; canonical kit CSS/HTML now reference the derivatives. App photo assets remain unchanged.

`packages/tide/assets/lossless-images.json` records original/derivative SHA-256 hashes, dimensions, the decoded RGBA digest and byte limits. Normal checks verify those exact conversion artifacts and require no imaging dependency. Changing either asset requires regenerating the derivative, comparing decoded RGBA bytes again and updating the provenance record; the hash check alone does not decode a new image or prove a newly edited record correct. Retaining originals increases the archive's stored asset inventory while reducing bytes requested by the interface.

## Local preview HTTP contracts

`tools/serve.cjs` is a local Node development tool, never a browser dependency. HTML, CSS, JSON, Markdown and SVG responses of at least 512 bytes negotiate Brotli or gzip through `Accept-Encoding`; browsers without a supported encoding receive identity bytes. Brotli quality 4 avoids expensive maximum-quality compression during source iteration. PNG/WebP/JPEG/WOFF2 responses are not recompressed. Compressed responses declare `Vary: Accept-Encoding`.

Every successful file response has a content ETag for its actual encoded representation and `Last-Modified`. Conditional GET/HEAD requests return 304 when valid; ETag takes precedence over date validation. Changed content is read anew and changes its validator immediately. Editable documents, styles and images retain `Cache-Control: no-cache`, which permits caching but requires validation; fonts retain their one-day freshness policy. HEAD returns matching representation headers without a response body. No persistent response cache conceals source edits.

## Regression gates

`npm run check` runs real local HTTP tests covering decoded byte equality for both encodings, quality negotiation/refusal, identity responses, representation-specific and weak/list ETags, date validation and precedence, conditional binary/CSS requests, font freshness, HEAD and immediate edit invalidation.

`tools/performance-budgets.json` caps kit/app CSS raw and gzip bytes, font bytes, generated document gzip bytes and referenced image sizes. Larger lossless kit assets have explicit budgets. Checks cover CSS background references as well as HTML images, require intrinsic image dimensions, and require a compatible shared local font preload on kit-consuming documents. Existing zero-script checks remain. Budgets are review thresholds, not claims about measured rendering speed.

The localhost HTTP tests need permission to open a loopback socket; restricted execution environments must permit that check rather than silently skip it. Asset preparation uses Pillow only for one-time encoding/pixel verification; ordinary build/check/dev still need only Node and Python standard libraries.

## Verification scope

HTTP integration tests and generated checks cover byte and markup contracts. Browser inspection uses Chromium on Windows. Exact decoded image equality and unchanged CSS declarations protect appearance; screenshots do not measure intermittent paint timing. Firefox/Safari, throttled-network, physical-device and screen-reader checks remain deferred.

Observed on 2026-10-26: the running preview served the app homepage as 13,650 Brotli bytes versus 97,891 identity bytes, and the shared stylesheet as 12,813 versus 86,756 bytes. Both decoded exactly to the identity response and returned 304 when revalidated. Both new WebP endpoints remained uncompressed and returned 304 with matching validators. These are response-body sizes, excluding HTTP headers. Chromium retained the same desktop heading geometry and resolved the lossless texture with zero browser scripts.
