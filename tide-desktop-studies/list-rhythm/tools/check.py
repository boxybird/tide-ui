"""Check only this study; read earlier sources and inventories without writing them."""
import importlib.util
import json
import re
import sys
from collections import Counter

sys.dont_write_bytecode=True
from context import ROOT,PARENT,APP,verify


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


build=load('rhythm_builder',ROOT/'tools/build.py')
sys.path.insert(0,str(PARENT/'tools'))
shared=load('rhythm_shared_contracts',PARENT/'tools/check.py')


def main():
    preserved=verify();failures=[];refs=0;parity=0;classes=set();target_ids={}
    manifest=json.loads((APP/'kit/component-manifest.json').read_text(encoding='utf-8'))
    generated=build.outputs()
    for name,expected in generated.items():
        path=ROOT/name;html=path.read_text(encoding='utf-8')
        if html!=expected:failures.append(name+': stale generated HTML')
        scan=shared.Scan();scan.feed(html);classes.update(scan.classes)
        failures.extend(name+': '+issue for issue in shared.markup_issues(html))
        failures.extend(name+': duplicate ID '+key for key,n in Counter(scan.ids).items() if n>1)
        failures.extend(name+': unbound description/form/label '+key for key in scan.linked if key not in scan.ids)
        if scan.styles or scan.handlers:failures.append(name+': inline HTML style/handler')
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
        for filename in build.steady.widths.wide.base.PAGES:
            html=(ROOT/slug/filename).read_text(encoding='utf-8')
            if slug=='lineup':html=html.replace(build.LINEUP_KICKER,'',1)
            html=html.replace(' data-feed-study="'+slug+'"','',1)
            html=re.sub(r'class="([^"]*)"',lambda m:'class="'+' '.join(c for c in m[1].split() if not c.startswith('tide-feed-study'))+'"',html)
            html=html.replace('<link rel="stylesheet" href="../list-rhythm.css">\n','',1).replace('<script src="../headings.js" defer></script>\n','',1)
            if html!=build.baseline(filename,name):failures.append(slug+'/'+filename+': preserved component markup drift')
            else:parity+=1
    failures.extend(shared.ownership_issues(classes,manifest,{'tide-app','tide-study','tide-study-review','tide-shell','tide-shell-document','tide-feed-study'}))
    css=re.sub(r'/\*.*?\*/','',(ROOT/'list-rhythm.css').read_text(encoding='utf-8'),flags=re.S)
    if re.search(r'\.(?:tide-event-|tide-button|tide-field|tide-badge|tide-choice|tide-expandable)',css):failures.append('Private CSS targets a kit component')
    if re.search(r'--tide-(?!feed-study-|shell-panel-height\s*:)[\w-]+\s*:',css):failures.append('Private CSS redefines a shared token')
    if re.search(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch)\(',css):failures.append('Private CSS bypasses semantic color tokens')
    if re.search(r'\b(?:font-family|border-radius)\s*:',css):failures.append('Private CSS changes a font or corner primitive')
    definitions='\n'.join(p.read_text(encoding='utf-8') for p in (APP/'kit/css').glob('*.css'))
    definitions+=(PARENT/'half-split-refinements/shell.css').read_text(encoding='utf-8')+css
    defined=set(re.findall(r'(--tide-[\w-]+)\s*:',definitions))
    defined.update(re.findall(r"setProperty\('(--tide-[\w-]+)'",(ROOT/'headings.js').read_text(encoding='utf-8')))
    for token in set(re.findall(r'var\((--tide-[\w-]+)',css))-defined:failures.append('Undefined CSS token '+token)
    verify()
    report={'pass':not failures,'htmlPages':len(generated),'localReferences':refs,'unchangedComponentDocuments':parity,'preserved':preserved,'newKitComponents':0,'failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)


if __name__=='__main__':raise SystemExit(main())
