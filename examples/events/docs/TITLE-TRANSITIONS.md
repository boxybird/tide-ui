# Event title transition experiment · paused

App 1.1.8 disables the cross-document title experiment introduced in 1.1.7. The app contains no `@view-transition` opt-in, title transition identities, snapshot overrides or replacement animation runtime. Native links remain in use. Responsive drawer and smooth-scroll behavior are separate; the current permanent desktop columns are described in the [desktop contract](DESKTOP-LAYOUT.md).

The initial experiment named all event-card titles. In Chromium, opening The Late Set visibly carried unrelated outgoing titles over the destination. Some history/filtered runs also skipped native transitions. The experiment did not establish a reliable motion contract and is not part of Tide 1.5.0.

The [performance cleanup and verification record](PERFORMANCE.md) covers image optimization, hidden preview loading and Back/filter-flash isolation. A future title experiment needs to establish a stable destination layout and a narrowly scoped set of shared elements before another visual evaluation. There is no active transition test to enable in the current app.
