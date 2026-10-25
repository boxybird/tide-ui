"""Successor checks. Dependencies are read-only; reports stay in this release."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from datetime import datetime
from urllib.parse import urlsplit, unquote
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
STUDIES = ROOT.parent
BASE = STUDIES / 'shared-filter-release'
KIT = BASE / 'kit'
from build import build
sys.path.insert(0, str(KIT / 'tools'))
from contracts import markup_issues, ownership_issues

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def preservation():
    spec=importlib.util.spec_from_file_location('successor_readonly_preservation',STUDIES/'event-pressure-test/tools/check.py')
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    preserved=prior.preserve()
    venue=STUDIES/'venue-discovery'
    lock=json.loads((STUDIES/'locks/venue-discovery-0.1.0.json').read_text(encoding='utf-8'))['files']
    current={p.relative_to(venue).as_posix():sha(p) for p in sorted(venue.rglob('*')) if p.is_file()}
    assert current==lock, 'Preserved venue study changed, including added/removed files'
    return {**preserved,'venueStudyFiles':len(current),'kitEdits':0,'preservedTreeEdits':0}

class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.bound=[];self.classes=[];self.times=[];self.inline=False;self.h1=0;self.main=0;self.labels=[];self.controls=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        self.classes+=d.get('class','').split()
        for k in ('href','src','action'):
            if d.get(k):self.refs.append(d[k])
        for k in ('for','form','aria-describedby','aria-labelledby','aria-controls'):self.bound+=d.get(k,'').split()
        if tag=='label' and d.get('for'):self.labels.append(d['for'])
        if tag in ('input','textarea','select') and d.get('type') not in ('hidden','checkbox','radio'):self.controls.append(d)
        if tag=='time' and 'datetime' in d:self.times.append(d['datetime'])
        if 'style' in d or any(k.startswith('on') for k in d):self.inline=True
        self.h1+=tag=='h1';self.main+=tag=='main'

def main():
    failures=[];preserved=preservation();build(check=True)
    manifest=json.loads((KIT/'component-manifest.json').read_text(encoding='utf-8'))
    private=json.loads((ROOT/'consumer-manifest.json').read_text(encoding='utf-8'))['privateBlocks']
    pages=sorted((ROOT/'app').glob('*.html'))+sorted((ROOT/'themes').rglob('*.html'))+[ROOT/'index.html']
    scans={}
    def scan(path):
        if path not in scans:
            parser=Scan();parser.feed(path.read_text(encoding='utf-8'));scans[path]=parser
        return scans[path]
    refs=0
    for path in pages:
        text=path.read_text(encoding='utf-8');s=scan(path);name=path.relative_to(ROOT).as_posix()
        failures.extend(name+': '+issue for issue in markup_issues(text))
        failures.extend(name+': '+issue for issue in ownership_issues(s.classes,manifest,private))
        failures.extend(name+': duplicate ID '+key for key,n in Counter(s.ids).items() if n>1)
        failures.extend(name+': unbound ID '+key for key in s.bound if key not in s.ids)
        if s.h1!=1 or s.main!=1:failures.append(name+': requires one H1 and main')
        if s.inline:failures.append(name+': inline style/handler')
        for d in s.controls:
            if not (d.get('aria-label') or d.get('aria-labelledby') or d.get('id') in s.labels):failures.append(name+': unlabelled control')
        for t in s.times:
            try:datetime.fromisoformat(t)
            except ValueError:failures.append(name+': invalid time '+t)
        for ref in s.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            refs+=1;target=(path.parent/unquote(u.path)).resolve() if u.path else path
            if not target.is_file():failures.append(name+': missing '+ref)
            elif u.fragment and target.suffix=='.html' and u.fragment not in scan(target).ids:failures.append(name+': missing fragment '+ref)
        if 'event-search-form' in s.ids:
            count=6 if path.name=='sunshine-theater.html' else 54
            if s.classes.count('tide-event-card')!=count:failures.append(name+': card count drift')
            if 'tide-app-release__feed' not in s.classes:failures.append(name+': feed isolation owner missing')
            if s.ids.count('event-query')!=1:failures.append(name+': duplicate original search controls')
    if (ROOT/'runtime/css/host.css').read_bytes()!=(BASE/'app/css/host.css').read_bytes():failures.append('Baseline host CSS changed')
    css=(ROOT/'runtime/css/app.css').read_text(encoding='utf-8')
    if re.search(r'#[\da-fA-F]{3,8}\b|rgba?\(|oklch\(',css):failures.append('Raw palette introduced')
    if not re.search(r'\.tide-app-release__feed\s*\{\s*isolation:\s*isolate;\s*\}',css):failures.append('Accepted isolated feed missing')
    source='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'src').rglob('*') if p.suffix in ('.html','.css','.js'))
    if 'tide-venue-study' in source or 'tide-pressure__' in source:failures.append('Obsolete experimental owner remains')
    for d in (ROOT/'themes').iterdir():
        t,m=d.name.split('-');text=(d/'index.html').read_text(encoding='utf-8')
        if f'data-theme="{t}"' not in text or f'data-mode="{m}"' not in text:failures.append('Theme routing mismatch '+d.name)
    node='C:/Users/andre/AppData/Local/pnpm/bin/node.EXE'
    test=subprocess.run([node,'tools/test-search.cjs'],cwd=ROOT,capture_output=True,text=True)
    if test.returncode:failures.append(test.stdout+test.stderr)
    preserved=preservation()
    report={'pass':not failures,'date':'2026-10-25','appVersion':'1.1.0','kitVersion':'1.3.0','htmlFiles':len(pages),'localReferences':refs,'themeModes':6,'globalSampleEvents':54,'sunshineSampleEvents':6,'baseHostUnchanged':True,'searchAssertions':test.stdout.strip(),'preservation':preserved,'failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)

if __name__=='__main__':
    raise SystemExit(main())
