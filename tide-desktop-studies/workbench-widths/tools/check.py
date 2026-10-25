"""Check width-study markup and references without running any parent writer."""
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
from preserve import ROOT, PARENT, APP, preserve


def module(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


build = module('width_build',ROOT/'tools/build.py')
sys.path.insert(0,str(PARENT/'tools'))
shared = module('preserved_checks',PARENT/'tools/check.py')


def main():
    prior_files = preserve()
    failures=[]; references=0; parity=0; classes=set(); target_ids={}
    manifest = json.loads((APP/'kit/component-manifest.json').read_text())
    outputs = build.outputs()
    for name, generated in outputs.items():
        page = ROOT/name
        html = page.read_text(encoding='utf-8')
        if html != generated: failures.append(name+': stale generated HTML')
        scan=shared.Scan(); scan.feed(html); classes.update(scan.classes)
        failures.extend(name+': '+issue for issue in shared.markup_issues(html))
        failures.extend(name+': duplicate ID '+key for key,count in Counter(scan.ids).items() if count>1)
        failures.extend(name+': unbound label/description/form '+key for key in scan.linked if key not in scan.ids)
        if scan.styles or scan.handlers: failures.append(name+': inline styles/handlers')
        for ref in scan.refs:
            target=shared.target_file(page,ref)
            if target is None: continue
            references+=1; path,fragment=target
            if not path.is_file(): failures.append(name+': missing '+ref); continue
            if fragment and path.suffix=='.html':
                if path not in target_ids:
                    other=shared.Scan(); other.feed(path.read_text(encoding='utf-8')); target_ids[path]=set(other.ids)
                if fragment not in target_ids[path]: failures.append(name+': missing fragment '+ref)
    for slug,name,*_ in build.VARIANTS:
        for filename in build.wide.base.PAGES:
            html = (ROOT/slug/filename).read_text(encoding='utf-8')
            html = html.replace(' tide-study--'+slug,'',1).replace('<link rel="stylesheet" href="../widths.css">\n','',1)
            html = html.replace('../../base/','../base/').replace('../../css/studies.css','../css/studies.css').replace('../../js/layout.js','../js/layout.js')
            if html != build.wide.study_page(filename,'workbench','Workbench / '+name):
                failures.append(slug+'/'+filename+': original Workbench markup changed')
            else: parity+=1
    failures.extend(shared.ownership_issues(classes,manifest,{'tide-app','tide-study','tide-study-review'}))
    css=re.sub(r'/\*.*?\*/','',(ROOT/'widths.css').read_text(),flags=re.S)
    declarations=re.findall(r'(?:^|[;{])\s*([\w-]+)\s*:',css)
    for prop in declarations:
        if prop not in {'grid-template-columns','display'} and not prop.startswith('--tide-study-'):
            failures.append('Width CSS changes a non-layout property: '+prop)
    if re.search(r'\.(?:tide-event-|tide-button|tide-field|tide-badge|tide-choice|tide-expandable)',css):
        failures.append('Width CSS targets a shared component')
    preserve()
    report={'pass':not failures,'htmlPages':len(outputs),'localReferences':references,
            'unchangedWorkbenchDocuments':parity,'originalStudyFilesPreserved':prior_files,
            'appFilesLocked':980,'kitFilesLocked':180,'newKitComponents':0,'failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return bool(failures)


if __name__=='__main__': raise SystemExit(main())
