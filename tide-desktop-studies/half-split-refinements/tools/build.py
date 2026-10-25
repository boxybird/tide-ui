"""Three isolated shell refinements, using the preserved Half Split generator."""
from html import escape
import argparse
import importlib.util
import sys

sys.dont_write_bytecode = True
from guard import ROOT, PARENT, WIDTHS, guard
sys.path.insert(0,str(WIDTHS/'tools'))
spec=importlib.util.spec_from_file_location('widths_source',WIDTHS/'tools/build.py')
widths=importlib.util.module_from_spec(spec);spec.loader.exec_module(widths)

VARIANTS=[
    ('steady-header','Steady Header','Keep the frame in place.',
     'The header stays visible while the event scrolls naturally. Both left panels stay at the same top and bottom offsets, including at the end of a long event.',
     'Sticky header · original filter scrolling'),
    ('pinned-apply','Pinned Apply','Keep the next action within reach.',
     'The same steady frame, with the original Apply filters and Clear all actions pinned to the bottom of the filter column. Filter options scroll above them.',
     'Sticky header · pinned Apply filters'),
    ('pinned-search','Pinned Search','Keep search close, too.',
     'Apply filters stays at the bottom. As you scroll the filter options, the original search field stays in sight at the top, ready to adjust the search without retracing your steps.',
     'Sticky header · pinned Apply filters · search stays visible'),
]


def baseline(filename,name):
    return widths.page(filename,'half-split','Half Split / '+name).replace('../widths.css','../../workbench-widths/widths.css')


def page(filename,slug,name):
    html=baseline(filename,name)
    html=html.replace('<html lang="en"','<html class="tide-shell-document" lang="en"',1)
    html=html.replace('<body class="','<body class="tide-shell tide-shell--'+slug+' ',1)
    html=html.replace('class="tide-app__search tide-stack"','class="tide-app__search tide-stack tide-shell__search"',1)
    extra='<link rel="stylesheet" href="../shell.css">\n'
    if slug!='steady-header' and 'id="event-search-form"' in html: extra+='<script src="../dock.js" defer></script>\n'
    return html.replace('</head>',extra+'</head>',1)


def overview():
    sections=[]
    for i,(slug,name,title,description,caption) in enumerate(VARIANTS,1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{i:02d} / {name}</p><h2 id="{slug}-title">{escape(title)}</h2><p>{escape(description)}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {name}<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>{escape(caption)}</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html" title="Half Split / {name}: live refinement" loading="lazy"></iframe></div></figure></section>''')
    links=''.join(f'<a class="tide-chip" href="#{slug}-title">{i:02d} · {name}</a>' for i,(slug,name,*_) in enumerate(VARIANTS,1))
    return f'''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Half Split · Keep your place · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><script src="../js/review.js" defer></script></head><body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the refinements</a>
<header class="tide-study-review__header"><div><p class="tide-eyebrow">Half Split / Three refinements</p><h1>Keep your place.</h1><p>Your preferred proportions, with a steadier frame and the controls close at hand.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Half Split preserved</span><span class="tide-badge">Same kit</span><span class="tide-badge">Natural event scrolling</span></div></div><a class="tide-button tide-button--secondary" href="../workbench-widths/half-split/index.html" target="_blank" rel="noopener">Open original Half Split<span class="tide-sr-only"> in a new tab</span></a></header>
<nav class="tide-study-review__jump" aria-label="Choose a refinement">{links}</nav><div class="tide-study-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="1200,800">Small desktop · 1200 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><p>Scroll the event in each live preview, then scroll the filter column. The Open links use your browser’s actual viewport.</p></div><p class="tide-study-review__note">All three keep the same Half Split widths and 24px gaps. Desktop refinements begin at 1200px. Mobile and tablet keep the approved layout.</p><main id="studies">{''.join(sections)}</main><footer class="tide-study-review__footer"><nav aria-label="Refinement documentation"><a class="tide-link" href="../workbench-widths/index.html">Width comparisons</a><a class="tide-link" href="README.md">Decisions and verification</a></nav></footer></body></html>'''


def outputs():
    return {'index.html':overview(),**{slug+'/'+f:page(f,slug,name) for slug,name,*_ in VARIANTS for f in widths.wide.base.PAGES}}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    guard()
    for name,html in outputs().items():
        target=ROOT/name
        if args.check:
            if not target.is_file() or target.read_text(encoding='utf-8')!=html:raise ValueError('Stale refinement: '+name)
        else:
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf-8',newline='\n')
    guard();print(f'{len(outputs())} refinement HTML pages '+('verified.' if args.check else 'built.'))
