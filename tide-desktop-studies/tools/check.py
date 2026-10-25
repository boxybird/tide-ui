"""Preservation, component ownership, static markup and portable-reference checks."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import posixpath
import re
import sys

sys.dont_write_bytecode = True
from foundation import ROOT, APP, lock
from build import base, STUDIES, study_page
sys.path.insert(0, str(APP/'kit/tools'))
from contracts import markup_issues, ownership_issues


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.refs=[]; self.classes=[]; self.linked=[]; self.styles=0; self.handlers=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        self.classes.extend(a.get('class','').split())
        self.styles += int('style' in a)
        self.handlers += sum(k.startswith('on') for k in a)
        for attr in ('href','src','action'):
            if a.get(attr): self.refs.append(a[attr])
        for attr in ('for','form','aria-labelledby','aria-describedby'):
            self.linked.extend(a.get(attr,'').split())


def target_file(page, ref):
    parsed=urlsplit(ref)
    if parsed.scheme or parsed.netloc: return None
    if parsed.path:
        parent=page.parent.relative_to(ROOT).as_posix()
        url=posixpath.normpath(posixpath.join('/'+parent,unquote(parsed.path)))
        target=APP/url[6:] if url.startswith('/base/') else ROOT/url.lstrip('/')
    else: target=page
    return target, parsed.fragment


def original_markup(html, name):
    html=re.sub(r'<aside class="tide-study__tools"[^>]*></aside>', '', html)
    html=re.sub(r'class="([^"]*)"', lambda m:'class="'+' '.join(c for c in m[1].split() if not c.startswith('tide-study'))+'"', html)
    html=html.replace('<title>'+name+' · ', '<title>', 1)
    html=html.replace('<link rel="stylesheet" href="../css/studies.css">\n','')
    return html.replace('<script src="../js/layout.js" defer></script>\n','')


def main():
    lock()
    failures=[]; references=0; classes=set(); target_ids={}; parity=0
    manifest=json.loads((APP/'kit/component-manifest.json').read_text(encoding='utf-8'))
    pages=[ROOT/'index.html']+[ROOT/slug/f for slug,*_ in STUDIES for f in base.PAGES]
    for page in pages:
        html=page.read_text(encoding='utf-8'); scan=Scan(); scan.feed(html)
        label=page.relative_to(ROOT).as_posix(); classes.update(scan.classes)
        failures.extend(label+': '+issue for issue in markup_issues(html))
        if scan.styles or scan.handlers: failures.append(label+': inline styles/handlers')
        failures.extend(label+': duplicate ID '+key for key,count in Counter(scan.ids).items() if count>1)
        failures.extend(label+': unbound description/form/label '+key for key in scan.linked if key not in scan.ids)
        for ref in scan.refs:
            target=target_file(page,ref)
            if target is None: continue
            references+=1; path,fragment=target
            if not path.is_file(): failures.append(label+': missing '+ref); continue
            if fragment and path.suffix=='.html':
                if path not in target_ids:
                    other=Scan(); other.feed(path.read_text(encoding='utf-8')); target_ids[path]=set(other.ids)
                if fragment not in target_ids[path]: failures.append(label+': missing fragment '+ref)
    failures.extend(ownership_issues(classes,manifest,{'tide-app','tide-study','tide-study-review'}))
    for slug,name,*_ in STUDIES:
        for filename in base.PAGES:
            actual=(ROOT/slug/filename).read_text(encoding='utf-8')
            expected=base.app_page(filename,'bumble','dark','../base/')
            if original_markup(actual,name)!=expected: failures.append(slug+'/'+filename+': component markup drift')
            else: parity+=1
    css=(ROOT/'css/studies.css').read_text(encoding='utf-8')
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
    if re.search(r'(?<![-\w])(?:font(?:-[\w-]+)?|line-height|letter-spacing|color|background(?:-[\w-]+)?|border(?:-[\w-]+)?|box-shadow)\s*:',css):
        failures.append('Product study CSS changes a primitive/component appearance')
    if re.search(r'\.(?:tide-event-|tide-button|tide-field|tide-choice|tide-badge|tide-expandable)',css):
        failures.append('Product study CSS targets shared component classes')
    if re.search(r'--tide-(?!study-)[\w-]+\s*:',css): failures.append('Product study CSS overrides a shared token')
    if 'data-theme' in css or '--tide-palette-' in css: failures.append('Product study CSS depends on a theme implementation')
    lock()
    report={'pass':not failures,'htmlPages':len(pages),'localReferences':references,'unchangedComponentDocuments':parity,
            'kitFilesLocked':len(json.loads((ROOT/'locks/kit-1.2.1.json').read_text())),
            'appFilesLocked':len(json.loads((ROOT/'locks/app-1.3.1.json').read_text())),
            'newKitComponents':0,'failures':failures}
    (ROOT/'qa/source-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    return bool(failures)


if __name__=='__main__': raise SystemExit(main())
