"""Guard original markup, component ownership and every preserved dependency."""
from collections import Counter
import importlib.util
import json
import re
import sys
sys.dont_write_bytecode=True
from refine_context import ROOT,PARENT,APP,verify
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
build=load('refined_builder',ROOT/'tools/build.py')
sys.path.insert(0,str(PARENT/'tools'))
shared=load('refined_contracts',PARENT/'tools/check.py')

def original(html):
    html=html.replace('class="tide-filter-study ','class="',1).replace(build.AFTER,build.BEFORE,1)
    html=html.replace('data-width="margin-refined"','data-width="margin-reveal"',1)
    html=html.replace('data-room="margin-refined"','data-room="contained-margin-reveal"',1)
    html=html.replace('href="../../contained-margin-filters/margin-filters.css"','href="../margin-filters.css"',1)
    html=html.replace('src="../../contained-margin-filters/slide-adapter.js"','src="../slide-adapter.js"',1)
    return html.replace('<link rel="stylesheet" href="../desktop-filters.css">\n','',1)

def main():
    preserved=verify();failures=[];refs=0;parity=0;classes=set();target_ids={}
    generated=build.outputs()
    for name,expected in generated.items():
        path=ROOT/name;html=path.read_text(encoding='utf-8')
        if html!=expected:failures.append(name+': stale generated HTML')
        scan=shared.Scan();scan.feed(html);classes.update(scan.classes)
        failures.extend(name+': '+issue for issue in shared.markup_issues(html))
        failures.extend(name+': duplicate ID '+key for key,n in Counter(scan.ids).items() if n>1)
        failures.extend(name+': unbound reference '+key for key in scan.linked if key not in scan.ids)
        if scan.styles or scan.handlers:failures.append(name+': inline style/handler')
        for ref in scan.refs:
            target=shared.target_file(path,ref)
            if target is None:continue
            refs+=1;other,fragment=target
            if not other.is_file():failures.append(name+': missing '+ref);continue
            if fragment and other.suffix=='.html':
                if other not in target_ids:
                    ids=shared.Scan();ids.feed(other.read_text(encoding='utf-8'));target_ids[other]=set(ids.ids)
                if fragment not in target_ids[other]:failures.append(name+': missing fragment '+ref)
    for name in build.PAGES:
        if original((ROOT/'demo'/name).read_text(encoding='utf-8'))!=build.source.page(name):failures.append(name+': original component HTML drift')
        else:parity+=1
    manifest=json.loads((APP/'kit/component-manifest.json').read_text(encoding='utf-8'))
    allowed={'tide-app','tide-study','tide-study-review','tide-shell','tide-shell-document','tide-feed-study','tide-slide-study','tide-slide-study-document','tide-room-study','tide-room-study-document','tide-width-study','tide-width-review','tide-margin-study','tide-filter-study'}
    failures.extend(shared.ownership_issues(classes,manifest,allowed))
    css=re.sub(r'/\*.*?\*/','',(ROOT/'desktop-filters.css').read_text(encoding='utf-8'),flags=re.S)
    if '@media (width >= 75rem)' not in css or '.tide-filter-study.tide-slide-study--mounted .tide-filter-study__summary { display: none; }' not in css:failures.append('Missing desktop-only mounted disclosure visibility contract')
    if re.search(r'--tide-[\w-]+\s*:|\.(?:tide-expandable|tide-field|tide-button)|(?:font|padding|border|background|color)[\w-]*\s*:',css):failures.append('Private CSS changes a primitive/component')
    verify();report={'pass':not failures,'htmlPages':len(generated),'localReferences':refs,'unchangedComponentDocuments':parity,'preserved':preserved,'newKitComponents':0,'newJavaScript':0,'failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)
if __name__=='__main__':raise SystemExit(main())
