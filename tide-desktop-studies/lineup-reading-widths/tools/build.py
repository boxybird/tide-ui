"""Three private compositions of the preserved Left study; no kit writes."""
from html import escape
import importlib.util
import re
import sys
sys.dont_write_bytecode=True
from room_context import ROOT,PARENT,SLIDING,verify
spec=importlib.util.spec_from_file_location('reading_widths_left_source',SLIDING/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES
VARIANTS=[
 ('contained','Contained','A quieter, narrower frame.','The whole composition stops at 1216px. Opening filters divides the browsing half, exactly as Left does today. This is the simplest width change.','Two equal columns → filters and events share the left half'),
 ('give-and-take','Give & Take','Let the event make room.','The list holds its reading width. Filters take their space from the individual event. The outer frame stays at 1216px.','390px event list · 288px filters · flexible individual event'),
 ('reading-room','Reading Room','Use the margins. Ease the photograph.','A stable list and a modest, uncropped organizer photo. On wide screens, opening filters uses the outer space first; on smaller desktops, the individual event yields.','390px list · flexible frame · photo beside the introduction'),
]

def page(filename,slug,name):
    html=source.page(filename,'left',name).replace('Sliding Filters / '+name,'Reading Widths / '+name)
    html=html.replace('tide-slide-study-document"','tide-slide-study-document tide-room-study-document"',1)
    html=html.replace('<body data-slide="left"','<body data-room="'+slug+'" data-slide="left"',1)
    html=html.replace('class="tide-slide-study tide-slide-study--left ','class="tide-room-study tide-room-study--'+slug+' tide-slide-study tide-slide-study--left ',1)
    html=html.replace('href="../sliding-filters.css"','href="../../lineup-sliding-filters/sliding-filters.css"',1)
    html=html.replace('src="../sliding-filters.js"','src="../slide-adapter.js"',1)
    html=html.replace('tide-slide-study__header"','tide-slide-study__header tide-room-study__header"')
    html=html.replace('tide-slide-study__detail"','tide-slide-study__detail tide-room-study__detail"')
    if slug=='reading-room':
        html=html.replace('class="tide-event-hero tide-study__opening"','class="tide-event-hero tide-study__opening tide-room-study__opening"')
        html=re.sub(r'(<img class="tide-event-hero__photo)("[^>]*>)',r'<figure class="tide-room-study__media">\1 tide-room-study__photo\2<figcaption class="tide-room-study__caption tide-caption">Shared by the organizer</figcaption></figure>',html)
        for element in ('scrim','toolbar','content'):
            html=html.replace('class="tide-event-hero__'+element+'"','class="tide-event-hero__'+element+' tide-room-study__'+element+'"')
    return html.replace('</head>','<link rel="stylesheet" href="../reading-widths.css">\n<script src="../room.js" defer></script>\n</head>',1)

def adapter():
    original=(SLIDING/'sliding-filters.js').read_text(encoding='utf-8')
    before="const storageKey='tide:sliding-filters:'+document.body.dataset.slide;"
    assert original.count(before)==1
    return original.replace(before,"const storageKey='tide:reading-widths:'+document.body.dataset.room;")

def overview():
    sections=[]
    for i,(slug,name,title,desc,caption) in enumerate(VARIANTS,1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{i:02} / {escape(name)}</p><h2 id="{slug}-title">{title}</h2><p>{desc}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {escape(name)}<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>{caption}</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html" title="Reading Widths / {escape(name)}: live desktop study" loading="lazy"></iframe></div></figure></section>''')
    links=''.join(f'<a class="tide-chip" href="#{slug}-title">{i:02} · {escape(name)}</a>' for i,(slug,name,*_) in enumerate(VARIANTS,1))
    return '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Lineup · Reading Widths · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><link rel="stylesheet" href="review.css"><script src="../js/review.js" defer></script><script src="review.js" defer></script></head><body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the studies</a><header class="tide-study-review__header"><div><p class="tide-eyebrow">Lineup / Reading Widths</p><h1>A little less screen. A little more focus.</h1><p>Three additions to Left. Same cards, same controls, same event details. Compare reading widths and what happens when filters enter.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Left preserved</span><span class="tide-badge">48 events</span><span class="tide-badge">Kit untouched</span></div></div><a class="tide-button tide-button--secondary" href="../lineup-sliding-filters/left/index.html" target="_blank" rel="noopener">Open preserved Left<span class="tide-sr-only"> in a new tab</span></a></header><nav class="tide-study-review__jump" aria-label="Choose a composition">'''+links+'''</nav><div class="tide-study-review__toolbar tide-room-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="390,844">Mobile · 390 × 844</option><option value="1024,768">Tablet · 1024 × 768</option><option value="1200,800">Small desktop · 1200 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><div class="tide-field"><label class="tide-field__label" for="upload-sample">Ink After Dark photo</label><select class="tide-field__control" id="upload-sample"><option value="rough" selected>Rough organizer capture</option><option value="original">Original photo</option><option value="none">No image</option></select></div><p>Review controls only. The same imperfect photo is used for Ink After Dark in all three. Other events retain their own artwork.</p></div><p class="tide-study-review__note">Open filters with the icon beside The lineup. Apply stays pinned, the header stays visible, and the event keeps its natural document scroll. Width experiments start at 1200px. Reading Room also adapts its smaller photo at tablet widths; mobile keeps the original opening.</p><main id="studies">'''+''.join(sections)+'''</main><footer class="tide-study-review__footer"><nav aria-label="Study documentation"><a class="tide-link" href="../lineup-sliding-filters/left/index.html">Preserved Left</a><a class="tide-link" href="README.md">Decisions and verification</a></nav></footer></body></html>'''

def outputs():
    return {'index.html':overview(),'slide-adapter.js':adapter(),**{slug+'/'+f:page(f,slug,name) for slug,name,*_ in VARIANTS for f in PAGES}}

if __name__=='__main__':
    verify();generated=outputs()
    for name,content in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8',newline='\n')
    assets=ROOT/'assets';assets.mkdir(exist_ok=True)
    fixture=PARENT.parent/'date-line-in-practice/assets/images/organizer-upload.png'
    (assets/'organizer-upload.png').write_bytes(fixture.read_bytes())
    verify();print(f'{len(generated)-1} HTML pages and one isolated adapter built.')
