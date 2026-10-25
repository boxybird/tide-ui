"""Portable source/contract checks; deliberately independent of design archives."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from datetime import datetime
from urllib.parse import urlsplit,unquote
import json
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'packages/tide'
sys.path.insert(0,str(KIT/'tools'))
from contracts import markup_issues,ownership_issues,registered_blocks,style_ownership_issues

class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.bound=[];self.classes=[];self.times=[];self.labels=[];self.controls=[];self.inline=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        self.classes+=d.get('class','').split()
        for key in ('href','src','action'):
            if d.get(key):self.refs.append(d[key])
        for key in ('for','form','aria-describedby','aria-labelledby','aria-controls'):self.bound+=d.get(key,'').split()
        if tag=='label' and d.get('for'):self.labels.append(d['for'])
        if tag in ('input','textarea','select') and d.get('type') not in ('hidden','checkbox','radio'):self.controls.append(d)
        if tag=='time' and d.get('datetime'):self.times.append(d['datetime'])
        if 'style' in d or any(key.startswith('on') for key in d):self.inline=True

def main():
    subprocess.run([sys.executable,'-B',str(ROOT/'tools/build.py'),'--check'],check=True,cwd=ROOT)
    manifest=json.loads((KIT/'component-manifest.json').read_text(encoding='utf-8'))
    private=json.loads((ROOT/'examples/events/consumer-manifest.json').read_text(encoding='utf-8'))['privateBlocks']
    site_blocks=json.loads((ROOT/'site/component-manifest.json').read_text(encoding='utf-8'))['privateBlocks']
    pages=sorted((ROOT/'build/site').rglob('*.html'))+sorted((ROOT/'build/events').rglob('*.html'))
    cached={};failures=[];refs=0;allclasses=set()
    def scan(path):
        if path not in cached:
            s=Scan();s.feed(path.read_text(encoding='utf-8'));cached[path]=s
        return cached[path]
    for path in pages:
        text=path.read_text(encoding='utf-8');s=scan(path);name=path.relative_to(ROOT).as_posix();allclasses.update(s.classes)
        failures.extend(name+': '+i for i in markup_issues(text))
        for cls in s.classes:
            if cls!='tide' and not re.fullmatch(r'tide(?:-[a-z0-9]+)+(?:__[a-z0-9]+(?:-[a-z0-9]+)*)?(?:--[a-z0-9]+(?:-[a-z0-9]+)*)?',cls):failures.append(name+': invalid BEM name '+cls)
        allowed=site_blocks if path.is_relative_to(ROOT/'build/site') else private
        failures.extend(name+': '+i for i in ownership_issues(s.classes,manifest,allowed))
        failures.extend(name+': duplicate ID '+i for i,n in Counter(s.ids).items() if n>1)
        failures.extend(name+': missing association '+i for i in s.bound if i not in s.ids)
        if s.inline:failures.append(name+': inline style/handler')
        for d in s.controls:
            if not(d.get('aria-label') or d.get('aria-labelledby') or d.get('id') in s.labels):failures.append(name+': unlabelled control')
        for t in s.times:
            try:datetime.fromisoformat(t)
            except ValueError:failures.append(name+': invalid time '+t)
        for ref in s.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc:continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path;refs+=1
            if not target.is_file():failures.append(name+': missing '+ref)
            elif url.fragment and target.suffix=='.html' and url.fragment not in scan(target).ids:failures.append(name+': missing fragment '+ref)
        if 'event-search-form' in s.ids:
            expected=6 if path.name=='sunshine-theater.html' else 54
            if s.classes.count('tide-event-card')!=expected:failures.append(name+': sample count drift')
            if s.ids.count('event-query')!=1 or 'tide-lineup__feed' not in s.classes:failures.append(name+': control/stacking owner missing')
    for name in ('base','layout','components','patterns','content','filter-panel','utilities'):
        css=(KIT/'css'/f'{name}.css').read_text(encoding='utf-8')
        if re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(|oklch\(|data-theme|--tide-palette-',css):failures.append(name+': theme input leaked into component source')
    for path in (ROOT/'build').rglob('*.css'):
        css=path.read_text(encoding='utf-8')
        for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css):
            if not urlsplit(ref).scheme and not(path.parent/ref).resolve().is_file():failures.append(str(path.relative_to(ROOT))+': missing CSS asset '+ref)
    for c in manifest['components']:
        if c['block'] not in allclasses:failures.append('No specimen for '+c['block'])
        if c.get('source') and not(KIT/c['source']).is_file():failures.append('Missing component source: '+c['block'])
        fixture=c['fixture']
        target=ROOT/'build/site/index.html' if fixture=='library' else ROOT/'build/site'/fixture if fixture.startswith('extensions/') else ROOT/'build/site/tide-dark/frames'/fixture
        if not target.is_file():failures.append('Missing component fixture: '+c['block'])
    for c in manifest.get('supportingBlocks',[]):
        if not(KIT/c['source']).is_file():failures.append('Missing supporting source: '+c['block'])
    for pattern in manifest.get('patterns',[]):
        if not(KIT/pattern['contract'].split('#')[0]).is_file():failures.append('Missing pattern contract: '+pattern['name'])
        failures.extend('Unknown pattern block '+block for block in pattern['uses'] if block not in registered_blocks(manifest))
    roles=set(next(iter(json.loads((ROOT/'build/tide/tokens/resolved.json').read_text(encoding='utf-8')).values()))['light'])
    for c in manifest['components']:failures.extend(c['block']+': unknown semantic role '+role for role in c.get('roles',[]) if role not in roles)
    kitcss='\n'.join(p.read_text(encoding='utf-8') for p in (KIT/'css').glob('*.css'))+(ROOT/'build/tide/css/themes.css').read_text(encoding='utf-8')+(KIT/'extensions/panel.css').read_text(encoding='utf-8')
    declared=set(re.findall(r'(--tide-[\w-]+)\s*:',kitcss));consumed=set(re.findall(r'var\((--tide-[\w-]+)',kitcss))
    failures.extend('Unbound kit CSS token: '+token for token in sorted(consumed-declared))
    markdown_refs=0
    markdown=[ROOT/name for name in ('README.md','CONTRIBUTING.md','CHANGELOG.md')]+[KIT/'README.md',ROOT/'examples/events/README.md']
    markdown+=list((ROOT/'docs').rglob('*.md'))+list((KIT/'docs').glob('*.md'))+list((ROOT/'examples/events/docs').glob('*.md'))
    markdown+=list((ROOT/'build').rglob('*.md'))
    for path in markdown:
        for ref in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            url=urlsplit(ref)
            if url.scheme or url.netloc or not url.path:continue
            markdown_refs+=1
            if not(path.parent/unquote(url.path)).resolve().is_file():failures.append(str(path.relative_to(ROOT))+': missing documentation link '+ref)
    appcss='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'examples/events/src/styles').glob('*.css'))
    failures+=style_ownership_issues(appcss,manifest)
    if not re.search(r'\.tide-lineup__feed\s*\{\s*isolation:\s*isolate;',appcss):failures.append('Accepted feed isolation missing')
    # Private app selectors have one current home, never inherited study aliases.
    app_source=ROOT/'examples/events/src'
    usage='\n'.join(p.read_text(encoding='utf-8') for p in app_source.rglob('*') if p.suffix in ('.html','.js'))
    usage+=(ROOT/'examples/events/tools/build.py').read_text(encoding='utf-8')
    for p in app_source.rglob('*'):
        if p.suffix in ('.html','.js','.css') and re.search(r'\btide-(?:[\w-]*study[\w-]*|shell(?:-document)?)(?:__[\w-]+)?\b',p.read_text(encoding='utf-8')):
            failures.append(str(p.relative_to(ROOT))+': historical app selector returned')
    for cls in set(re.findall(r'\.(tide-[\w-]+(?:__[\w-]+)?)',appcss)):
        if any(cls==block or cls.startswith(block+'__') or cls.startswith(block+'--') for block in private) and not re.search(r'(?<![\w-])'+re.escape(cls)+r'(?![\w-])',usage):
            failures.append('Unused private app selector: '+cls)
    # All emitted six-mode screen bodies remain identical apart from paths.
    signatures={}
    for path in (ROOT/'build/site').glob('*/frames/*.html'):
        body=re.search(r'<body\b.*</body>',path.read_text(encoding='utf-8'),re.S).group()
        normalized=re.sub(r'(?:\.\./)+tide/assets/','assets/',body)
        if signatures.setdefault(path.name,normalized)!=normalized:failures.append('Theme specimen structure differs: '+path.name)
    runs=[]
    tests=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tools','-p','test_*.py'],cwd=KIT,capture_output=True,text=True)
    runs.append({'name':'palette-and-contract-tests','pass':tests.returncode==0,'output':(tests.stdout+tests.stderr).strip()})
    node=shutil.which('node')
    assert node,'Node.js is required for the sample search assertions'
    search=subprocess.run([node,str(ROOT/'examples/events/tools/test-search.cjs')],cwd=ROOT,capture_output=True,text=True)
    runs.append({'name':'sample-search-tests','pass':search.returncode==0,'output':(search.stdout+search.stderr).strip()})
    failures.extend(run['name']+' failed: '+run['output'] for run in runs if not run['pass'])
    report={'pass':not failures,'kitVersion':manifest['version'],'htmlFiles':len(pages),'localReferences':refs,'markdownReferences':markdown_refs,'themes':3,'modesPerTheme':2,'runs':runs,'failures':failures}
    out=ROOT/'build/reports';out.mkdir(parents=True,exist_ok=True)
    (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)

if __name__=='__main__':raise SystemExit(main())
