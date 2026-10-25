"""Source and preservation checks; all report writes stay in this study."""
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from urllib.parse import urlsplit,unquote
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'shared-filter-release'
spec=importlib.util.spec_from_file_location('venue_preservation',ROOT.parent/'event-pressure-test/tools/check.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

def main():
    preservation=prior.preserve();failures=[];refs=0
    manifest=json.loads((BASE/'kit/component-manifest.json').read_text(encoding='utf-8'))
    private=json.loads((BASE/'consumer-manifest.json').read_text(encoding='utf-8'))['privateBlocks']+['tide-venue-study']
    pages=list((ROOT/'app').glob('*.html'))+[ROOT/'index.html']
    for p in pages:
        text=p.read_text(encoding='utf-8');scan=prior.Scan();scan.feed(text)
        failures.extend(p.name+': '+s for s in prior.markup_issues(text))
        failures.extend(p.name+': '+s for s in prior.ownership_issues(scan.classes,manifest,private))
        failures.extend(p.name+': duplicate ID '+s for s,n in Counter(scan.ids).items() if n>1)
        failures.extend(p.name+': missing association '+s for s in scan.bound if s not in scan.ids)
        if scan.inline:failures.append(p.name+': inline style or handler')
        for time in scan.times:
            try:datetime.fromisoformat(time)
            except ValueError:failures.append(p.name+': invalid date/time '+time)
        for ref in scan.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc:continue
            refs+=1;target=(p.parent/unquote(url.path)).resolve() if url.path else p
            if target==ROOT/'qa/checks.json':continue
            if not target.is_file():failures.append(p.name+': missing '+ref)
            elif url.fragment and target.suffix=='.html':
                other=prior.Scan();other.feed(target.read_text(encoding='utf-8'))
                if url.fragment not in other.ids:failures.append(p.name+': missing fragment '+ref)
        if 'id="event-search-form"' in text and 'tide-venue-study__feed' not in scan.classes:failures.append(p.name+': accepted feed isolation missing')
    if (ROOT/'app/css/host.css').read_bytes()!=(BASE/'app/css/host.css').read_bytes():failures.append('Base host CSS drifted')
    css=(ROOT/'css/venue.css').read_text(encoding='utf-8')
    if re.search(r'#[\da-fA-F]{3,8}\b|rgba?\(|oklch\(',css):failures.append('New raw color input')
    if not re.search(r'\.tide-venue-study__feed\s*\{\s*isolation:\s*isolate;\s*\}',css):failures.append('Sticky hierarchy contract missing')
    for block in re.findall(r'([^{}]+)\{[^{}]*\}',re.sub(r'/\*.*?\*/','',css,flags=re.S)):
        if '.' in block and '.tide-venue-study' not in block:failures.append('Rule outside private composition: '+block.strip())
    page=(ROOT/'app/sunshine-theater.html').read_text(encoding='utf-8')
    if len(re.findall(r'<article class="tide-event-card\b',page))!=6:failures.append('Venue source must contain six scoped sample cards')
    if 'data-venue="other"' in page:failures.append('Venue source includes unrelated events')
    if 'Sample schedule' not in page or 'not Sunshine Theater' not in page:failures.append('Sample/live data distinction missing')
    run=subprocess.run([sys.executable,'-B','tools/build.py','--check'],cwd=ROOT,capture_output=True,text=True)
    if run.returncode:failures.append(run.stdout+run.stderr)
    prior.preserve()
    report={'pass':not failures,'htmlFiles':len(pages),'localReferences':refs,'globalEvents':54,'venueSampleEvents':6,'baselineFilesPreserved':preservation['lockedFiles'],'acceptedStickyFixFilesPreserved':preservation['acceptedStickyFixFiles'],'baseHostUnchanged':True,'kitEdits':0,'failures':failures}
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)

if __name__=='__main__':raise SystemExit(main())
