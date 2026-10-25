"""Read-only baseline checks plus HTML/data checks for the separate study."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from urllib.parse import urlsplit,unquote
from datetime import date,datetime
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'shared-filter-release'
KIT=BASE/'kit'
sys.path.insert(0,str(BASE/'tools'))
spec=importlib.util.spec_from_file_location('pressure_baseline_check',BASE/'tools/check.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
sys.path.insert(0,str(KIT/'tools'))
from contracts import markup_issues,ownership_issues
spec=importlib.util.spec_from_file_location('pressure_builder',ROOT/'tools/build.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)

class Scan(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.refs=[];self.bound=[];self.classes=[];self.times=[];self.inline=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        self.classes+=d.get('class','').split()
        for k in ('href','src','action'):
            if d.get(k):self.refs.append(d[k])
        for k in ('for','form','aria-describedby','aria-labelledby'):self.bound+=d.get(k,'').split()
        if tag=='time' and 'datetime' in d:self.times.append(d['datetime'])
        if 'style' in d or any(k.startswith('on') for k in d):self.inline=True

def preserve():
    lock=json.loads((ROOT.parent/'locks/shared-filter-release-1.0.0.json').read_text(encoding='utf-8'))
    current={p.relative_to(BASE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(BASE.rglob('*')) if p.is_file()}
    assert current==lock['files'],'Approved283-file baseline changed'
    accepted=json.loads((ROOT.parent/'locks/event-pressure-test-sticky-0.1.1.json').read_text(encoding='utf-8'))
    for name,digest in accepted['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'Accepted sticky fix changed: '+name
    return {'lockedFiles':len(current),'acceptedStickyFixFiles':len(accepted['files']),'prior':previous.preservation()}

def main():
    preserved=preserve();failures=[];refs=0
    manifest=json.loads((KIT/'component-manifest.json').read_text(encoding='utf-8'))
    private=json.loads((BASE/'consumer-manifest.json').read_text(encoding='utf-8'))['privateBlocks']+['tide-pressure','tide-pressure-review']
    files=list((ROOT/'app').glob('*.html'))+[ROOT/'index.html']
    for p in files:
        text=p.read_text(encoding='utf-8');scan=Scan();scan.feed(text)
        failures.extend(p.name+': '+x for x in markup_issues(text))
        failures.extend(p.name+': '+x for x in ownership_issues(scan.classes,manifest,private))
        failures.extend(p.name+': duplicate ID '+x for x,n in Counter(scan.ids).items() if n>1)
        failures.extend(p.name+': unbound description/form '+x for x in scan.bound if x not in scan.ids)
        if scan.inline:failures.append(p.name+': inline style/handler')
        for t in scan.times:
            try:datetime.fromisoformat(t) if 'T' in t else date.fromisoformat(t)
            except ValueError:failures.append(p.name+': invalid datetime '+t)
        for ref in scan.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p;refs+=1
            if target==ROOT/'qa/checks.json':continue
            if not target.is_file():failures.append(p.name+': missing '+ref)
            elif u.fragment and target.suffix=='.html':
                other=Scan();other.feed(target.read_text(encoding='utf-8'))
                if u.fragment not in other.ids:failures.append(p.name+': missing fragment '+ref)
    events=json.loads((ROOT/'data/events.json').read_text(encoding='utf-8'))
    for e in events:
        if e.get('date') and e.get('endDate') and e['endDate']<e['date']:failures.append('Inverted fixture '+e['id'])
        if e.get('start') and e.get('end') and datetime.fromisoformat(e['start'])>=datetime.fromisoformat(e['end']):failures.append('Inverted instant '+e['id'])
    for id in ('details-tba','postponed','open-end'):
        e=next(e for e in events if e['id']==id);detail=build.detail(e,1)
        if not e.get('price') and '>Free<' in detail:failures.append('Missing price became Free: '+id)
        if not e.get('end') and '2 hours' in detail:failures.append('Invented duration: '+id)
    for id in ('cancelled','postponed','sold-out','ended','removed'):
        e=next(e for e in events if e['id']==id)
        if 'href="#attendance"' in build.detail(e,1):failures.append('Inactive event offers attendance: '+id)
    if (ROOT/'app/css/host.css').read_bytes()!=(BASE/'app/css/host.css').read_bytes():failures.append('Approved base shell CSS drifted')
    for p in (ROOT/'css').glob('*.css'):
        text=re.sub(r'/\*.*?\*/','',p.read_text(encoding='utf-8'),flags=re.S)
        if re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(|oklch\(',text):failures.append('Raw color in '+p.name)
        if re.search(r'\n\s*\.tide-(?:button|notice|event-card|filter-panel)(?:\s|__|--|\{)',text):failures.append('Kit rule overridden in '+p.name)
    run=subprocess.run([sys.executable,'-B','tools/build.py','--check'],cwd=ROOT,capture_output=True,text=True)
    if run.returncode:failures.append(run.stdout+run.stderr)
    preserve()
    report={'pass':not failures,'authoredEvents':len(events),'recoveryScenes':len(build.SCENES),'htmlFiles':len(files),'localReferences':refs,'baselineFilesPreserved':preserved['lockedFiles'],'acceptedStickyFixFilesPreserved':preserved['acceptedStickyFixFiles'],'priorPreservation':preserved['prior'],'baseShellUnchanged':True,'kitEdits':0,'failures':failures}
    (ROOT/'qa/checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='priorPreservation'},indent=2));return bool(failures)

if __name__=='__main__':raise SystemExit(main())
