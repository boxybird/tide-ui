from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,zipfile,hashlib
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
        if not target.is_relative_to(root):issues.append(f'{p.name}: external collection dependency')
        if not target.exists():issues.append(f'{p.name}: missing {ref}')
        if url.fragment and target in pages and url.fragment not in pages[target].ids:issues.append(f'{p.name}: broken fragment {ref}')
for css in root.glob('*.css'):
    for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)',css.read_text()):
        if not (css.parent/ref).exists():issues.append(f'{css.name}: missing CSS asset {ref}')
fonts=list((root/'assets/fonts').glob('*.woff2'))
for p in fonts:
    if p.read_bytes()[:4]!=b'wOF2':issues.append(f'Invalid font: {p.name}')
if len(pages)!=12:issues.append('Expected 12 HTML documents')
if len(fonts)!=3:issues.append('Expected 3 local fonts from frozen font-face stylesheet')
native=json.loads((root/'qa/browser-metrics-390.json').read_text())
for m in native:
    if m['width']!=390 or m['overflow'] or m['clipped'] or m['scripts']:issues.append(f'Native frame failed: {m["slug"]}/{m["kind"]}')
    if m['kind']=='event' and (m['hero']['height']!=844 or m['detailsY']!=844):issues.append('Full-screen event geometry changed')
    for a in m['targets']:
        if a['width']<44 or a['height']<44:issues.append(f'Small target: {a["label"]}')
responsive=json.loads((root/'qa/responsive-metrics.json').read_text())
short=json.loads((root/'qa/short-phone-metrics.json').read_text())
for m in responsive+short:
    if m['pageOverflow'] or m['clipped']:issues.append(f'Responsive failed: {m["slug"]}/{m["width"]}')
gallery=json.loads((root/'qa/gallery-metrics.json').read_text())
if any(m['overflow'] or m['captionOverflow'] for m in gallery):issues.append('Gallery overflow')
preservation=json.loads((root/'qa/preservation-results.json').read_text())
contrast=json.loads((root/'qa/contrast-results.json').read_text())
if not preservation['passed']:issues.append('Preservation comparison failed')
if not contrast['passed']:issues.append('Contrast failed')
lock=json.loads((root/'baseline-lock.json').read_text())
for f in lock['files']:
    for p in [(root/f['source']).resolve(),root/f['copy']]:
        if hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:issues.append(f'Approved source drift: {p.name}')
with zipfile.ZipFile(root/'date-line-in-practice.zip') as z:
    if z.testzip():issues.append('ZIP CRC error')
    names=z.namelist()
    required=['index.html','baseline.html','frames/baseline-list.html','frames/local-partner-event.html','frames/rough-upload-event.html','baseline-lock.json','source/approved-list.inc','assets/images/organizer-upload.png','assets/images/provenance.json','qa/preservation-results.json']
    for name in required:
        if name not in names:issues.append(f'Archive missing {name}')
    if any('node_modules' in n or '..' in Path(n).parts for n in names):issues.append('Unexpected ZIP entry')
    if len([n for n in names if n.endswith('.html')])!=12:issues.append('Archive HTML count mismatch')
result={'html_pages':len(pages),'phone_frames':len(native),'browser_scripts':sum(p.scripts for p in pages.values()),'responsive_checks':len(responsive),'short_phone_checks':len(short),'gallery_checks':len(gallery),'contrast_checks':len(contrast['checks']),'locked_approved_files':len(lock['files']),'zip_entries':len(names),'issues':issues,'passed':not issues}
(root/'qa/validation-results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
raise SystemExit(bool(issues))
