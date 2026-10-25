"""Place the existing sidebar sections on the header's desktop start line."""
import importlib.util
import re
import sys
sys.dont_write_bytecode=True
from align_context import ROOT,REFINED,verify
spec=importlib.util.spec_from_file_location('alignment_refined_source',REFINED/'tools/build.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
PAGES=source.PAGES

def page(filename):
    html=source.page(filename)
    html=html.replace('class="tide-filter-study ','class="tide-gutter-study tide-filter-study ',1)
    html=html.replace('data-width="margin-refined"','data-width="margin-aligned"',1)
    html=html.replace('data-room="margin-refined"','data-room="margin-aligned"',1)
    html=html.replace('href="../desktop-filters.css"','href="../../margin-reveal-refined/desktop-filters.css"',1)
    return html.replace('</head>','<link rel="stylesheet" href="../sidebar-alignment.css">\n</head>',1)

def overview():
    html=source.overview()
    html=html.replace('<title>Margin Reveal · Desktop filters · Burque</title>','<title>Margin Reveal · Header alignment · Burque</title>',1)
    html=html.replace('Margin Reveal, refined.','One shared left edge.',1)
    html=html.replace('Margin Reveal preserved','Previous refinement preserved',1)
    html=html.replace('../contained-margin-filters/demo/index.html','../margin-reveal-refined/demo/index.html')
    note='The sidebar heading, search field, date/category groups and pinned Apply action now share the header’s left edge. Desktop section wrappers surrender their duplicate start inset. Control padding, right spacing, event geometry and the smaller-screen layout are retained.'
    return re.sub(r'(<p class="tide-study-review__note">).*?(</p>)',lambda m:m[1]+note+m[2],html,count=1,flags=re.S)

def outputs():return {'index.html':overview(),**{'demo/'+name:page(name) for name in PAGES}}

if __name__=='__main__':
    verify();generated=outputs()
    for name,content in generated.items():
        target=ROOT/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8',newline='\n')
    verify();print(f'{len(generated)} HTML documents built; no new JavaScript.')
