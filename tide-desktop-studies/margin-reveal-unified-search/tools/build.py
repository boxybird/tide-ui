"""Reuse the exact Browse First documents; change the behavior source only."""
import importlib.util
import sys
sys.dont_write_bytecode=True
from unified_context import ROOT,BROWSE,verify
spec=importlib.util.spec_from_file_location('unified_browse_source',BROWSE/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES

def page(filename):
    html=source.page(filename)
    html=html.replace('src="../browse-flyout.js"','src="../unified-search.js"',1)
    html=html.replace('href="../browse-flyout.css"','href="../../margin-reveal-browse-first/browse-flyout.css"',1)
    return html.replace('</head>','<link rel="stylesheet" href="../unified-search.css">\n</head>',1)

def overview():
    html=source.overview()
    html=html.replace('Margin Reveal · Browse first · Burque','Margin Reveal · Unified search · Burque',1)
    html=html.replace('Margin Reveal / Browse first','Margin Reveal / Unified search',1)
    html=html.replace('Events first. Tools one tap away.','One search behavior. Every screen.',1)
    html=html.replace('A browse-first alternative for phones and tablets. Search, dates and categories share a left flyout; the approved desktop stays exactly as selected.','Search, dates and categories preview the matching count as you edit. One pinned Show events action applies everything — on desktop, tablet and phone.',1)
    html=html.replace('Desktop preserved</span>','Desktop geometry preserved</span>',1)
    html=html.replace('href="../margin-reveal-aligned/demo/index.html"','href="demo/index.html"',1).replace('Approved desktop<span','Open responsive prototype<span',1)
    desktop='''<section class="tide-study-review__section" aria-labelledby="desktop-title"><header class="tide-study-review__section-header"><div><p class="tide-eyebrow">01 / Desktop</p><h2 id="desktop-title">The same live count. One action.</h2><p>The original margin-aligned rail stays put. Search has no separate submit. Edit any criteria and watch the pinned count; Show events applies the draft. Reset all clears the draft.</p></div><a class="tide-button tide-button--secondary" href="demo/index.html" target="_blank" rel="noopener">Open desktop prototype<span class="tide-sr-only"> in a new tab</span></a></header><figure class="tide-study-review__figure"><figcaption><span>Live match count · Pinned Show events · Existing layout</span><span>1440 × 900 · live HTML</span></figcaption><div class="tide-responsive-filters-review__viewport" data-width="1440" data-height="900"><iframe src="demo/index.html" title="Desktop: unified search and filters" loading="eager"></iframe></div></figure></section>'''
    html=html.replace('<main id="study">','<main id="study">'+desktop,1)
    html=html.replace('01 / Mobile','02 / Mobile',1).replace('02 / Tablet','03 / Tablet',1)
    html=html.replace('Preserved desktop review</a>','Preserved desktop review</a><a class="tide-link" href="../margin-reveal-browse-first/index.html">Preserved Browse First</a>',1)
    html=html.replace('This is an isolated responsive proposal. The maintained kit and approved desktop release remain unchanged.','The previous Browse First release and both kits remain unchanged. This sibling extends its live preview and single-apply behavior to desktop.',1)
    return html

def outputs():return {'index.html':overview(),**{'demo/'+name:page(name) for name in PAGES}}
if __name__=='__main__':
    verify();generated=outputs()
    for name,content in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)} HTML documents built; original component markup preserved.')
