"""Build independent HTML compositions using the locked app, without writing to it."""
from pathlib import Path
from html import escape
import argparse
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
from foundation import ROOT, APP, lock

sys.path.insert(0, str(APP/'tools'))
spec = importlib.util.spec_from_file_location('approved_tide_app', APP/'tools/build.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

STUDIES = [
    ('panorama', 'Panorama', 'A broader canvas, with a familiar rhythm.',
     'The existing list stays beside the event. The browser’s remaining width becomes a larger photo canvas, while written details keep a comfortable reading measure.',
     'Best for browsing with a strong visual preview.'),
    ('workbench', 'Workbench', 'Find, compare, then settle on an evening.',
     'Search and filters have their own column. The feed starts with results, so more events fit on screen. The event keeps its natural document height.',
     'Best for narrowing a busy calendar without losing your place.'),
    ('open-book', 'Open Book', 'The photograph and the story, together.',
     'The existing event opening and written details sit beside one another. Read the practical information immediately, with the event list still close at hand.',
     'Best for reading the event rather than scrolling past its opening.'),
]


def study_page(filename, slug, name):
    html = base.app_page(filename, 'bumble', 'dark', '../base/')
    html = html.replace('<title>', '<title>'+escape(name)+' · ', 1)
    html = html.replace('<body class="', f'<body class="tide-study tide-study--{slug} ', 1)
    classes = {'header':'header', 'workspace':'workspace', 'results':'results',
               'detail':'detail', 'site-footer':'footer'}
    for original, addition in classes.items():
        html = html.replace(f'class="tide-app__{original}"',
                            f'class="tide-app__{original} tide-study__{addition}"')
    html = html.replace('class="tide-event-hero"', 'class="tide-event-hero tide-study__opening"')
    html = html.replace('class="tide-event-details"', 'class="tide-event-details tide-study__story"')
    html = html.replace('class="tide-app__preview-state tide-empty"', 'class="tide-app__preview-state tide-empty tide-study__placeholder"')
    extra = '<link rel="stylesheet" href="../css/studies.css">\n'
    if slug == 'workbench' and 'id="event-search-form"' in html:
        html = html.replace('<main class="tide-app__workspace tide-study__workspace">',
            '<main class="tide-app__workspace tide-study__workspace"><aside class="tide-study__tools" aria-label="Search and filters" tabindex="0" hidden></aside>', 1)
        extra += '<script src="../js/layout.js" defer></script>\n'
    return html.replace('</head>', extra+'</head>', 1)


def overview():
    sections=[]
    for index, (slug, name, title, description, purpose) in enumerate(STUDIES, 1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title">
          <header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{index:02d} / {name}</p><h2 id="{slug}-title">{title}</h2><p>{description}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {name}<span class="tide-sr-only"> in a new tab</span></a></header>
          <figure class="tide-study-review__figure"><figcaption><span>{purpose}</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html" title="{name}: live desktop layout study" loading="lazy"></iframe></div></figure>
        </section>''')
    return f'''<!doctype html>
<html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Wide Open · Three desktop studies · Burque</title><link rel="stylesheet" href="base/kit/css/tide.css"><link rel="stylesheet" href="css/review.css"><script src="js/review.js" defer></script></head>
<body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the studies</a>
<header class="tide-study-review__header"><div><p class="tide-eyebrow">Wide Open / Desktop layout studies</p><h1>More room. Same kit.</h1><p>Three ways to use a wider browser, with the components you already chose. Bumble Dark throughout.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Kit 1.2.1 · locked</span><span class="tide-badge">App 1.3.1 · preserved</span><span class="tide-badge">No new kit components</span></div></div><a class="tide-button tide-button--secondary" href="base/bumble-dark/index.html" target="_blank" rel="noopener">Open the current version<span class="tide-sr-only"> in a new tab</span></a></header>
<nav class="tide-study-review__jump" aria-label="Choose a study"><a class="tide-chip" href="#panorama-title">01 · Panorama</a><a class="tide-chip" href="#workbench-title">02 · Workbench</a><a class="tide-chip" href="#open-book-title">03 · Open Book</a></nav>
<div class="tide-study-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="1280,800">Laptop · 1280 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><p>These are working pages: scroll, search, filter and open events inside each preview. The previews scale to this page; the “Open” links use your browser’s actual width.</p></div>
<p class="tide-study-review__note">Desktop changes begin at 1200px. Below that, the approved layout is unchanged. The original app and every kit file stay untouched.</p>
<main id="studies">{''.join(sections)}</main>
<footer class="tide-study-review__footer"><p>Composition studies only. Same 48 events, type, tokens, controls and unframed event surfaces. No React, new services or kit changes.</p><nav aria-label="Study documentation"><a class="tide-link" href="README.md">Decisions and ownership</a><a class="tide-link" href="qa/REPORT.md">Verification and preservation</a></nav></footer>
</body></html>'''


def outputs():
    out={'index.html':overview()}
    for slug, name, *_ in STUDIES:
        for filename in base.PAGES:
            out[f'{slug}/{filename}']=study_page(filename, slug, name)
    return out


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args=parser.parse_args()
    lock()
    stale=[]
    for relative, html in outputs().items():
        path=ROOT/relative
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=html: stale.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding='utf-8', newline='\n')
    if stale: raise SystemExit('Stale study HTML: '+', '.join(stale))
    lock()
    print(f'{len(outputs())} HTML pages '+('verified' if args.check else 'built')+'; approved app and complete kit unchanged.')
