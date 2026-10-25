# Margin Reveal · Header alignment

[Open the prototype](http://127.0.0.1:4187/margin-reveal-aligned/demo/black-ink-bright-paper.html?preview-filters=open) · [Viewport review](http://127.0.0.1:4187/margin-reveal-aligned/index.html) · [Preserved previous refinement](http://127.0.0.1:4187/margin-reveal-refined/demo/black-ink-bright-paper.html)

The header gutter already positions the revealed rail correctly. Each section previously added another24px start inset. This desktop-only refinement makes the composition own that outer alignment. It removes the redundant inline-start padding from the intro, search, context row and pinned action wrapper, and the equivalent start margin from the native filter wrapper. One grouped rule governs the padded wrappers; one handles the margin-based wrapper. Existing end and block insets remain intact.

Fields, search buttons, choices and Apply keep their internal component padding. No global token is overridden. There is no negative alignment margin, transform, duplicated control, new script or kit change. The title, form borders, fieldset legends and Apply button border share the header wordmark's start line; text inside a control retains its intentional internal inset.

Because controls now meet a scrolling/clipping boundary, the local composition draws the existing keyboard focus outline inside the control using the kit's focus-width token. Its color and width stay unchanged; all four edges remain visible. This focus offset is unrelated to geometric alignment and is also desktop-only.

The rule is active only for a mounted desktop sidebar at75rem and above. Below that breakpoint, or without JavaScript, the original layout and native disclosure remain unchanged. The existing header gutter is32px on ordinary desktops and grows to48/64px on larger widths; this refinement follows that gutter automatically rather than hard-coding32px again.

The right event and results geometry, original76rem constraint, reveal motion, bounded scrolling, bottom48px clearance and pinned Apply behavior are retained. The previous refinement and entire dependency chain are hash-verified before and after each local build/check/package. This is app layout ownership, so no new UI kit component is introduced.

Use Python `-B tools/build.py`, `-B tools/check.py`, then `-B tools/package.py` from this folder. Dependencies remain read-only. Browser evidence lives in `qa/`; immutable release files live in `dist/`.
