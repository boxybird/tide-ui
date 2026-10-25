from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw,ImageChops
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
root=Path('tide-ui-kit-studies');q=root/'qa'
a=json.loads((q/'tide-before-state-metrics.json').read_text());b=json.loads((q/'tide-after-state-metrics.json').read_text());shift=[]
for i,(x,y) in enumerate(zip(a['notices'],b['notices'])):
 if any(x[k]!=y[k] for k in x):shift.append({'index':i,'before':x,'after':y})
(q/'stripe-removal.json').write_text(json.dumps({'same_text':a['text']==b['text'],'geometry_changes':shift,'uniform_borders':all(c['left']==c['top'] and c['leftWidth']==c['topWidth'] for c in b['notices'])},indent=2))
data=json.loads((q/'layout-390.json').read_text());src={x['page']:x for x in data if x['skin']=='source'};dif=[]
for row in data:
 if row['skin']=='source':continue
 before=src[row['page']]
 if row['text']!=before['text'] or row['geometry']!=before['geometry']:dif.append({'skin':row['skin'],'page':row['page'],'text_same':row['text']==before['text'],'geometry_same':row['geometry']==before['geometry']})
(q/'invariance.json').write_text(json.dumps({'views':len(data),'differences':dif},indent=2))
for name in ['search','states','01-event','submit']:
 out=Image.new('RGB',(1608,880),'#0f1720');d=ImageDraw.Draw(out)
 for i,(skin,title) in enumerate([('tide','Tide / current favorite'),('mist','Mist / light mode'),('slate','Slate / muted blue-gray'),('deep','Deep / darker cyan')]):
  out.paste(Image.open(q/f'{skin}-{name}.png'),(i*406,36));d.text((i*406+12,10),title,fill='white')
 out.save(q/f'compare-{name}.png')
preview=Image.new('RGB',(1202,880),'#0f1720');d=ImageDraw.Draw(preview)
for i,(skin,title) in enumerate([('mist','01 / Mist'),('slate','02 / Slate'),('deep','03 / Deep')]):
 preview.paste(Image.open(q/f'{skin}-search.png'),(i*406,36));d.text((i*406+12,10),title,fill='white')
preview.save(q/'preview.png')
out=Image.new('RGB',(796,880),'#0f1720');d=ImageDraw.Draw(out)
for i,(name,title) in enumerate([('tide-before-states','Before / colored left stripe'),('tide-after-states','After / uniform neutral outline')]):
 out.paste(Image.open(q/f'{name}.png'),(i*406,36));d.text((i*406+12,10),title,fill='white')
out.save(q/'callouts-before-after.png')
class Refs(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.scripts=0
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs);self.scripts+=tag=='script'
  for k in ['href','src']:
   if k in attrs:self.refs.append(attrs[k])
errors=[];links=0;scripts=0
for f in root.rglob('*.html'):
 p=Refs();p.feed(f.read_text(encoding='utf-8'));scripts+=p.scripts
 for value in p.refs:
  url=urlsplit(value)
  if url.scheme or not url.path:continue
  links+=1
  if not (f.parent/unquote(url.path)).exists():errors.append({'file':str(f),'ref':value})
def lum(c):
 c=[int(c[i:i+2],16)/255 for i in (1,3,5)];c=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in c];return sum(x*y for x,y in zip(c,[.2126,.7152,.0722]))
def contrast(a,b):a,b=sorted([lum(a),lum(b)]);return round((b+.05)/(a+.05),2)
palettes=json.loads((root/'palettes.json').read_text());ratios={k:{'primary':contrast(p['primary'],p['base']),'secondary':contrast(p['secondary'],p['base']),'tertiary':contrast(p['tertiary'],p['base']),'accent':contrast(p['accent'],p['base']),'onAccent':contrast(p['onAccent'],p['accent']),'fieldBorder':contrast(p['control'],p['field']),'success':contrast(p['success'],p['successBg']),'warning':contrast(p['warning'],p['warningBg']),'danger':contrast(p['danger'],p['dangerBg'])} for k,p in palettes.items()}
checks={'html_files':len(list(root.rglob('*.html'))),'local_references':links,'scripts':scripts,'errors':errors,'contrast':ratios,'shared_css_preserved':{f:hashlib.sha256((root/f).read_bytes()).hexdigest()==hashlib.sha256((root.parent/'date-line-ui-kit'/f).read_bytes()).hexdigest() for f in ['screens.css','themes.css','cards.css','fonts.css','ui.css','gallery.css']}}
(q/'structural-checks.json').write_text(json.dumps(checks,indent=2))
print('Stripe-removal shifts:',shift);print('Kit invariance differences:',dif);print(checks)
