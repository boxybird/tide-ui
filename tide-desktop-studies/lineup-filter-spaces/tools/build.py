"""Three on-demand filtering compositions, using preserved Lineup documents."""
from html import escape
import importlib.util
import sys
sys.dont_write_bytecode=True
from space_context import ROOT,PARENT,BARS,verify
spec=importlib.util.spec_from_file_location('preserved_bar_source',BARS/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES
VARIANTS=[
 ('pocket','Pocket','Keep search close. Tuck the rest away.','Search stays in the list. Filters open a small, dismissible panel over it; the event remains available.','Visible search · nonmodal filter popover'),
 ('focus','Focus','A clear space to find something.','One Search & filter action opens a focused dialog. Close it and the two-column view returns exactly where you left it.','Minimal resting view · focused search dialog'),
 ('refine','Refine','Let the list become the controls.','Refine temporarily replaces the left-hand list. The individual event stays visible and usable throughout.','No overlay · temporary left-pane workspace'),
]
CLASSES={
 'tide-app__workspace tide-study__workspace':'tide-refine-study__workspace',
 'tide-app__header tide-study__header':'tide-refine-study__header',
 'tide-app__site-footer tide-study__footer':'tide-refine-study__footer',
 'tide-app__results tide-study__results tide-feed-study__results':'tide-refine-study__results',
 'tide-app__detail tide-study__detail':'tide-refine-study__detail',
 'tide-page-intro tide-app__intro tide-feed-study__heading':'tide-refine-study__intro',
 'tide-app__search tide-stack tide-shell__search':'tide-refine-study__search',
 'tide-app__filter-row':'tide-refine-study__context',
 'tide-expandable__body tide-app__filter-form':'tide-refine-study__fields',
 'tide-app__filter-actions':'tide-refine-study__actions',
 'tide-app__date-fields':'tide-refine-study__date-fields',
 'tide-event-group__header tide-feed-study__month-header':'tide-refine-study__month-header',
 'tide-results tide-feed-study__summary tide-feed-study__heading':'tide-refine-study__summary',
}

def editor(slug):
    tag='dialog' if slug=='focus' else 'section'
    attributes=' popover="auto" role="dialog" aria-modal="false"' if slug=='pocket' else ''
    title='Filter the lineup' if slug=='pocket' else 'Find your next good thing.'
    close='Back to lineup' if slug=='refine' else 'Close filters' if slug=='pocket' else 'Close search and filters'
    close_text='Back to lineup' if slug=='refine' else 'Close'
    return f'''<div class="tide-refine-study__quick" hidden></div>
<{tag} class="tide-refine-study__editor" id="refine-editor" aria-labelledby="refine-title"{attributes} hidden>
<header class="tide-refine-study__editor-head"><div><p class="tide-eyebrow">Albuquerque · {escape(slug.title())}</p><h2 class="tide-refine-study__title" id="refine-title">{title}</h2></div><button class="tide-button tide-button--secondary tide-refine-study__close" type="button" aria-label="{close}">{close_text}</button></header>
<div class="tide-refine-study__editor-body"><p class="tide-caption">Choose what works for you. Apply when you’re ready.</p></div>
</{tag}>
'''

def trigger(slug):
    label={'pocket':'Filters','focus':'Search & filter','refine':'Refine'}[slug]
    popup=' aria-haspopup="dialog"' if slug!='refine' else ''
    target=' popovertarget="refine-editor"' if slug=='pocket' else ''
    return f'<button class="tide-button tide-button--secondary tide-refine-study__trigger" type="button" aria-controls="refine-editor" aria-expanded="false"{popup}{target} hidden>{escape(label)}</button>'

ORDER='<span class="tide-results__order tide-feed-study__order">Soonest first</span>'

def page(filename,slug,name):
    html=source.baseline(filename,'Filter Spaces / '+name)
    html=html.replace('class="tide-shell-document"','class="tide-shell-document tide-refine-study-document"',1)
    for script in source.REMOVED: html=html.replace(script,'',1)
    html=html.replace('<body data-feed-study="lineup" class="','<body data-refine="'+slug+'" data-feed-study="lineup" class="tide-refine-study tide-refine-study--'+slug+' ',1)
    # This unused original mount stays hidden, so preceding three-column CSS never activates.
    html=html.replace('class="tide-study__tools"','class="tide-refine-study__unused"',1)
    for original,addition in CLASSES.items():html=html.replace('class="'+original+'"','class="'+original+' '+addition+'"')
    extra='<link rel="stylesheet" href="../filter-spaces.css">\n'
    if 'id="event-search-form"' in html:
        html=html.replace(ORDER,ORDER+trigger(slug),1)
        html=html.replace('<div class="tide-page-intro',editor(slug)+'<div class="tide-page-intro',1)
        extra+='<script src="../filter-spaces.js" defer></script>\n'
    return html.replace('</head>',extra+'</head>',1)

def overview():
    sections=[]
    for i,(slug,name,title,desc,caption) in enumerate(VARIANTS,1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{i:02} / {name}</p><h2 id="{slug}-title">{title}</h2><p>{desc}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {name}<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>{caption}</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html" title="Filter Spaces / {name}: live desktop study" loading="lazy"></iframe></div></figure></section>''')
    return '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Lineup · Filter Spaces · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><script src="../js/review.js" defer></script></head><body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the studies</a><header class="tide-study-review__header"><div><p class="tide-eyebrow">Lineup / Filter Spaces</p><h1>Two columns. Room to find.</h1><p>Three ways to bring search and filters forward only when you need them. Same Lineup cards, same event detail, same Bumble Dark.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">On demand</span><span class="tide-badge">48 events</span><span class="tide-badge">Kit preserved</span></div></div><a class="tide-button tide-button--secondary" href="../list-rhythm/lineup/index.html" target="_blank" rel="noopener">Open preserved Lineup<span class="tide-sr-only"> in a new tab</span></a></header><nav class="tide-study-review__jump" aria-label="Choose a filtering approach">'''+''.join(f'<a class="tide-chip" href="#{slug}-title">{i:02} · {name}</a>' for i,(slug,name,*_) in enumerate(VARIANTS,1))+'''</nav><div class="tide-study-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="390,844">Mobile · 390 × 844</option><option value="1024,768">Tablet · 1024 × 768</option><option value="1200,800">Small desktop · 1200 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><p>Try each action beside The lineup. Set dates and categories, apply, then clear. Close without applying to return to browsing.</p></div><p class="tide-study-review__note">Desktop changes begin at 1200px. The list stays bounded; the event scrolls naturally. Tablet and mobile restore the approved Lineup. Unapplied choices survive closing and reopening; submit search or Apply to change results.</p><main id="studies">'''+''.join(sections)+'''</main><footer class="tide-study-review__footer"><nav aria-label="Study documentation"><a class="tide-link" href="../lineup-control-bars/index.html">Previous control bars</a><a class="tide-link" href="README.md">Decisions and verification</a></nav></footer></body></html>'''

def outputs():return {'index.html':overview(),**{slug+'/'+f:page(f,slug,name) for slug,name,*_ in VARIANTS for f in PAGES}}

if __name__=='__main__':
    verify()
    generated=outputs()
    for name,html in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)} filter-space pages built.')
