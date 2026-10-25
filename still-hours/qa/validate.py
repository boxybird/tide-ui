"""Check the delivered documents, assets, browser evidence and portable archive."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,zipfile
root=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.refs=[];self.scripts=0;self.images=[];self.lang=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='script':self.scripts+=1
        if a.get('id'):self.ids.append(a['id'])
        if tag=='img':self.images.append(a)
        for k in ['href','src']:
            if a.get(k):self.refs.append((k,a[k]))
pages={}
for p in list(root.glob('*.html'))+list((root/'frames').glob('*.html')):
    obj=Page();obj.feed(p.read_text(encoding='utf-8'));pages[p]=obj
issues=[]
for p,obj in pages.items():
    if obj.lang!='en':issues.append(f'{p.name}: missing language')
    if obj.scripts:issues.append(f'{p.name}: browser script')
    if len(obj.ids)!=len(set(obj.ids)):issues.append(f'{p.name}: duplicate IDs')
    for im in obj.images:
        if 'alt' not in im:issues.append(f'{p.name}: missing alt')
    for key,ref in obj.refs:
        url=urlsplit(ref)
        if url.scheme:
            if key=='src':issues.append(f'{p.name}: remote embedded asset')
            continue
        target=(p.parent/unquote(url.path)).resolve() if url.path else p
        if not target.is_relative_to(root):issues.append(f'{p.name}: external collection dependency {ref}')
        if not target.exists():issues.append(f'{p.name}: missing {ref}')
        if url.fragment and target in pages and url.fragment not in pages[target].ids:issues.append(f'{p.name}: broken fragment {ref}')
for css in root.glob('*.css'):
    for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)',css.read_text()):
        if not (css.parent/ref).exists():issues.append(f'{css.name}: missing CSS asset {ref}')
fonts=list((root/'assets/fonts').glob('*.woff2'))
for p in fonts:
    if p.read_bytes()[:4]!=b'wOF2':issues.append(f'Invalid WOFF2: {p.name}')
if len(pages)!=20:issues.append(f'Expected 20 HTML documents, found {len(pages)}')
if len(fonts)!=7:issues.append(f'Expected 7 local fonts, found {len(fonts)}')
native=json.loads((root/'qa/browser-metrics-390.json').read_text())
for m in native:
    if m['width']!=390 or m['overflow'] or m['clipped'] or m['scripts']:issues.append(f'Native frame failed: {m["study"]}/{m["kind"]}')
    if m['kind']=='event' and m['hero']!=844:issues.append('Event height mismatch')
    for a in m['targets']:
        if a['width']<44 or a['height']<44:issues.append(f'Target too small: {m["study"]}/{a["label"]}')
responsive=json.loads((root/'qa/responsive-metrics.json').read_text())
short=json.loads((root/'qa/short-phone-metrics.json').read_text())
for m in responsive+short:
    if m['pageOverflow'] or m['clipped']:issues.append(f'Responsive failed: {m["study"]}/{m["width"]}')
gallery=json.loads((root/'qa/gallery-metrics.json').read_text())
if any(m['overflow'] for m in gallery):issues.append('Gallery overflow')
contrast=json.loads((root/'qa/contrast-results.json').read_text())
if not all(m['pass'] for m in contrast):issues.append('Contrast failed')
with zipfile.ZipFile(root/'still-hours.zip') as z:
    if z.testzip():issues.append('Archive CRC error')
    names=z.namelist()
    for required in ['index.html','frames/01-list.html','frames/06-event.html','assets/images/ink-after-dark.png','qa/contrast-results.json']:
        if required not in names:issues.append(f'Archive missing {required}')
    if any('node_modules' in n or '..' in Path(n).parts for n in names):issues.append('Unexpected archive entry')
    if len([n for n in names if n.endswith('.html')])!=20:issues.append('Archive document count mismatch')
result={'html_pages':len(pages),'standalone_frames':len(list((root/'frames').glob('*.html'))),'local_fonts':len(fonts),'browser_scripts':sum(p.scripts for p in pages.values()),'native_checks':len(native),'responsive_checks':len(responsive),'short_phone_checks':len(short),'gallery_checks':len(gallery),'contrast_checks':sum(len(m['checks']) for m in contrast),'zip_entries':len(names),'issues':issues,'passed':not issues}
(root/'qa/validation-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
raise SystemExit(bool(issues))
