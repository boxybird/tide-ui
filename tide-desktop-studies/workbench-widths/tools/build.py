"""Reuse the preserved Workbench HTML; vary only its desktop grid tracks."""
from html import escape
import argparse
import importlib.util
import sys

sys.dont_write_bytecode = True
from preserve import ROOT, PARENT, preserve

spec = importlib.util.spec_from_file_location('wide_open', PARENT/'tools/build.py')
wide = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wide)

VARIANTS = [
    ('matched', 'Matched', 'Two equal columns. The event gets the rest.',
     'Search and filters match the existing event-list width: 352px on smaller desktops, 390px from 1440px. The individual event fills the remaining space.',
     'Existing list width × 2 · remaining width for the event'),
    ('half-split', 'Half Split', 'Half for finding. Half for the event.',
     'Search and filters share the browsing half equally with the event list. The individual event receives the other half. The proportions stay fluid as the browser grows.',
     '50% filters + event list · 50% individual event · central gutter excluded'),
    ('midpoint', 'Midpoint', 'A measured step between the two.',
     'The two left columns stay equal. Each uses the average of Matched’s fixed width and Half Split’s fluid width, giving a direct middle comparison at every desktop size.',
     'Halfway between Matched and Half Split at the selected width'),
]


def page(filename, slug, name):
    html = wide.study_page(filename, 'workbench', 'Workbench / '+name)
    html = html.replace('tide-study--workbench ', 'tide-study--workbench tide-study--'+slug+' ', 1)
    html = html.replace('../base/', '../../base/').replace('../css/studies.css', '../../css/studies.css').replace('../js/layout.js', '../../js/layout.js')
    return html.replace('</head>', '<link rel="stylesheet" href="../widths.css">\n</head>', 1)


def overview():
    sections = []
    for number, (slug, name, title, description, caption) in enumerate(VARIANTS, 1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title">
<header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{number:02d} / {name}</p><h2 id="{slug}-title">{escape(title)}</h2><p>{escape(description)}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {name}<span class="tide-sr-only"> in a new tab</span></a></header>
<figure class="tide-study-review__figure"><figcaption><span>{escape(caption)}</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html" title="Workbench {name}: live width comparison" loading="lazy"></iframe></div></figure>
</section>''')
    links = ''.join(f'<a class="tide-chip" href="#{slug}-title">{i:02d} · {name}</a>' for i,(slug,name,*_) in enumerate(VARIANTS,1))
    return f'''<!doctype html>
<html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Workbench · Width comparisons · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><script src="../js/review.js" defer></script></head>
<body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the comparisons</a>
<header class="tide-study-review__header"><div><p class="tide-eyebrow">Wide Open / Workbench / Width comparisons</p><h1>A little more room to find your evening.</h1><p>The same Workbench, with three ways to balance filters, the event list and the individual event.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Widths only</span><span class="tide-badge">Kit unchanged</span><span class="tide-badge">Original Workbench preserved</span></div></div><a class="tide-button tide-button--secondary" href="../workbench/index.html" target="_blank" rel="noopener">Open original Workbench<span class="tide-sr-only"> in a new tab</span></a></header>
<nav class="tide-study-review__jump" aria-label="Choose a width comparison">{links}</nav>
<div class="tide-study-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="1200,800">Small desktop · 1200 × 800</option><option value="1280,800">Laptop · 1280 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><p>These are working HTML previews. Search, filter, scroll and choose events. Open a comparison to use your browser’s actual width.</p></div>
<p class="tide-study-review__note">The same 24px gaps and outer insets apply to every version. Half Split gives the browsing pair, including its internal gap, the same width as the event. Changes begin at 1200px; the approved mobile and tablet layouts remain.</p>
<main id="studies">{''.join(sections)}</main>
<footer class="tide-study-review__footer"><p>Same components, spacing, type, colors, 48 events and scrolling behavior. Only column proportions change.</p><nav aria-label="Comparison documentation"><a class="tide-link" href="../index.html">Back to Wide Open</a><a class="tide-link" href="README.md">Layout rules and verification</a></nav></footer></body></html>'''


def outputs():
    return {'index.html':overview(), **{slug+'/'+filename:page(filename,slug,name)
            for slug,name,*_ in VARIANTS for filename in wide.base.PAGES}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    preserve()
    for name, html in outputs().items():
        target = ROOT/name
        if args.check:
            if not target.is_file() or target.read_text(encoding='utf-8') != html:
                raise ValueError('Stale width comparison: '+name)
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(html,encoding='utf-8',newline='\n')
    preserve()
    print(f'{len(outputs())} width-comparison HTML pages '+('verified.' if args.check else 'built.'))
