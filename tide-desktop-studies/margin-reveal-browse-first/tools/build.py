"""A smaller-screen browse-first alternative, preserving prior proposals."""
import importlib.util
import sys
sys.dont_write_bytecode=True
from browse_context import ROOT,RESPONSIVE,verify
spec=importlib.util.spec_from_file_location('browse_responsive_source',RESPONSIVE/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES
LAUNCHER='''<button class="tide-button tide-button--quiet tide-button--icon tide-responsive-filters__trigger tide-browse-flyout__trigger" type="button" aria-label="Search and filters" title="Search and filters" aria-haspopup="dialog" aria-controls="responsive-filters" aria-expanded="false" hidden><svg class="tide-icon" viewBox="0 0 15 15" fill="none" aria-hidden="true" focusable="false"><circle cx="6.5" cy="6.5" r="4" stroke="currentColor" stroke-width="1.25"/><path d="m9.5 9.5 3.5 3.5" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"/></svg><span class="tide-browse-flyout__trigger-label">Search &amp; filters</span></button>'''
DIALOG=source.DIALOG.replace('class="tide-responsive-filters__dialog"','class="tide-responsive-filters__dialog tide-browse-flyout__dialog"',1).replace('class="tide-responsive-filters__body"','class="tide-responsive-filters__body tide-browse-flyout__body"',1).replace('tabindex="-1">Filters</h2>','tabindex="-1">Search &amp; filters</h2>',1).replace('Cancel filter changes','Cancel search and filter changes',1).replace('Choose dates and categories. Changes apply together.','Find an event or narrow the lineup. Changes apply together.',1).replace('Reset filters</button>','Reset all</button>',1)

def page(filename):
    html=source.page(filename)
    html=html.replace('src="../responsive-filters.js"','src="../browse-flyout.js"',1)
    html=html.replace('href="../responsive-filters.css"','href="../../margin-reveal-responsive-filters/responsive-filters.css"',1)
    html=html.replace(source.LAUNCHER,LAUNCHER,1).replace(source.DIALOG,DIALOG,1)
    return html.replace('</head>','<link rel="stylesheet" href="../browse-flyout.css">\n</head>',1)

def overview():
    html=source.overview()
    html=html.replace('Margin Reveal · Tablet and mobile filters · Burque','Margin Reveal · Browse first · Burque',1)
    html=html.replace('href="review.css"','href="../margin-reveal-responsive-filters/review.css"',1).replace('src="review.js"','src="../margin-reveal-responsive-filters/review.js"',1)
    html=html.replace('Margin Reveal / Responsive filters','Margin Reveal / Browse first',1).replace('Room to choose.','Events first. Tools one tap away.',1)
    html=html.replace('The approved desktop stays exactly as selected. On smaller screens, the same filters get their own space, with the action always in reach.','A browse-first alternative for phones and tablets. Search, dates and categories share a left flyout; the approved desktop stays exactly as selected.',1)
    html=html.replace('A dedicated filter screen.','Open straight into the lineup.',1)
    html=html.replace('Tap Filters. Dates and categories open full screen. Change your choices, reset them, or cancel; Show events applies them together and returns to the lineup.','Start with events. Tap the search icon in the header to reveal the left sidebar. Search and filters share one form, a live match count and the pinned Show events action.',1)
    html=html.replace('Search stays in the list · Filters get the screen · Apply stays visible','Events lead · Search is one tap away · Left flyout',1)
    html=html.replace('Mobile: working filter screen','Mobile: browse-first left flyout',1)
    html=html.replace('A drawer, without a tighter list.','The same flyout on tablet.',1)
    html=html.replace('The filters open over the right edge. The underlying list and selected event keep their space. The controls and draft/apply behavior match the phone.','Search and filters open from the left over the page. The underlying event list and single event retain their widths. The header action stays reachable as you browse.',1)
    html=html.replace('Tap Filters in the list to open the drawer','Tap Search &amp; filters in the header to open the left sidebar',1).replace('Tablet: working filter drawer','Tablet: browse-first left flyout',1)
    html=html.replace('<a class="tide-link" href="README.md">','<a class="tide-link" href="../margin-reveal-responsive-filters/index.html">Previous search-first proposal</a><a class="tide-link" href="README.md">',1)
    return html

def outputs():return {'index.html':overview(),**{'demo/'+name:page(name) for name in PAGES}}
if __name__=='__main__':
    verify();generated=outputs()
    for name,content in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)} HTML documents built; desktop source unchanged.')
