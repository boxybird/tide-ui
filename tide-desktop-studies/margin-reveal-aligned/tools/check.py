"""Check additive markup, references, ownership and preserved release inventories."""
from collections import Counter
import importlib.util
import json
import re
import sys
sys.dont_write_bytecode=True
from align_context import ROOT,PARENT,APP,verify
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
build=load('alignment_builder',ROOT/'tools/build.py')
sys.path.insert(0,str(PARENT/'tools'))
shared=load('alignment_contracts',PARENT/'tools/check.py')

def original(html):
    html=html.replace('class="tide-gutter-study ','class="',1)
    html=html.replace('data-width="margin-aligned"','data-width="margin-refined"',1)
    html=html.replace('data-room="margin-aligned"','data-room="margin-refined"',1)
    html=html.replace('href="../../margin-reveal-refined/desktop-filters.css"','href="../desktop-filters.css"',1)
    return html.replace('<link rel="stylesheet" href="../sidebar-alignment.css">\n','',1)

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
    allowed={'tide-app','tide-study','tide-study-review','tide-shell','tide-shell-document','tide-feed-study','tide-slide-study','tide-slide-study-document','tide-room-study','tide-room-study-document','tide-width-study','tide-width-review','tide-margin-study','tide-filter-study','tide-gutter-study'}
    failures.extend(shared.ownership_issues(classes,manifest,allowed))
    css=re.sub(r'/\*.*?\*/','',(ROOT/'sidebar-alignment.css').read_text(encoding='utf-8'),flags=re.S)
    if '@media (width >= 75rem)' not in css or 'padding-inline-start: 0' not in css or 'margin-inline-start: 0' not in css:failures.append('Missing desktop-only start inset contract')
    if re.search(r'--tide-[\w-]+\s*:|!important|(?:font|border|background|color|transform|translate|inline-size)[\w-]*\s*:|margin-inline-start:\s*-',css):failures.append('Alignment CSS changes a primitive or compensates with an offset')
    verify();report={'pass':not failures,'htmlPages':len(generated),'localReferences':refs,'unchangedComponentDocuments':parity,'preserved':preserved,'newKitComponents':0,'newJavaScript':0,'failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)
if __name__=='__main__':raise SystemExit(main())
