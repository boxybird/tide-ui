"""Preserve original Contained geometry; let only its browsing area use the gutter."""
import importlib.util
import sys
sys.dont_write_bytecode=True
from margin_context import ROOT,PARENT,WIDTHS,verify
spec=importlib.util.spec_from_file_location('margin_contained_source',WIDTHS/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES

def page(filename):
    html=source.page(filename,'original','Margin Reveal')
    html=html.replace('data-width="original"','data-width="margin-reveal"',1)
    html=html.replace('data-room="contained-widths-original"','data-room="contained-margin-reveal"',1)
    html=html.replace('class="tide-width-study ','class="tide-margin-study tide-width-study ',1)
    html=html.replace('href="../widths-search.css"','href="../../contained-widths-search/widths-search.css"',1)
    html=html.replace('src="../search-layout.js"','src="../../contained-widths-search/search-layout.js"',1)
    return html.replace('</head>','<link rel="stylesheet" href="../margin-filters.css">\n</head>',1)

def adapter():
    return source.adapter().replace("'tide:contained-widths:filters:'","'tide:margin-filters:'",1)

def overview():
    return '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Contained · Margin Reveal · Burque</title><link rel="stylesheet" href="../base/kit/css/tide.css"><link rel="stylesheet" href="../css/review.css"><link rel="stylesheet" href="../contained-widths-search/review.css"><script src="../js/review.js" defer></script><script src="../contained-widths-search/review.js" defer></script></head><body class="tide tide-study-review"><a class="tide-skip-link" href="#study">Skip to the study</a><header class="tide-study-review__header"><div><p class="tide-eyebrow">Contained / Margin Reveal</p><h1>Let the margin make room.</h1><p>The original 1216px composition. Filters extend toward the header’s left edge; the individual event holds its position and width.</p><div class="tide-row tide-study-review__badges"><span class="tide-badge">Original Contained preserved</span><span class="tide-badge">Single event stays put</span><span class="tide-badge">Kit unchanged</span></div></div><a class="tide-button tide-button--secondary" href="demo/index.html" target="_blank" rel="noopener">Open Margin Reveal<span class="tide-sr-only"> in a new tab</span></a></header><div class="tide-study-review__toolbar tide-width-review__toolbar"><div class="tide-field"><label class="tide-field__label" for="preview-size">Preview viewport</label><select class="tide-field__control" id="preview-size"><option value="390,844">Mobile · 390 × 844</option><option value="1024,768">Tablet · 1024 × 768</option><option value="1200,600">Small desktop · 1200 × 600</option><option value="1280,800">Compact laptop · 1280 × 800</option><option value="1440,900" selected>Desktop · 1440 × 900</option><option value="1600,900">Desktop · 1600 × 900</option><option value="1920,1080">Wide · 1920 × 1080</option><option value="2560,1440">Wide · 2560 × 1440</option></select></div><div class="tide-field"><label class="tide-field__label" for="search-layout">Search button position</label><select class="tide-field__control" id="search-layout"><option value="below" selected>Below · full width</option><option value="compact">Below · compact</option><option value="inline">Beside · original</option></select></div><div class="tide-field"><label class="tide-field__label" for="upload-sample">Ink After Dark photo</label><select class="tide-field__control" id="upload-sample"><option value="rough" selected>Rough organizer capture</option><option value="original">Original photo</option><option value="none">No image</option></select></div></div><p class="tide-study-review__note">This preview starts open. Close and reopen with the filter icon beside The lineup. The filters’ outer left edge aligns with the Burque wordmark. On roomy desktops, the list can retain its original width; on compact desktops with little outer margin, it still shares the available left-hand space. The right event never moves to accommodate filters.</p><main id="study"><section class="tide-study-review__section" aria-labelledby="margin-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">01 / Margin Reveal</p><h2 id="margin-title">The event stays. The left opens out.</h2><p>Search and filters use a modest column at the wider header margin. The list keeps its original right edge and stops growing at its approved width.</p></div><a class="tide-button tide-button--secondary" href="../lineup-reading-widths/contained/index.html" target="_blank" rel="noopener">Open preserved Contained<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>Closed: original two columns · Open: filters in the outer margin, list to the midpoint</span><span class="tide-study-review__dimensions">1440 × 900 · live HTML</span></figcaption><div class="tide-study-review__viewport"><iframe src="demo/index.html?preview-filters=open" title="Contained / Margin Reveal: live desktop study" loading="lazy"></iframe></div></figure></section></main><footer class="tide-study-review__footer"><nav aria-label="Study documentation"><a class="tide-link" href="../lineup-reading-widths/contained/index.html">Preserved Contained</a><a class="tide-link" href="../contained-widths-search/index.html">Previous width comparisons</a><a class="tide-link" href="README.md">Decisions and verification</a></nav></footer></body></html>'''

def outputs():
    return {'index.html':overview(),'slide-adapter.js':adapter(),**{'demo/'+name:page(name) for name in PAGES}}

if __name__=='__main__':
    verify();generated=outputs()
    for name,content in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)-1} HTML documents and one namespaced adapter built.')
