# Half Split · steady desktop studies

Preserve the original app, kit, Wide Open collection and Workbench width studies. This sibling adds three isolated refinements to Half Split: Steady Header, Pinned Apply, Pinned Search. No kit component or primitive changes. Keep the exact half-split columns, 24px gaps and mobile/tablet fallback.

The header stays in normal flow and becomes sticky. A desktop body grid and semantic MAIN subgrid share the footer row, so the left panels remain fixed at the same viewport offsets through the very end of the right document. Do not put the event in a separate scroll container or use display:contents on landmarks. Existing components remain unframed.

Pinned Apply and Pinned Search move the original action row into a private bottom dock; all controls keep their native form association. Only the options area scrolls. Pinned Search also makes the original search form sticky within that area, with focus-safe scroll padding. Restore original nodes and focus below 75rem. App composition owns shell.css and dock.js; these are experiments, not kit additions.

Use Python -B with this folder's tools; never invoke parent/app/kit writers. Serve using the running port4187 server, at /half-split-refinements/index.html. Save evidence and source archives here only. Do not publish.
