"""Portable source/contract checks; deliberately independent of design archives."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from datetime import datetime
from urllib.parse import urlsplit,unquote
import json
import gzip
import hashlib
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'packages/tide'
sys.path.insert(0,str(KIT/'tools'))
from contracts import markup_issues,ownership_issues,registered_blocks,style_ownership_issues,registry_issues,registry_entries

class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.bound=[];self.classes=[];self.times=[];self.labels=[];self.controls=[];self.images=[];self.fonts=[];self.inline=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        self.classes+=d.get('class','').split()
        for key in ('href','src','action'):
            if d.get(key):self.refs.append(d[key])
        for key in ('for','form','aria-describedby','aria-labelledby','aria-controls','popovertarget','commandfor'):self.bound+=d.get(key,'').split()
        if tag=='label' and d.get('for'):self.labels.append(d['for'])
        if tag in ('input','textarea','select') and d.get('type') not in ('hidden','checkbox','radio'):self.controls.append(d)
        if tag=='time' and d.get('datetime'):self.times.append(d['datetime'])
        if tag=='img':self.images.append(d)
        if tag=='link' and d.get('rel')=='preload' and d.get('as')=='font':self.fonts.append(d)
        if 'style' in d or any(key.startswith('on') for key in d):self.inline=True

def main():
    subprocess.run([sys.executable,'-B',str(ROOT/'tools/build.py'),'--check'],check=True,cwd=ROOT)
    manifest=json.loads((KIT/'component-manifest.json').read_text(encoding='utf-8'))
    private=json.loads((ROOT/'application-kits/lineup/consumer-manifest.json').read_text(encoding='utf-8'))['privateBlocks']
    site_blocks=json.loads((ROOT/'site/component-manifest.json').read_text(encoding='utf-8'))['privateBlocks']
    pages=sorted((ROOT/'build/site').rglob('*.html'))+sorted((ROOT/'build/events').rglob('*.html'))
    cached={};failures=[];refs=0;allclasses=set()
    budgets=json.loads((ROOT/'tools/performance-budgets.json').read_text(encoding='utf-8'))
    for name,limits in budgets['files'].items():
        data=(ROOT/name).read_bytes()
        if len(data)>limits['maxBytes']:failures.append(name+': raw asset budget exceeded')
        if limits.get('maxGzipBytes') and len(gzip.compress(data))>limits['maxGzipBytes']:failures.append(name+': compressed asset budget exceeded')
    for image in json.loads((KIT/'assets/lossless-images.json').read_text(encoding='utf-8'))['images']:
        for key,digest in (('source','sourceSha256'),('served','servedSha256')):
            if hashlib.sha256((KIT/image[key]).read_bytes()).hexdigest()!=image[digest]:failures.append(image[key]+': lossless conversion provenance changed; verify decoded pixels and update the record')
        if (KIT/image['served']).stat().st_size>image['maxBytes']:failures.append(image['served']+': lossless asset budget exceeded')
    def scan(path):
        if path not in cached:
            s=Scan();s.feed(path.read_text(encoding='utf-8'));cached[path]=s
        return cached[path]
    for path in pages:
        text=path.read_text(encoding='utf-8');s=scan(path);name=path.relative_to(ROOT).as_posix();allclasses.update(s.classes)
        if len(gzip.compress(text.encode('utf-8')))>budgets['maxPageGzipBytes']:failures.append(name+': compressed document budget exceeded')
        if any(ref.endswith('/css/tide.css') for ref in s.refs):
            expected=ROOT/'build/tide/assets/fonts/manrope-latin-wght-normal.woff2'
            if len(s.fonts)!=1 or (path.parent/s.fonts[0].get('href','')).resolve()!=expected or s.fonts[0].get('type')!='font/woff2' or 'crossorigin' not in s.fonts[0]:failures.append(name+': shared local font preload missing or incompatible')
        for image in s.images:
            if not all(re.fullmatch(r'[1-9][0-9]*',image.get(key,'')) for key in ('width','height')):failures.append(name+': image intrinsic dimensions missing')
            source=urlsplit(image.get('src',''))
            if source.scheme or source.netloc:continue
            target=(path.parent/unquote(source.path)).resolve()
            if target.is_file() and target.is_relative_to(ROOT):
                limit=budgets['imageExceptions'].get(target.relative_to(ROOT).as_posix(),budgets['maxServedImageBytes'])
                if target.stat().st_size>limit:failures.append(name+': served image budget exceeded: '+source.path)
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
            fixture_routes=json.loads((ROOT/'application-kits/lineup/data/pages.json').read_text(encoding='utf-8'))
            fixture_events=json.loads((ROOT/'application-kits/lineup/data/events.json').read_text(encoding='utf-8'))
            route=fixture_routes.get(path.stem,{})
            state=route.get('sampleFilter',{})
            venue=route.get('venue') or next((e['venue'] for e in fixture_events if e['id']==path.stem),None)
            expected=0 if state.get('empty') else sum((not venue or e['venue']==venue) and (not state.get('category') or e['category']==state['category']) for e in fixture_events)
            if s.classes.count('tide-event-card')!=expected:failures.append(name+': sample count drift')
            if s.ids.count('event-query')!=1 or 'tide-lineup__feed' not in s.classes:failures.append(name+': control/stacking owner missing')
    for name in ('base','layout','components','patterns','content','filter-panel','page-patterns','utilities'):
        css=(KIT/'css'/f'{name}.css').read_text(encoding='utf-8')
        if re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(|oklch\(|data-theme|--tide-palette-',css):failures.append(name+': theme input leaked into component source')
    for path in (ROOT/'build').rglob('*.css'):
        css=path.read_text(encoding='utf-8')
        for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css):
            if not urlsplit(ref).scheme:
                target=(path.parent/ref).resolve()
                if not target.is_file():failures.append(str(path.relative_to(ROOT))+': missing CSS asset '+ref)
                elif target.suffix in ('.png','.webp','.jpg','.jpeg') and target.is_relative_to(ROOT):
                    limit=budgets['imageExceptions'].get(target.relative_to(ROOT).as_posix(),budgets['maxServedImageBytes'])
                    if target.stat().st_size>limit:failures.append(str(path.relative_to(ROOT))+': CSS image budget exceeded: '+ref)
    failures+=registry_issues(manifest,KIT)
    for c in registry_entries(manifest):
        if c['block'] not in allclasses:failures.append('No specimen for '+c['block'])
        if c.get('source') and not(KIT/c['source']).is_file():failures.append('Missing component source: '+c['block'])
        fixture=c.get('fixture')
        if not fixture or '..' in fixture.split('/'):continue
        target=ROOT/'build/site/index.html' if fixture=='library' else ROOT/'build/site'/fixture if fixture.startswith('extensions/') else ROOT/'build/site/tide-dark/frames'/fixture
        if not target.is_file():failures.append('Missing component fixture: '+c['block'])
        else:
            fixture_html=target.read_text(encoding='utf-8')
            if not re.search(r'(?<![\w-])'+re.escape(c['block'])+r'(?![\w-])',fixture_html):failures.append('Registered fixture omits block: '+c['block'])
    for pattern in manifest.get('patterns',[]):
        if not(KIT/pattern['contract'].split('#')[0]).is_file():failures.append('Missing pattern contract: '+pattern['name'])
        failures.extend('Unknown pattern block '+block for block in pattern['uses'] if block not in registered_blocks(manifest))
    roles=set(next(iter(json.loads((ROOT/'build/tide/tokens/resolved.json').read_text(encoding='utf-8')).values()))['light'])
    for c in manifest['components']:failures.extend(c['block']+': unknown semantic role '+role for role in c.get('roles',[]) if role not in roles)
    kitcss='\n'.join(p.read_text(encoding='utf-8') for p in (KIT/'css').glob('*.css'))+(ROOT/'build/tide/css/themes.css').read_text(encoding='utf-8')+(KIT/'extensions/panel.css').read_text(encoding='utf-8')
    declared=set(re.findall(r'(--tide-[\w-]+)\s*:',kitcss));consumed=set(re.findall(r'var\((--tide-[\w-]+)',kitcss))
    failures.extend('Unbound kit CSS token: '+token for token in sorted(consumed-declared))
    markdown_refs=0
    markdown=[ROOT/name for name in ('README.md','CONTRIBUTING.md','CHANGELOG.md')]+[KIT/'README.md',ROOT/'application-kits/lineup/README.md']
    markdown += [ROOT/'application-kits/README.md']
    markdown+=list((ROOT/'docs').rglob('*.md'))+list((KIT/'docs').glob('*.md'))+list((ROOT/'application-kits/lineup/docs').glob('*.md'))
    markdown+=list((ROOT/'build').rglob('*.md'))
    for path in markdown:
        for ref in re.findall(r'\]\((<[^>]+>|[^)]+)\)',path.read_text(encoding='utf-8')):
            ref=ref.removeprefix('<').removesuffix('>')
            url=urlsplit(ref)
            if url.scheme or url.netloc or not url.path:continue
            markdown_refs+=1
            if not(path.parent/unquote(url.path)).resolve().is_file():failures.append(str(path.relative_to(ROOT))+': missing documentation link '+ref)
    appcss='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'application-kits/lineup/src/styles').glob('*.css'))
    failures+=style_ownership_issues(appcss,manifest)
    if not re.search(r'\.tide-lineup__feed\s*\{\s*isolation:\s*isolate;',appcss):failures.append('Accepted feed isolation missing')
    # Private app selectors have one current home, never inherited study aliases.
    app_source=ROOT/'application-kits/lineup/src'
    usage='\n'.join(p.read_text(encoding='utf-8') for p in app_source.rglob('*') if p.suffix in ('.html','.js'))
    usage+=(ROOT/'application-kits/lineup/tools/build.py').read_text(encoding='utf-8')
    # Template context can compose a class that is absent from literal markup.
    usage+='\n'+' '.join(allclasses)
    for p in app_source.rglob('*'):
        if p.suffix in ('.html','.js','.css') and re.search(r'\btide-(?:[\w-]*study[\w-]*|shell(?:-document)?)(?:__[\w-]+)?\b',p.read_text(encoding='utf-8')):
            failures.append(str(p.relative_to(ROOT))+': historical app selector returned')
    for p in (app_source/'pages').glob('*.html'):
        source=p.read_text(encoding='utf-8')
        if re.search(r'<!doctype|</?(?:html|head|body)\b|<script\b|{{> header}}',source,re.I):
            failures.append(str(p.relative_to(ROOT))+': unique content belongs inside the shared document')
        if re.search(r'<(?:header|form|article|dialog|aside|section|main|footer|div)\s+class="(?:tide-app__header|tide-app__search|tide-event-card\b|tide-filter-panel|tide-app__filter-rail|tide-event-hero\b|tide-event-details\b|tide-app__workspace|tide-app__preview-state|tide-app__site-footer|tide-field\b)',source):
            failures.append(str(p.relative_to(ROOT))+': duplicated shared app markup; use its partial')
    for cls in set(re.findall(r'\.(tide-[\w-]+(?:__[\w-]+)?)',appcss)):
        if any(cls==block or cls.startswith(block+'__') or cls.startswith(block+'--') for block in private) and not re.search(r'(?<![\w-])'+re.escape(cls)+r'(?![\w-])',usage):
            failures.append('Unused private app selector: '+cls)
    # All emitted theme/mode screen bodies remain identical apart from paths.
    signatures={}
    for path in (ROOT/'build/site').glob('*/frames/*.html'):
        body=re.search(r'<body\b.*</body>',path.read_text(encoding='utf-8'),re.S).group()
        normalized=re.sub(r'(?:\.\./)+tide/assets/','assets/',body)
        if signatures.setdefault(path.name,normalized)!=normalized:failures.append('Theme specimen structure differs: '+path.name)
    runs=[]
    http_tests=subprocess.run([shutil.which('node') or 'node','--test','tools/test-serve.cjs'],cwd=ROOT,capture_output=True,text=True)
    runs.append({'name':'preview-http-contracts','pass':http_tests.returncode==0,'output':(http_tests.stdout+http_tests.stderr).strip()})
    tests=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tools','-p','test_*.py'],cwd=KIT,capture_output=True,text=True)
    runs.append({'name':'palette-and-contract-tests','pass':tests.returncode==0,'output':(tests.stdout+tests.stderr).strip()})
    templates=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tools','-p','test_*.py'],cwd=ROOT/'application-kits/lineup',capture_output=True,text=True)
    runs.append({'name':'app-template-contracts','pass':templates.returncode==0,'output':(templates.stdout+templates.stderr).strip()})
    map_tests=subprocess.run([shutil.which('node') or 'node','--test','application-kits/lineup/tools/test-map.cjs'],cwd=ROOT,capture_output=True,text=True)
    runs.append({'name':'lineup-map-contracts','pass':map_tests.returncode==0,'output':(map_tests.stdout+map_tests.stderr).strip()})
    # The approved Lineup map is the only browser-runtime exception. Tide,
    # reference specimens and every other Lineup route remain script-free.
    app=ROOT/'application-kits/lineup'
    consumer=json.loads((app/'consumer-manifest.json').read_text(encoding='utf-8'))
    allowed_scripts={app/name for name in consumer['behaviorHome']}
    allowed_scripts.update(ROOT/'build/events/runtime/map'/p.relative_to(app/'src/map') for p in list(allowed_scripts))
    for folder in (KIT/'templates', KIT/'css', KIT/'assets', ROOT/'site', ROOT/'application-kits/lineup/src', ROOT/'build/tide', ROOT/'build/site', ROOT/'build/events'):
        for p in folder.rglob('*'):
            if not p.is_file():continue
            if p.suffix.lower() in ('.js','.mjs','.cjs') and p not in allowed_scripts:
                failures.append(str(p.relative_to(ROOT))+': unregistered browser JavaScript is forbidden')
            if p.suffix.lower() in ('.html','.svg'):
                text=p.read_text(encoding='utf-8')
                if p.is_relative_to(ROOT/'build/events') and p.name=='venues.html':
                    expected=(p.parent/'../runtime/map/venue-map.mjs').resolve() if p.parent.name=='app' else (p.parent/'../../runtime/map/venue-map.mjs').resolve()
                    tags=re.findall(r'<script\b[^>]*>.*?</script>',text,re.S|re.I)
                    for tag in tags:
                        match=re.fullmatch(r'<script type="module" src="([^"]+)"></script>',tag)
                        if match and (p.parent/match[1]).resolve()==expected:
                            text=text.replace(tag,'',1)
                    if len(tags)!=1:failures.append(str(p.relative_to(ROOT))+': exactly one registered map entry module required')
                if re.search(r'<script\b|\son[a-z]+\s*=|(?:href|src)\s*=\s*[\"\']\s*javascript:',text,re.I):
                    failures.append(str(p.relative_to(ROOT))+': executable browser dependency is forbidden')
    failures.extend(run['name']+' failed: '+run['output'] for run in runs if not run['pass'])
    report={'pass':not failures,'kitVersion':manifest['version'],'htmlFiles':len(pages),'localReferences':refs,'markdownReferences':markdown_refs,'themes':len(json.loads((KIT/'tokens/themes.json').read_text(encoding='utf-8'))['themes']),'modesPerTheme':2,'runs':runs,'failures':failures}
    out=ROOT/'build/reports';out.mkdir(parents=True,exist_ok=True)
    (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));return bool(failures)

if __name__=='__main__':raise SystemExit(main())
