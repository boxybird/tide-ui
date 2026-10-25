"""Structural acceptance checks for the actual static deliverable."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

root = Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.refs=[]; self.scripts=0; self.images=[]; self.lang=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='script': self.scripts+=1
        if tag=='html': self.lang=a.get('lang')
        if 'id' in a: self.ids.append(a['id'])
        for key in ['href','src']:
            if a.get(key): self.refs.append((tag,key,a[key]))
        if tag=='img': self.images.append(a)

pages={}
for p in list(root.glob('*.html'))+list((root/'frames').glob('*.html')):
    parser=Page(); parser.feed(p.read_text(encoding='utf-8'));pages[p]=parser
issues=[]
for p,page in pages.items():
    if page.lang!='en':issues.append(f'{p.name}: missing language')
    if page.scripts:issues.append(f'{p.name}: browser script present')
    if len(set(page.ids))!=len(page.ids):issues.append(f'{p.name}: duplicate IDs')
    for a in page.images:
        if 'alt' not in a:issues.append(f'{p.name}: image lacks alt attribute')
    for tag,key,ref in page.refs:
        parsed=urlsplit(ref)
        if parsed.scheme:
            if key=='src':issues.append(f'{p.name}: remote embedded asset {ref}')
            continue
        target=(p.parent/unquote(parsed.path)).resolve() if parsed.path else p
        if not target.is_relative_to(root):issues.append(f'{p.name}: resource outside collection')
        if not target.exists():issues.append(f'{p.name}: missing {ref}')
        if parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:issues.append(f'{p.name}: broken fragment {ref}')

frames=list((root/'frames').glob('*.html'))
if len(frames)!=12:issues.append(f'Expected12 standalone frames, found{len(frames)}')
metrics=json.loads((root/'qa/browser-metrics-390.json').read_text())
if len(metrics)!=12:issues.append('Missing browser captures')
for m in metrics:
    if m['overflow'] or m['clipped']:issues.append(f'Native-width clipping in{m["study"]} {m["kind"]}')
    if m['scripts']:issues.append(f'Unexpected script in{m["study"]}')
    if 'hero' in m and m['hero']!=844:issues.append(f'Unexpected hero height in{m["study"]}')
    for t in m['targets']:
        if t['width']<44 or t['height']<44:issues.append(f'Small target in{m["study"]}: {t["label"]}')
responsive=json.loads((root/'qa/responsive-metrics.json').read_text())
for m in responsive:
    if m['pageOverflow'] or m['clipped']:issues.append(f'Responsive clipping in{m["study"]} at{m["width"]}')
fonts=list((root/'assets/fonts').glob('*.woff2'))
if len(fonts)!=7:issues.append('Expected7 local font files')
for p in fonts:
    if p.read_bytes()[:4]!=b'wOF2':issues.append(f'Invalid font file{p.name}')
result={'html_pages':len(pages),'standalone_frames':len(frames),'local_fonts':len(fonts),'browser_native_checks':len(metrics),'responsive_checks':len(responsive),'browser_scripts':sum(p.scripts for p in pages.values()),'issues':issues,'passed':not issues}
(root/'qa/validation-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
raise SystemExit(bool(issues))
