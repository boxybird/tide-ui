"""List-heading variations on the preserved Pinned Apply shell."""
from html import escape
import argparse
import importlib.util
import sys

sys.dont_write_bytecode=True
from context import ROOT,PARENT,REFINEMENTS,verify
spec=importlib.util.spec_from_file_location('steady_source',REFINEMENTS/'tools/build.py')
steady=importlib.util.module_from_spec(spec);spec.loader.exec_module(steady)

VARIANTS=[
 ('lineup','Lineup','Give the results a clear heading.','The overall event count leads the column. Month headings stay quieter and the list opens without a framing rule.','Result count first · quieter month headings'),
 ('calendar','Calendar','Let the calendar lead.','The month and year become the main anchor, paired with the existing count badge. Overall results and ordering become supporting information.','Month first · existing neutral count badge'),
 ('month-index','Month Index','A stronger marker for each month.','A compact month number echoes Date Line’s prominent dates. The year, count and month jumps stay close, and the same treatment repeats as the feed enters November.','Numeric month index · clear month-to-month rhythm'),
]
CLASSES={
 'tide-app__results tide-study__results':'tide-feed-study__results',
 'tide-results':'tide-feed-study__summary','tide-results__count':'tide-feed-study__total','tide-results__order':'tide-feed-study__order',
 'tide-event-group__header':'tide-feed-study__month-header','tide-event-group__title':'tide-feed-study__month-title',
 'tide-event-group__count':'tide-feed-study__month-count','tide-event-group__nav':'tide-feed-study__month-nav',
}
LINEUP_CLASSES={
 'tide-page-intro tide-app__intro':'tide-feed-study__heading',
 'tide-page-intro__title':'tide-feed-study__heading-title',
 'tide-results tide-feed-study__summary':'tide-feed-study__heading',
 'tide-results__count tide-feed-study__total':'tide-feed-study__heading-title',
}
LINEUP_KICKER='<p class="tide-eyebrow tide-feed-study__kicker">The lineup</p>'


def baseline(filename,name):
    return steady.page(filename,'pinned-apply',name).replace('../shell.css','../../half-split-refinements/shell.css').replace('../dock.js','../../half-split-refinements/dock.js')


def page(filename,slug,name):
    html=baseline(filename,name).replace('<body class="','<body data-feed-study="'+slug+'" class="tide-feed-study tide-feed-study--'+slug+' ',1)
    for original,addition in CLASSES.items():html=html.replace('class="'+original+'"','class="'+original+' '+addition+'"')
    if slug=='lineup':
        for original,addition in LINEUP_CLASSES.items():html=html.replace('class="'+original+'"','class="'+original+' '+addition+'"')
        if 'id="event-search-form"' in html:html=html.replace('<h2 class="tide-results__count',LINEUP_KICKER+'<h2 class="tide-results__count',1)
    extra='<link rel="stylesheet" href="../list-rhythm.css">\n'
    if 'id="event-search-form"' in html:extra+='<script src="../headings.js" defer></script>\n'
    return html.replace('</head>',extra+'</head>',1)


def overview():
    sections=[]
    for i,(slug,name,title,description,caption) in enumerate(VARIANTS,1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{i:02d} / {name}</p><h2 id="{slug}-title">{escape(title)}</h2><p>{escape(description)}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {name}<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>{escape(caption)}</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html" title="List Rhythm / {name}: live desktop study" loading="lazy"></iframe></div></figure></section>''')
    links=''.join(f'<a class="tide-chip" href="#{slug}-title">{i:02d} · {name}</a>' for i,(slug,name,*_) in enumerate(VARIANTS,1))
    return f'''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Half Split · List Rhythm · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><script src="../js/review.js" defer></script></head><body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the studies</a>
<header class="tide-study-review__header"><div><p class="tide-eyebrow">Half Split / List Rhythm</p><h1>More breathing room. A clearer rhythm.</h1><p>Three desktop list headings on the same Half Split layout, with the pinned Apply controls aligned to the list’s bottom edge.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Double bottom space</span><span class="tide-badge">Same event cards</span><span class="tide-badge">Kit preserved</span></div></div><a class="tide-button tide-button--secondary" href="../half-split-refinements/pinned-apply/index.html" target="_blank" rel="noopener">Open previous Pinned Apply<span class="tide-sr-only"> in a new tab</span></a></header>
<nav class="tide-study-review__jump" aria-label="Choose a list heading">{links}</nav><div class="tide-study-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="390,844">Mobile · 390 × 844</option><option value="1024,768">Tablet · 1024 × 768</option><option value="1200,800">Small desktop · 1200 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><p>Scroll the event, scroll the list into November, then try search and filters. Open each study to use your browser’s actual width.</p></div><p class="tide-study-review__note">Lineup is the selected favorite. Its aligned heading rhythm continues through tablet and mobile. Desktop panels retain the doubled bottom gap and aligned Apply controls. Calendar and Month Index retain their original desktop-only treatments.</p><main id="studies">{''.join(sections)}</main><footer class="tide-study-review__footer"><nav aria-label="Study documentation"><a class="tide-link" href="../half-split-refinements/index.html">Previous refinements</a><a class="tide-link" href="README.md">Decisions and verification</a></nav></footer></body></html>'''


def outputs():return {'index.html':overview(),**{slug+'/'+f:page(f,slug,name) for slug,name,*_ in VARIANTS for f in steady.widths.wide.base.PAGES}}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();verify()
    for name,html in outputs().items():
        target=ROOT/name
        if args.check:
            if not target.is_file() or target.read_text(encoding='utf-8')!=html:raise ValueError('Stale list study: '+name)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf-8',newline='\n')
    verify();print(f'{len(outputs())} list-study HTML pages '+('verified.' if args.check else 'built.'))
