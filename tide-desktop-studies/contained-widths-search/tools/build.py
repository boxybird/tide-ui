"""Three small width increments, with orthogonal search-layout comparisons."""
from html import escape
import importlib.util
import sys
sys.dont_write_bytecode=True
from width_context import ROOT,PARENT,READING,SLIDING,verify
spec=importlib.util.spec_from_file_location('contained_width_source',READING/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES
VARIANTS=[
 ('original','Original width','1216px','76rem','Contained, as selected.','The current maximum width, with the search button moved below. Switch it back beside the field to compare with the preserved version.'),
 ('wider','A little wider','1280px','80rem','A little more room.','An extra 64px overall. Each open browsing column gains 16px; the individual event gains 32px.'),
 ('widest','Wider again','1344px','84rem','One more small step.','Another 64px overall. The same equal halves and left reveal, with a little more room for the filters and event titles.'),
]
SEARCH_TEXT='<span class="tide-width-study__search-text" aria-hidden="true">Search events</span>'

def page(filename,slug,name):
    html=source.page(filename,'contained',name).replace('Reading Widths / '+name,'Contained / '+name)
    html=html.replace('<body data-room="contained"','<body data-width="'+slug+'" data-search-layout="below" data-room="contained-widths-'+slug+'"',1)
    html=html.replace('class="tide-room-study ','class="tide-width-study tide-width-study--'+slug+' tide-room-study ',1)
    html=html.replace('href="../reading-widths.css"','href="../../lineup-reading-widths/reading-widths.css"',1)
    html=html.replace('src="../room.js"','src="../../lineup-reading-widths/room.js"',1)
    html=html.replace('class="tide-search-line"','class="tide-search-line tide-width-study__search-row"',1)
    before='<button class="tide-button tide-button--icon" aria-label="Search events" type="submit">'
    after='<button class="tide-button tide-button--icon tide-width-study__search-submit" aria-label="Search events" type="submit">'+SEARCH_TEXT
    html=html.replace(before,after,1)
    return html.replace('</head>','<link rel="stylesheet" href="../widths-search.css">\n<script src="../search-layout.js" defer></script>\n</head>',1)

def adapter():
    original=(SLIDING/'sliding-filters.js').read_text(encoding='utf-8')
    before="const storageKey='tide:sliding-filters:'+document.body.dataset.slide;"
    assert original.count(before)==1
    original=original.replace(before,"const storageKey='tide:contained-widths:filters:'+document.body.dataset.width;")
    stored="  try{desiredOpen=sessionStorage.getItem(storageKey)==='open';}catch{}"
    assert original.count(stored)==1
    return original.replace(stored,stored+"\n  if(new URLSearchParams(location.search).get('preview-filters')==='open'){\n    desiredOpen=true;\n    try{sessionStorage.setItem(storageKey,'open');}catch{}\n  }")

def overview():
    sections=[]
    for i,(slug,name,width,rem,title,desc) in enumerate(VARIANTS,1):
        sections.append(f'''<section class="tide-study-review__section" aria-labelledby="{slug}-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">{i:02} / {name} / {width}</p><h2 id="{slug}-title">{title}</h2><p>{desc}</p></div><a class="tide-button tide-button--secondary" href="{slug}/index.html" target="_blank" rel="noopener">Open {name.lower()}<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>{width} maximum · equal list and event halves · filters reveal on the left</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="{slug}/index.html?preview-filters=open" title="Contained / {name}: live desktop study" loading="lazy"></iframe></div></figure></section>''')
    links=''.join(f'<a class="tide-chip" href="#{slug}-title">{i:02} · {width}</a>' for i,(slug,name,width,*_) in enumerate(VARIANTS,1))
    return '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Contained · Width &amp; Search · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><link rel="stylesheet" href="review.css"><script src="../js/review.js" defer></script><script src="review.js" defer></script></head><body class="tide tide-study-review"><a class="tide-skip-link" href="#studies">Skip to the studies</a><header class="tide-study-review__header"><div><p class="tide-eyebrow">Contained / Width &amp; Search</p><h1>A little room to search.</h1><p>Your selected Contained composition, in three close widths. Compare the width and the search arrangement independently.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Contained preserved</span><span class="tide-badge">Existing kit components</span><span class="tide-badge">48 events</span></div></div><a class="tide-button tide-button--secondary" href="../lineup-reading-widths/contained/index.html" target="_blank" rel="noopener">Open preserved Contained<span class="tide-sr-only"> in a new tab</span></a></header><nav class="tide-study-review__jump" aria-label="Choose a width">'''+links+'''</nav><div class="tide-study-review__toolbar tide-width-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="390,844">Mobile · 390 × 844</option><option value="1024,768">Tablet · 1024 × 768</option><option value="1200,600">Small desktop · 1200 × 600</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option></select></div><div class="tide-field"><label class="tide-field__label" for="search-layout">Search button position</label><select class="tide-field__control" id="search-layout"><option value="below" selected>Below · full width</option><option value="compact">Below · compact</option><option value="inline">Beside · original</option></select></div><div class="tide-field"><label class="tide-field__label" for="upload-sample">Ink After Dark photo</label><select class="tide-field__control" id="upload-sample"><option value="rough" selected>Rough organizer capture</option><option value="original">Original photo</option><option value="none">No image</option></select></div></div><p class="tide-study-review__note">Previews open with filters visible. The search-position choice applies to all three, giving nine combinations. Close filters to compare the two-column view. These changes start at 1200px; tablet and mobile retain the current layout. On smaller desktops the three maximum widths naturally converge to fit the available space.</p><main id="studies">'''+''.join(sections)+'''</main><footer class="tide-study-review__footer"><nav aria-label="Study documentation"><a class="tide-link" href="../lineup-reading-widths/contained/index.html">Preserved Contained</a><a class="tide-link" href="README.md">Decisions and verification</a></nav></footer></body></html>'''

def outputs():
    return {'index.html':overview(),'slide-adapter.js':adapter(),**{slug+'/'+f:page(f,slug,name) for slug,name,*_ in VARIANTS for f in PAGES}}

if __name__=='__main__':
    verify();generated=outputs()
    for name,content in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)-1} HTML pages and one isolated adapter built.')
