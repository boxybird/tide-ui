"""Validate the review and preservation without writing frozen kit QA."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import urlsplit,unquote
import hashlib
import importlib.util
import json
import posixpath
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
STUDIES=ROOT.parent
WORKSPACE=STUDIES.parent
APP=WORKSPACE/'tide-responsive-app'
KIT=APP/'kit'
PROTOTYPE=STUDIES/'margin-reveal-unified-search'
sys.path.insert(0,str(PROTOTYPE/'tools'))
from unified_context import verify
sys.path.insert(0,str(KIT/'tools'))
from contracts import markup_issues,ownership_issues,registered_blocks

class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.classes=[];self.refs=[];self.linked=[];self.handlers=0;self.controls=[];self.labels=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        self.classes.extend(d.get('class','').split())
        self.handlers+=int(tag=='script' or 'style' in d or any(k.startswith('on') for k in d))
        for key in ('href','src'):
            if d.get(key):self.refs.append(d[key])
        for key in ('for','form','aria-labelledby','aria-describedby'):self.linked.extend(d.get(key,'').split())
        if tag=='label' and d.get('for'):self.labels.append(d['for'])
        if tag in ('input','select','textarea'):self.controls.append(d)

def load_builder():
    spec=importlib.util.spec_from_file_location('search_filter_review_builder',ROOT/'build.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def kit_checks():
    inventory=json.loads((STUDIES/'locks/kit-1.2.1.json').read_text(encoding='utf-8'))
    digest=hashlib.sha256(json.dumps(inventory,sort_keys=True).encode()).hexdigest()
    record=ROOT/'qa/kit-checks.json'
    if record.exists():
        previous=json.loads(record.read_text(encoding='utf-8'))
        if previous.get('inputDigest')==digest and previous.get('pass'):return previous
    runs=[]
    # This fresh temporary directory is the only recursive-cleanup target.
    with tempfile.TemporaryDirectory(prefix='tide-adoption-check-',dir=ROOT/'qa') as folder:
        temporary=Path(folder).resolve()
        assert temporary.parent==(ROOT/'qa').resolve()
        stage=temporary/'kit';shutil.copytree(KIT,stage)
        commands=[['tools/build.py','--check'],['tools/check.py'],['-m','unittest','discover','-s','tools','-p','test_*.py']]
        for args in commands:
            result=subprocess.run([sys.executable,'-B',*args],cwd=stage,capture_output=True,text=True)
            runs.append({'command':'python -B '+' '.join(args),'exitCode':result.returncode,'output':(result.stdout+result.stderr).strip()})
    report={'pass':all(item['exitCode']==0 for item in runs),'inputDigest':digest,'execution':'Temporary copy only; frozen source and QA files untouched.','runs':runs}
    record.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report

def main():
    (ROOT/'qa').mkdir(exist_ok=True)
    preserved=verify();failures=[]
    checks=kit_checks()
    if not checks['pass']:failures.append('Kit verification failed in isolated copy')
    archive=PROTOTYPE/'dist/margin-reveal-unified-search-1.0.2.zip'
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest==archive.with_name(archive.name+'.sha256').read_text().split()[0]
    with ZipFile(archive) as bundle:
        files=json.loads(bundle.read('RELEASE.json'))['files']
        for name,expected in files.items():
            assert hashlib.sha256(bundle.read(name)).hexdigest()==expected
            assert hashlib.sha256((PROTOTYPE/name).read_bytes()).hexdigest()==expected,'Approved prototype changed: '+name
    manifest=json.loads((KIT/'component-manifest.json').read_text(encoding='utf-8'))
    registered=registered_blocks(manifest)
    decisions=json.loads((ROOT/'decisions.json').read_text(encoding='utf-8'))
    for item in decisions['decisions']:
        failures.extend('Unknown reused block '+block for block in item['reuse'] if block not in registered)
        failures.extend('Missing current source '+name for name in item['currentSources'] if not (WORKSPACE/name).is_file())
    if any(block in registered for block in decisions['newBlockCandidates']):failures.append('Proposal incorrectly marked as shipped')
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    if html!=load_builder().output():failures.append('Review output is stale')
    sample=(ROOT/'examples/combined-form.html.txt').read_text(encoding='utf-8')
    for label,source in [('review',html),('form specimen','<main><h1>Specimen</h1>'+sample+'</main>')]:
        scan=Scan();scan.feed(source)
        failures.extend(label+': '+error for error in markup_issues(source))
        failures.extend(label+': '+error for error in ownership_issues(scan.classes,manifest))
        failures.extend(label+': duplicate ID '+name for name,count in Counter(scan.ids).items() if count>1)
        failures.extend(label+': unbound label/form/description '+name for name in scan.linked if name not in scan.ids)
        if scan.handlers:failures.append(label+': runtime script or inline style/handler')
        if label=='review':
            for ref in scan.refs:
                parsed=urlsplit(ref)
                if parsed.scheme or parsed.netloc:continue
                url=posixpath.normpath(posixpath.join('/kit-adoption-review/',unquote(parsed.path))) if parsed.path else '/kit-adoption-review/index.html'
                target=APP/url[6:] if url.startswith('/base/') else STUDIES/url.lstrip('/')
                if target==ROOT/'qa/preservation.json':continue
                if not target.is_file():failures.append('Missing review reference '+ref)
                elif parsed.fragment:
                    other=Scan();other.feed(target.read_text(encoding='utf-8'))
                    if parsed.fragment not in other.ids:failures.append('Missing review fragment '+ref)
    verify()
    report={'pass':not failures,'date':'2026-10-24','scope':'Companion adoption documentation; no component release','prototypeVersion':'1.0.2','prototypeFilesPreserved':len(files),'prototypeArchiveSha256':digest,'kitFilesPreserved':preserved['kitFiles'],'appFilesPreserved':preserved['appFiles'],'precedingDependencyChainPreserved':True,'decisions':len(decisions['decisions']),'stateRows':len(decisions['states']),'proposedNewBlocks':decisions['newBlockCandidates'],'newComponentsShipped':0,'runtimeChanges':0,'kitChecksPass':checks['pass'],'failures':failures}
    (ROOT/'qa/preservation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)

if __name__=='__main__':raise SystemExit(main())
