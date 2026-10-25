"""Dependency-free checks for the static HTML/CSS contract and local references."""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from contracts import markup_issues,registered_blocks

ROOT=Path(__file__).resolve().parents[1]
BEM=re.compile(r'^tide(?:-[a-z0-9]+)+(?:__[a-z0-9]+(?:-[a-z0-9]+)*)?(?:--[a-z0-9]+(?:-[a-z0-9]+)*)?$')


class Scan(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.classes=[];self.errors=[];self.described=[];self.for_ids=[];self.controls=[];self.labels=0;self.scripts=0;self.inline_styles=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        self.classes.extend(d.get('class','').split())
        if 'style' in d:self.errors.append('Inline style');self.inline_styles+=1
        if tag=='script' or any(k.startswith('on') for k in d):self.errors.append('Browser script / event handler');self.scripts+=1
        for key in ['href','src','action']:
            if d.get(key):self.refs.append(d[key])
        self.described.extend(d.get('aria-describedby','').split())
        self.described.extend(d.get('aria-labelledby','').split())
        if tag=='label':
            self.labels+=1
            if d.get('for'):self.for_ids.append(d['for'])
        if tag in ['input','select','textarea']:
            self.controls.append((tag,d,self.labels>0))
    def handle_endtag(self,tag):
        if tag=='label':self.labels=max(0,self.labels-1)


def main():
    failures=[];files=[];refs=0;signatures={};scripts=0;inline_styles=0;all_classes=set()
    for path in ROOT.rglob('*.html'):
        if 'templates' in path.relative_to(ROOT).parts or 'qa' in path.relative_to(ROOT).parts:continue
        files.append(path);scan=Scan();scan.feed(path.read_text(encoding='utf-8'))
        scripts+=scan.scripts;inline_styles+=scan.inline_styles;all_classes.update(scan.classes)
        local=str(path.relative_to(ROOT))
        failures.extend(f'{local}: {error}' for error in markup_issues(path.read_text(encoding='utf-8')))
        failures.extend(f'{local}: {error}' for error in scan.errors)
        failures.extend(f'{local}: invalid class {cls}' for cls in scan.classes if cls!='tide' and not BEM.fullmatch(cls))
        failures.extend(f'{local}: duplicate ID {key}' for key,count in Counter(scan.ids).items() if count>1)
        failures.extend(f'{local}: unbound description {key}' for key in scan.described if key not in scan.ids)
        failures.extend(f'{local}: unbound label {key}' for key in scan.for_ids if key not in scan.ids)
        for tag,d,wrapped in scan.controls:
            if d.get('type') in ['hidden','submit','button','reset']:continue
            if not (wrapped or d.get('aria-label') or d.get('aria-labelledby') or d.get('id') in scan.for_ids):failures.append(f'{local}: unlabelled {tag}')
        for ref in scan.refs:
            parsed=urlsplit(ref)
            if parsed.scheme or parsed.netloc:continue
            target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            refs+=1
            if not target.is_file():failures.append(f'{local}: missing {ref}')
            elif parsed.fragment and target.suffix=='.html':
                target_scan=Scan();target_scan.feed(target.read_text(encoding='utf-8'))
                if parsed.fragment not in target_scan.ids:failures.append(f'{local}: missing fragment {ref}')
        if path.parent.name=='frames':
            body=re.search(r'<body\b.*</body>',path.read_text(encoding='utf-8'),re.S).group()
            normalized=re.sub(r'(?:\.\./)*assets/','assets/',body)
            old=signatures.setdefault(path.name,normalized)
            if old!=normalized:failures.append(f'{local}: screen structure/content differs across themes')
    # No theme-specific selectors, raw colors or implementation-token consumers in components.
    for name in ['base.css','layout.css','components.css','patterns.css','content.css','filter-panel.css','utilities.css']:
        text=(ROOT/'css'/name).read_text(encoding='utf-8')
        if '--tide-palette-' in text:failures.append(f'{name}: consumes private palette token')
        if re.search(r'#[0-9a-fA-F]{3,8}\b|rgba?\(|oklch\(',text):failures.append(f'{name}: raw color outside the token layer')
        if 'data-theme' in text:failures.append(f'{name}: theme-dependent component selector')
    all_css='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'css').glob('*.css'))+'\n'+(ROOT/'extensions/panel.css').read_text(encoding='utf-8')
    declared=set(re.findall(r'(--tide-[\w-]+)\s*:',all_css))
    consumed=set(re.findall(r'var\((--tide-[\w-]+)',all_css))
    failures.extend('Unbound CSS token: '+name for name in sorted(consumed-declared))
    for path in (ROOT/'css').glob('*.css'):
        for url in re.findall(r'url\([\'"]?([^\)\'\"]+)',path.read_text(encoding='utf-8')):
            if not urlsplit(url).scheme and not (path.parent/url).resolve().is_file():failures.append(f'{path.name}: missing CSS asset/import {url}')
    manifest=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))
    color_roles=set(next(iter(json.loads((ROOT/'tokens/resolved.json').read_text(encoding='utf-8')).values()))['light'])
    for component in manifest['components']:
        if component['block'] not in all_classes:failures.append('No fixture for component '+component['block'])
        failures.extend(component['block']+': unknown semantic role '+role for role in component['roles'] if role not in color_roles)
        if component.get('source') and not (ROOT/component['source']).is_file():failures.append('Missing component CSS source: '+component['block'])
        fixture=component['fixture']
        target=ROOT/'index.html' if fixture=='library' else ROOT/fixture if fixture.startswith('extensions/') else ROOT/'tide-dark/frames'/fixture
        if not target.is_file():failures.append('Missing component fixture: '+component['block'])
    for entry in manifest.get('supportingBlocks',[]):
        if not (ROOT/entry['source']).is_file():failures.append('Missing supporting CSS source: '+entry['block'])
    for pattern in manifest.get('patterns',[]):
        if not (ROOT/pattern['contract'].split('#')[0]).is_file():failures.append('Missing pattern contract: '+pattern['name'])
        failures.extend('Pattern uses unknown block: '+block for block in pattern['uses'] if block not in registered_blocks(manifest))
    report={'pass':not failures,'htmlFiles':len(files),'localReferences':refs,'screenTemplates':len(signatures),'registeredComponents':len(manifest['components']),'browserScripts':scripts,'inlineStyles':inline_styles,'failures':failures}
    (ROOT/'qa/structure.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return bool(failures)


if __name__=='__main__':sys.exit(main())
