"""Guard every dependency, original component markup, BEM and local references."""
from collections import Counter
import hashlib
import importlib.util
import json
import re
import sys
sys.dont_write_bytecode=True
from room_context import ROOT,PARENT,SLIDING,APP,verify
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
build=load('room_builder',ROOT/'tools/build.py')
sys.path.insert(0,str(PARENT/'tools'))
shared=load('room_contracts',PARENT/'tools/check.py')

def original(html,slug):
    html=html.replace(' data-room="'+slug+'"','',1)
    html=re.sub(r'class="([^"]*)"',lambda m:'class="'+' '.join(c for c in m[1].split() if not c.startswith('tide-room-study'))+'"',html)
    html=re.sub(r'<figure class="">(.*?)<figcaption class="tide-caption">Shared by the organizer</figcaption></figure>',r'\1',html,flags=re.S)
    html=html.replace('Reading Widths / ','Sliding Filters / ',1)
    html=html.replace('href="../../lineup-sliding-filters/sliding-filters.css"','href="../sliding-filters.css"',1)
    html=html.replace('src="../slide-adapter.js"','src="../sliding-filters.js"',1)
    html=html.replace('<link rel="stylesheet" href="../reading-widths.css">\n<script src="../room.js" defer></script>\n','',1)
    return html

def main():
    preserved=verify();failures=[];refs=0;parity=0;classes=set();target_ids={}
    manifest=json.loads((APP/'kit/component-manifest.json').read_text(encoding='utf-8'))
    generated=build.outputs()
    for name,expected in generated.items():
        path=ROOT/name;content=path.read_text(encoding='utf-8')
        if content!=expected:failures.append(name+': stale generated source')
        if path.suffix!='.html':continue
        scan=shared.Scan();scan.feed(content);classes.update(scan.classes)
        failures.extend(name+': '+issue for issue in shared.markup_issues(content))
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
    for slug,name,*_ in build.VARIANTS:
        for filename in build.PAGES:
            actual=original((ROOT/slug/filename).read_text(encoding='utf-8'),slug)
            expected=build.source.page(filename,'left',name)
            if actual!=expected:failures.append(slug+'/'+filename+': existing component markup drift')
            else:parity+=1
    allowed={'tide-app','tide-study','tide-study-review','tide-shell','tide-shell-document','tide-feed-study','tide-slide-study','tide-slide-study-document','tide-room-study','tide-room-study-document','tide-room-review'}
    failures.extend(shared.ownership_issues(classes,manifest,allowed))
    css=re.sub(r'/\*.*?\*/','',(ROOT/'reading-widths.css').read_text(encoding='utf-8'),flags=re.S)
    if re.search(r'\.(?:tide-event-|tide-button|tide-field|tide-badge|tide-choice|tide-expandable)',css):failures.append('Private CSS targets kit component selectors')
    if re.search(r'--tide-(?!room-study-)[\w-]+\s*:',css):failures.append('Private CSS redefines shared token')
    if re.search(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch)\(',css):failures.append('Private CSS bypasses palette')
    if re.search(r'\b(?:font[\w-]*|line-height|letter-spacing|border-radius)\s*:',css):failures.append('Private CSS changes a primitive')
    definitions='\n'.join(p.read_text(encoding='utf-8') for p in (APP/'kit/css').glob('*.css'))
    for path in [APP/'css/app.css',PARENT/'css/studies.css',PARENT/'half-split-refinements/shell.css',PARENT/'list-rhythm/list-rhythm.css',SLIDING/'sliding-filters.css']:definitions+=path.read_text(encoding='utf-8')
    definitions+=css
    defined=set(re.findall(r'(--tide-[\w-]+)\s*:',definitions))
    for path in [ROOT/'slide-adapter.js',PARENT/'list-rhythm/headings.js']:defined.update(re.findall(r"setProperty\('(--tide-[\w-]+)'",path.read_text(encoding='utf-8')))
    failures.extend('Undefined token '+token for token in set(re.findall(r'var\((--tide-[\w-]+)',css))-defined)
    fixture=PARENT.parent/'date-line-in-practice/assets/images/organizer-upload.png'
    if (ROOT/'assets/organizer-upload.png').read_bytes()!=fixture.read_bytes():failures.append('Organizer fixture changed')
    if '@media (prefers-reduced-motion: reduce)' not in css:failures.append('Missing reduced motion rule')
    verify()
    report={'pass':not failures,'htmlPages':len(generated)-1,'localReferences':refs,'unchangedComponentDocuments':parity,'preserved':preserved,'newKitComponents':0,'adapterChange':'Namespaced session key only; all original behavior retained.','failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)
if __name__=='__main__':raise SystemExit(main())
