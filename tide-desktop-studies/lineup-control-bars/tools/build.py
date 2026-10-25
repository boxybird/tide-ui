"""Build desktop control-bar comparisons from preserved Lineup HTML."""
from html import escape
import importlib.util
import sys

sys.dont_write_bytecode=True
from bar_context import ROOT,PARENT,LINEUP,verify
spec=importlib.util.spec_from_file_location('lineup_source',LINEUP/'tools/build.py')
lineup=importlib.util.module_from_spec(spec);spec.loader.exec_module(lineup)
PAGES=lineup.steady.widths.wide.base.PAGES
VARIANTS=[
 ('inline','Inline','Everything within one reach.','A compact context row above one horizontal row of search, dates, categories and actions.','Always-visible controls · compact horizontal arrangement'),
 ('search-first','Search First','Give the search room.','A generous search beside the familiar introduction, with date and category controls on a second line.','Wide search · separate filter row'),
 ('filter-shelf','Filter Shelf','Open the filters when you need them.','The search stays in view. The original native Filters disclosure opens a horizontal shelf above both event columns.','Search always visible · expandable filter shelf'),
]
CLASSES={
 'tide-app__workspace tide-study__workspace':'tide-control-study__workspace',
 'tide-app__header tide-study__header':'tide-control-study__header',
 'tide-app__site-footer tide-study__footer':'tide-control-study__footer',
 'tide-app__results tide-study__results tide-feed-study__results':'tide-control-study__results',
 'tide-app__detail tide-study__detail':'tide-control-study__detail',
 'tide-page-intro tide-app__intro tide-feed-study__heading':'tide-control-study__intro',
 'tide-app__search tide-stack tide-shell__search':'tide-control-study__search',
 'tide-app__filter-row':'tide-control-study__context',
 'tide-expandable tide-app__filters':'tide-control-study__disclosure',
 'tide-expandable__body tide-app__filter-form':'tide-control-study__filter-body',
 'tide-app__date-fields':'tide-control-study__date-fields',
 'tide-app__filter-actions':'tide-control-study__actions',
}
REMOVED=['<script src="../../js/layout.js" defer></script>\n','<script src="../../half-split-refinements/dock.js" defer></script>\n']


def baseline(filename,name):
    return lineup.page(filename,'lineup',name).replace('../list-rhythm.css','../../list-rhythm/list-rhythm.css').replace('../headings.js','../../list-rhythm/headings.js')


def page(filename,slug,name):
    html=baseline(filename,'Control Bars / '+name)
    html=html.replace('class="tide-shell-document"','class="tide-shell-document tide-control-study-document"',1)
    for script in REMOVED:html=html.replace(script,'',1)
    html=html.replace('<body data-feed-study="lineup" class="','<body data-controls="'+slug+'" data-feed-study="lineup" class="tide-control-study tide-control-study--'+slug+' ',1)
    html=html.replace('class="tide-study__tools"','class="tide-control-study__bar"',1)
    for original,addition in CLASSES.items():html=html.replace('class="'+original+'"','class="'+original+' '+addition+'"')
    extra='<link rel="stylesheet" href="../control-bars.css">\n'
    if 'id="event-search-form"' in html:extra+='<script src="../controls.js" defer></script>\n'
    return html.replace('</head>',extra+'</head>',1)


def overview():
    html=lineup.overview()
    html=html.replace('Half Split · List Rhythm · Burque','Lineup · Control Bars · Burque').replace('Half Split / List Rhythm','Lineup / Control Bars')
    html=html.replace('More breathing room. A clearer rhythm.','Controls above. Events below.')
    html=html.replace('Three desktop list headings on the same Half Split layout, with the pinned Apply controls aligned to the list’s bottom edge.','Three desktop arrangements of the same search and filters, in a bar beneath the header and above both event columns.')
    html=html.replace('../half-split-refinements/pinned-apply/index.html','../list-rhythm/lineup/index.html').replace('Open previous Pinned Apply','Open preserved Lineup')
    html=html.replace('Double bottom space','Desktop control bars').replace('Same event cards','Same kit and cards')
    html=html.replace('Lineup is the selected favorite. Its aligned heading rhythm continues through tablet and mobile. Desktop panels retain the doubled bottom gap and aligned Apply controls. Calendar and Month Index retain their original desktop-only treatments.','Controls move above both columns at 1200px. The header and bar stay visible, the list fits the viewport, and the event scrolls naturally. Tablet and mobile remain the preserved Lineup.')
    html=html.replace('../half-split-refinements/index.html','../list-rhythm/index.html').replace('Previous refinements','Previous Lineup studies')
    for old,new in zip(lineup.VARIANTS,VARIANTS):
        oldslug,oldname,oldtitle,olddesc,oldcaption=old
        slug,name,title,description,caption=new
        html=html.replace(oldslug+'-title',slug+'-title').replace(oldslug+'/index.html',slug+'/index.html')
        html=html.replace(escape(oldtitle),escape(title)).replace(escape(olddesc),escape(description)).replace(escape(oldcaption),escape(caption))
        html=html.replace('Open '+oldname,'Open '+name).replace('· '+oldname,'· '+name).replace('/ '+oldname,'/ '+name)
    html=html.replace('List Rhythm /','Control Bars /')
    return html.replace('../list-rhythm/inline/index.html','../list-rhythm/lineup/index.html')


def outputs():return {'index.html':overview(),**{slug+'/'+f:page(f,slug,name) for slug,name,*_ in VARIANTS for f in PAGES}}


if __name__=='__main__':
    verify()
    for name,html in outputs().items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf-8',newline='\n')
    verify();print(f'{len(outputs())} control-bar pages built.')
