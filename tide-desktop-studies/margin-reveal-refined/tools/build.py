"""Desktop filter contents stay open; keep the native disclosure for smaller screens."""
import importlib.util
import re
import sys
sys.dont_write_bytecode=True
from refine_context import ROOT,MARGIN,verify
spec=importlib.util.spec_from_file_location('refined_margin_source',MARGIN/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES
BEFORE='<details class="tide-expandable tide-app__filters"><summary class="tide-expandable__summary">'
AFTER='<details class="tide-expandable tide-app__filters"><summary class="tide-expandable__summary tide-filter-study__summary">'

def page(filename):
    html=source.page(filename)
    html=html.replace('class="tide-margin-study ','class="tide-filter-study tide-margin-study ',1)
    html=html.replace('data-width="margin-reveal"','data-width="margin-refined"',1)
    html=html.replace('data-room="contained-margin-reveal"','data-room="margin-refined"',1)
    html=html.replace('href="../margin-filters.css"','href="../../contained-margin-filters/margin-filters.css"',1)
    html=html.replace('src="../slide-adapter.js"','src="../../contained-margin-filters/slide-adapter.js"',1)
    html=html.replace(BEFORE,AFTER,1)
    return html.replace('</head>','<link rel="stylesheet" href="../desktop-filters.css">\n</head>',1)

def overview():
    html=source.overview()
    html=html.replace('<title>Contained · Margin Reveal · Burque</title>','<title>Margin Reveal · Desktop filters · Burque</title>',1)
    html=html.replace('Let the margin make room.','Margin Reveal, refined.',1)
    html=html.replace('Original Contained preserved','Margin Reveal preserved',1)
    html=html.replace('../lineup-reading-widths/contained/index.html','../contained-margin-filters/demo/index.html')
    html=html.replace('Open preserved Contained','Open previous Margin Reveal').replace('Preserved Contained','Previous Margin Reveal')
    note='Desktop date and category options remain visible inside the filter sidebar, without the extra Filters disclosure. Tablet and mobile retain their native collapsible filters. The approved margin reveal, event geometry, search and pinned Apply remain unchanged.'
    return re.sub(r'(<p class="tide-study-review__note">).*?(</p>)',lambda m:m[1]+note+m[2],html,count=1,flags=re.S)

def outputs():return {'index.html':overview(),**{'demo/'+name:page(name) for name in PAGES}}

if __name__=='__main__':
    verify();generated=outputs()
    for name,content in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)} HTML documents built; no new JavaScript.')
