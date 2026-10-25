"""Build two sliding-filter studies from unchanged Lineup component HTML."""
from html import escape
import importlib.util
import sys
sys.dont_write_bytecode=True
from slide_context import ROOT,PARENT,BARS,verify
spec=importlib.util.spec_from_file_location('sliding_lineup_source',BARS/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES
VARIANTS=[
 ('between','Between','Make room in the middle.','The list stays on the left. Filters slide into the space between the list and the individual event.','Closed: list / event · Open: list / filters / event'),
 ('left','Left','Bring Lineup back from the left.','Filters slide in on the left, narrowing and shifting the event list into the middle. The event detail stays steady.','Closed: list / event · Open: filters / list / event'),
]
CLASSES={
 'tide-app__workspace tide-study__workspace':'tide-slide-study__workspace',
 'tide-app__header tide-study__header':'tide-slide-study__header',
 'tide-app__site-footer tide-study__footer':'tide-slide-study__footer',
 'tide-app__results tide-study__results tide-feed-study__results':'tide-slide-study__results',
 'tide-app__detail tide-study__detail':'tide-slide-study__detail',
 'tide-page-intro tide-app__intro tide-feed-study__heading':'tide-slide-study__intro',
 'tide-results tide-feed-study__summary tide-feed-study__heading':'tide-slide-study__summary',
 'tide-event-group__header tide-feed-study__month-header':'tide-slide-study__month-header',
 'tide-results__order tide-feed-study__order':'tide-slide-study__order',
}
FILTER_ICON='<svg class="tide-icon" viewBox="0 0 15 15" fill="none" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><path d="M2 4h11M2 11h11M5 2v4M10 9v4" stroke="currentColor" stroke-linecap="round" stroke-width="1.25"/></svg>'
CLOSE_ICON='<svg class="tide-icon" viewBox="0 0 15 15" fill="none" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><path d="m4 4 7 7M11 4l-7 7" stroke="currentColor" stroke-linecap="round" stroke-width="1.25"/></svg>'
TRIGGER='<button class="tide-button tide-button--secondary tide-button--icon tide-slide-study__trigger" type="button" aria-label="Show search and filters" title="Show search and filters" aria-controls="lineup-filters" aria-expanded="false" hidden>'+FILTER_ICON+'</button>'
CLOSE='<button class="tide-button tide-button--quiet tide-button--icon tide-slide-study__close" type="button" aria-label="Close filters" title="Close filters" hidden>'+CLOSE_ICON+'</button>'
BADGE='<span class="tide-badge tide-slide-study__applied" hidden></span>'
ORIGINAL_RAIL='<aside class="tide-study__tools" aria-label="Search and filters" tabindex="0" hidden></aside>'
NEW_RAIL='<aside class="tide-slide-study__rail" id="lineup-filters" aria-label="Search and filters" tabindex="0" hidden>'+CLOSE+'</aside>'
ORDER='<span class="tide-results__order tide-feed-study__order tide-slide-study__order">Soonest first</span>'

def page(filename,slug,name):
    html=source.baseline(filename,'Sliding Filters / '+name)
    html=html.replace('class="tide-shell-document"','class="tide-shell-document tide-slide-study-document"',1)
    for script in source.REMOVED:html=html.replace(script,'',1)
    html=html.replace('<body data-feed-study="lineup" class="','<body data-slide="'+slug+'" data-feed-study="lineup" class="tide-slide-study tide-slide-study--'+slug+' ',1)
    html=html.replace(ORIGINAL_RAIL,NEW_RAIL,1)
    for original,addition in CLASSES.items():html=html.replace('class="'+original+'"','class="'+original+' '+addition+'"')
    extra='<link rel="stylesheet" href="../sliding-filters.css">\n'
    if 'id="event-search-form"' in html:
        html=html.replace(ORDER,ORDER.replace('</span>',BADGE+'</span>')+TRIGGER,1)
        extra+='<script src="../sliding-filters.js" defer></script>\n'
    return html.replace('</head>',extra+'</head>',1)

def overview():
    sections=[]
    for i,(slug,name,title,desc,caption) in enumerate(VARIANTS,1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{i:02} / {name}</p><h2 id="{slug}-title">{title}</h2><p>{desc}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {name}<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>{caption}</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html" title="Sliding Filters / {name}: live desktop study" loading="lazy"></iframe></div></figure></section>''')
    links=''.join(f'<a class="tide-chip" href="#{slug}-title">{i:02} · {name}</a>' for i,(slug,name,*_) in enumerate(VARIANTS,1))
    return '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Lineup · Sliding Filters · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><script src="../js/review.js" defer></script></head><body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the studies</a><header class="tide-study-review__header"><div><p class="tide-eyebrow">Lineup / Sliding Filters</p><h1>Two columns. Open into three.</h1><p>Lineup’s original controls return as an expanding column. Compare the middle reveal with a reveal from the left.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Half Split proportions</span><span class="tide-badge">48 events</span><span class="tide-badge">Kit preserved</span></div></div><a class="tide-button tide-button--secondary" href="../list-rhythm/lineup/index.html" target="_blank" rel="noopener">Open preserved Lineup<span class="tide-sr-only"> in a new tab</span></a></header><nav class="tide-study-review__jump" aria-label="Choose a reveal direction">'''+links+'''</nav><div class="tide-study-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="390,844">Mobile · 390 × 844</option><option value="1024,768">Tablet · 1024 × 768</option><option value="1200,800">Small desktop · 1200 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><p>Use the filter icon beside The lineup. Close with the same icon, the × in the filters column, or Escape. Try it again after scrolling the list.</p></div><p class="tide-study-review__note">At 1200px and above, the browsing half expands into two equal columns. The individual event keeps its width and natural page scroll. Apply stays pinned. Reduced motion switches immediately. Tablet and mobile retain the preserved Lineup.</p><main id="studies">'''+''.join(sections)+'''</main><footer class="tide-study-review__footer"><nav aria-label="Study documentation"><a class="tide-link" href="../list-rhythm/lineup/index.html">Preserved Lineup</a><a class="tide-link" href="README.md">Decisions and verification</a></nav></footer></body></html>'''

def outputs():return {'index.html':overview(),**{slug+'/'+f:page(f,slug,name) for slug,name,*_ in VARIANTS for f in PAGES}}

if __name__=='__main__':
    verify();generated=outputs()
    for name,html in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)} sliding-filter pages built.')
