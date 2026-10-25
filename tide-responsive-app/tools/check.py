"""Verify source contracts, portable links and preservation. Not a WCAG audit."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
from urllib.parse import urlsplit,unquote
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'kit/tools'))
from contracts import ContractScan,markup_issues,ownership_issues,style_ownership_issues


def check():
    failures=[];refs=0;scripts=0;script_files=set();classes=set()
    pages=[p for p in ROOT.rglob('*.html') if not any(x in p.relative_to(ROOT).parts for x in ('kit','qa','dist','versions'))]
    parsed={p:ContractScan() for p in pages}
    for p,scan in parsed.items():scan.feed(p.read_text(encoding='utf-8'))
    for p,scan in parsed.items():
        source=p.read_text(encoding='utf-8');label=str(p.relative_to(ROOT))
        failures.extend(f'{label}: {s}' for s in markup_issues(source))
        counts=Counter(n['attrs']['id'] for n in scan.nodes if n['attrs'].get('id'))
        if any(n>1 for n in counts.values()):failures.append(label+': duplicate ID')
        ids=set(counts)
        for node in scan.nodes:
            a=node['attrs'];tag=node['tag']
            if tag=='script':
                scripts+=1
                script_path=(p.parent/a.get('src','')).resolve()
                script_files.add(script_path)
                allowed={(ROOT/'js'/name).resolve() for name in ('search-core.js','event-search.js','event-navigation.js')}
                if script_path not in allowed or 'defer' not in a or node['text'].strip():failures.append(label+': unregistered or inline browser script')
            if 'style' in a or any(k.startswith('on') for k in a):failures.append(label+': inline styling or event handler')
            for cls in a.get('class','').split():
                classes.add(cls)
                if cls!='tide' and not cls.startswith('tide-'):failures.append(label+': unprefixed class '+cls)
            for attr in ('aria-labelledby','aria-describedby','for','form'):
                for ref in a.get(attr,'').split():
                    if ref not in ids:failures.append(label+': missing label reference '+ref)
            if tag in ('input','textarea','select') and a.get('type') not in ('hidden','submit','reset'):
                # Native explicit labels or nested choice labels are checked from authored markup.
                explicit=a.get('id') and re.search(r'<label\b[^>]*\bfor="'+re.escape(a['id'])+'"',source)
                if not explicit and a.get('type') not in ('radio','checkbox'):failures.append(label+': unlabelled form field '+a.get('id',''))
            for attr in ('href','src','action'):
                if attr not in a:continue
                url=urlsplit(a[attr])
                if url.scheme or url.netloc:continue
                target=(p.parent/unquote(url.path)).resolve() if url.path else p
                refs+=1
                if not target.is_file():failures.append(label+': missing local reference '+a[attr]);continue
                if url.fragment:
                    other=parsed.get(target)
                    if other is None:
                        other=ContractScan();other.feed(target.read_text(encoding='utf-8'))
                    if not any(n['attrs'].get('id')==url.fragment for n in other.nodes):failures.append(label+': missing fragment '+a[attr])
    css=(ROOT/'css/app.css').read_text(encoding='utf-8')+(ROOT/'css/review.css').read_text(encoding='utf-8')
    manifest=json.loads((ROOT/'kit/component-manifest.json').read_text(encoding='utf-8'))
    failures.extend(ownership_issues(classes,manifest,{'tide-app','tide-review'}))
    failures.extend(style_ownership_issues(css,manifest))
    if re.search(r'#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|oklch|hsla?)\(',css):failures.append('App CSS contains raw palette colors')
    if re.search(r'\[data-(?:theme|mode)',css):failures.append('App CSS contains theme-specific component selectors')
    # Public app tokens must resolve either in the app or the imported kit.
    allcss=css+(ROOT/'kit/css/tide.css').read_text(encoding='utf-8')
    defined=set(re.findall(r'(--tide-[\w-]+)\s*:',allcss))
    used=set(re.findall(r'var\((--tide-[\w-]+)',allcss))
    for token in sorted(used-defined):failures.append('Undefined CSS token: '+token)
    lock=json.loads((ROOT/'qa/original-kit-lock.json').read_text(encoding='utf-8'))
    # Lock schema is a path/hash mapping; metadata is allowed in the wrapper.
    hashes=lock.get('files',lock)
    if isinstance(hashes,list):hashes={x['path']:x['sha256'] for x in hashes}
    original=ROOT.parent/'tide-ui-kit'
    if original.is_dir():
        for rel,digest in hashes.items():
            p=original/rel
            actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
            expected=digest.get('sha256') if isinstance(digest,dict) else digest
            if actual!=expected:failures.append('Original kit changed: '+rel)
    for rel in ('css/tokens.css','tokens/themes.json','assets/fonts/manrope-latin-wght-normal.woff2'):
        if hashlib.sha256((ROOT/'kit'/rel).read_bytes()).hexdigest()!=hashes[rel]:failures.append('Preserved primitive changed: '+rel)
    baseline=json.loads((ROOT/'qa/iteration-1.0.3-lock.json').read_text(encoding='utf-8'))
    for rel,digest in baseline.items():
        p=ROOT/'versions/1.0.3'/rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:failures.append('Preserved 1.0.3 baseline changed: '+rel)
    report={'pass':not failures,'htmlFiles':len(pages),'localReferences':refs,'browserScriptFiles':len(script_files),'browserScriptReferences':scripts,'originalKitFilesVerified':len(hashes) if original.is_dir() else 0,'frozenBaselineFilesVerified':len(baseline),'originalKitStatus':'Verified against preserved sibling' if original.is_dir() else 'Original not bundled; reference hashes retained','preservedPrimitives':['type','space','radius','targets','theme inputs','font'],'failures':failures}
    report.update(kitVersion=manifest['version'],sharedBlocksVerified=len({cls.split('__')[0].split('--')[0] for cls in classes}-{'tide','tide-app','tide-review'}))
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return not failures


if __name__=='__main__':raise SystemExit(0 if check() else 1)
