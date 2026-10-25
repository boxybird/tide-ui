"""Verify source ownership, native form contracts and preservation."""
import importlib.util
import json
import re
import sys
from collections import Counter

sys.dont_write_bytecode=True
from guard import ROOT,PARENT,APP,guard


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    item=importlib.util.module_from_spec(spec);spec.loader.exec_module(item);return item


build=load('shell_builder',ROOT/'tools/build.py')
sys.path.insert(0,str(PARENT/'tools'))
shared=load('shared_contracts',PARENT/'tools/check.py')


def main():
    preserved=guard();failures=[];refs=0;parity=0;classes=set();target_ids={}
    manifest=json.loads((APP/'kit/component-manifest.json').read_text())
    generated=build.outputs()
    for name,expected in generated.items():
        path=ROOT/name;html=path.read_text(encoding='utf-8')
        if html!=expected:failures.append(name+': stale generated HTML')
        scan=shared.Scan();scan.feed(html);classes.update(scan.classes)
        failures.extend(name+': '+issue for issue in shared.markup_issues(html))
        failures.extend(name+': duplicate ID '+k for k,n in Counter(scan.ids).items() if n>1)
        failures.extend(name+': unbound label/description/form '+k for k in scan.linked if k not in scan.ids)
        if scan.styles or scan.handlers:failures.append(name+': inline HTML styles/handlers')
        for ref in scan.refs:
            target=shared.target_file(path,ref)
            if target is None:continue
            refs+=1;other,fragment=target
            if not other.is_file():failures.append(name+': missing '+ref);continue
            if fragment and other.suffix=='.html':
                if other not in target_ids:
                    ids=shared.Scan();ids.feed(other.read_text(encoding='utf-8'));target_ids[other]=set(ids.ids)
                if fragment not in target_ids[other]:failures.append(name+': missing fragment '+ref)
    for slug,name,*_ in build.VARIANTS:
        for filename in build.widths.wide.base.PAGES:
            html=(ROOT/slug/filename).read_text(encoding='utf-8')
            html=html.replace('<html class="tide-shell-document" lang="en"','<html lang="en"',1)
            html=html.replace('tide-shell tide-shell--'+slug+' ','',1).replace(' tide-shell__search','',1)
            html=html.replace('<link rel="stylesheet" href="../shell.css">\n','',1).replace('<script src="../dock.js" defer></script>\n','',1)
            if html!=build.baseline(filename,name):failures.append(slug+'/'+filename+': component markup drift')
            else:parity+=1
    failures.extend(shared.ownership_issues(classes,manifest,{'tide-app','tide-study','tide-study-review','tide-shell','tide-shell-document'}))
    css=re.sub(r'/\*.*?\*/','',(ROOT/'shell.css').read_text(),flags=re.S)
    if re.search(r'\.(?:tide-event-|tide-button|tide-field|tide-badge|tide-choice|tide-expandable)',css):failures.append('Shell CSS targets a kit component')
    if re.search(r'(?:^|[;{])\s*(?:font[\w-]*|line-height|letter-spacing|border-radius)\s*:',css):failures.append('Shell CSS changes a primitive')
    if re.search(r'--tide-(?!shell-)[\w-]+\s*:',css):failures.append('Shell CSS redefines a shared token')
    if 'display: contents' in css or 'display:contents' in css:failures.append('Landmarks must keep their boxes')
    guard()
    report={'pass':not failures,'htmlPages':len(generated),'localReferences':refs,'unchangedComponentDocuments':parity,
            'preserved':preserved,'newKitComponents':0,'failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)


if __name__=='__main__':raise SystemExit(main())
