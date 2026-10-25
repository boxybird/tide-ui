"""Preservation, adoption and consumer HTML checks. Writes only new release QA."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
from zipfile import ZipFile
import hashlib
import json
import re
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
STUDIES=ROOT.parent
WORKSPACE=STUDIES.parent
KIT=ROOT/'kit'
PROTOTYPE=STUDIES/'margin-reveal-unified-search'
sys.path.insert(0,str(PROTOTYPE/'tools'))
from unified_context import verify
sys.path.insert(0,str(KIT/'tools'))
from contracts import markup_issues,ownership_issues

class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.classes=[];self.refs=[];self.linked=[];self.controls=[];self.labels=[];self.cards=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        self.classes.extend(d.get('class','').split())
        for key in ('href','src','action'):
            if d.get(key):self.refs.append(d[key])
        for key in ('for','form','aria-labelledby','aria-describedby'):self.linked+=d.get(key,'').split()
        if tag=='label' and d.get('for'):self.labels.append(d['for'])
        if tag in ('input','select','textarea'):self.controls.append(d)
        self.cards+=int('tide-event-card' in d.get('class','').split())

def preservation():
    preserved=verify()
    original=json.loads((WORKSPACE/'tide-responsive-app/qa/original-kit-lock.json').read_text(encoding='utf-8'))
    for name,expected in original.items():
        assert hashlib.sha256((WORKSPACE/'tide-ui-kit'/name).read_bytes()).hexdigest()==expected,'Original foundation changed: '+name
    archive=PROTOTYPE/'dist/margin-reveal-unified-search-1.0.2.zip'
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest=='1f8226ef94f33fec68671b6f72ac9c0de87fdf2c94554714a95f506e344ac490'
    with ZipFile(archive) as bundle:
        files=json.loads(bundle.read('RELEASE.json'))['files']
        for name,expected in files.items():
            assert hashlib.sha256((PROTOTYPE/name).read_bytes()).hexdigest()==expected,'Prototype changed: '+name
            assert hashlib.sha256(bundle.read(name)).hexdigest()==expected
    return {**preserved,'originalFoundationFiles':len(original),'approvedPrototypeFiles':len(files),'approvedPrototypeArchiveSha256':digest}

def main():
    preserved=preservation();failures=[]
    manifest=json.loads((KIT/'component-manifest.json').read_text(encoding='utf-8'))
    consumer=json.loads((ROOT/'consumer-manifest.json').read_text(encoding='utf-8'))
    old=WORKSPACE/'tide-responsive-app/kit'
    unchanged=['css/tokens.css','tokens/themes.json','css/reset.css','css/base.css','css/layout.css','css/components.css','css/patterns.css','css/content.css','css/utilities.css']
    for name in unchanged:
        if (KIT/name).read_bytes()!=(old/name).read_bytes():failures.append('Existing kit input changed: '+name)
    previous=json.loads((old/'component-manifest.json').read_text(encoding='utf-8'))
    newblocks={c['block'] for c in manifest['components']}-{c['block'] for c in previous['components']}
    if newblocks!={'tide-filter-panel'}:failures.append('Unexpected new component set')
    htmlfiles=list((ROOT/'app').glob('*.html'));refs=0
    for path in htmlfiles:
        text=path.read_text(encoding='utf-8');scan=Scan();scan.feed(text)
        failures.extend(path.name+': '+e for e in markup_issues(text))
        failures.extend(path.name+': '+e for e in ownership_issues(scan.classes,manifest,consumer['privateBlocks']))
        failures.extend(path.name+': duplicate ID '+key for key,n in Counter(scan.ids).items() if n>1)
        failures.extend(path.name+': unbound label/form/description '+key for key in scan.linked if key not in scan.ids)
        for d in scan.controls:
            if not (d.get('aria-label') or d.get('aria-labelledby') or d.get('id') in scan.labels or d.get('type')=='checkbox'):failures.append(path.name+': unlabelled control')
        if 'id="event-search-form"' in text:
            if scan.ids.count('event-query')!=1 or scan.cards!=48:failures.append(path.name+': duplicated controls or event data drift')
            if '../kit/css/tide.css' not in text or 'tide-filter-panel__footer' not in text:failures.append(path.name+': missing shared component')
        if re.search(r'\s(?:style|on\w+)=',text):failures.append(path.name+': inline style/handler')
        for ref in scan.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc:continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            refs+=1
            if not target.is_file():failures.append(path.name+': missing reference '+ref)
            elif url.fragment and target.suffix=='.html':
                other=Scan();other.feed(target.read_text(encoding='utf-8'))
                if url.fragment not in other.ids:failures.append(path.name+': missing fragment '+ref)
    host=(ROOT/'app/css/host.css').read_text(encoding='utf-8')
    host=re.sub(r'/\*.*?\*/','',host,flags=re.S)
    if re.search(r'\.tide-filter-panel(?:__|--|\b)',host):failures.append('Shared panel selectors redefined in consumer CSS')
    app_sources='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'app').rglob('*') if p.suffix in ('.html','.css','.js'))
    for obsolete in ['tide-responsive-filters__','tide-shell__filter-scroll','tide-shell__action-dock','tide-shell__rail','tide-slide-study__scroller','tide-browse-flyout__body','tide-unified-search__status-row','tide-unified-search__count','tide-unified-search__apply']:
        if obsolete in app_sources:failures.append('Extracted private alias remains: '+obsolete)
    if (ROOT/'app/js/assets/organizer-upload.png').read_bytes()!=(STUDIES/'lineup-reading-widths/assets/organizer-upload.png').read_bytes():failures.append('Organizer photo mismatch')
    runs=[]
    for directory,args in [(KIT,['tools/build.py','--check']),(KIT,['tools/check.py']),(KIT,['-m','unittest','discover','-s','tools','-p','test_*.py']),(ROOT,['tools/build_app.py','--check'])]:
        result=subprocess.run([sys.executable,'-B',*args],cwd=directory,capture_output=True,text=True)
        runs.append({'command':'python -B '+' '.join(args),'cwd':str(directory.relative_to(ROOT)) or '.','exitCode':result.returncode,'output':(result.stdout+result.stderr).strip()})
        if result.returncode:failures.append('Failed: '+' '.join(args))
    preservation()
    report={'pass':not failures,'date':'2026-10-24','kitVersion':manifest['version'],'newComponents':sorted(newblocks),'primitiveAndExistingComponentSourcesUnchanged':len(unchanged),'themeModes':6,'appPages':len(htmlfiles),'appReferences':refs,'preservation':preserved,'runs':runs,'failures':failures}
    (ROOT/'qa/verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='runs'},indent=2))
    return bool(failures)

if __name__=='__main__':raise SystemExit(main())
