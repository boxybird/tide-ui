from pathlib import Path
import json,re,hashlib
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image,ImageDraw,ImageChops
p=Path('date-line-kit-variations');q=p/'qa'
data=json.loads((q/'layout-390.json').read_text());source={d['page']:d for d in data if d['skin']=='source'}
differences=[]
for row in data:
 if row['skin']=='source':continue
 a=source[row['page']]
 if row['content']!=a['content']:differences.append({'skin':row['skin'],'page':row['page'],'difference':'text'})
 if row['geometry']!=a['geometry']:
  dif=[]
  for i,(before,after) in enumerate(zip(a['geometry'],row['geometry'])):
   if before!=after:dif.append({'index':i,'before':before,'after':after})
  differences.append({'skin':row['skin'],'page':row['page'],'geometry':dif,'counts':[len(a['geometry']),len(row['geometry'])]})
(q/'invariance.json').write_text(json.dumps({'screens':len(data),'differences':differences},indent=2))
print('Geometry/content differences:',[(x['skin'],x['page'],x.get('difference','geometry')) for x in differences])
for name in ['search','states','01-event','review']:
 out=Image.new('RGB',(1608,880),'#111517');draw=ImageDraw.Draw(out)
 for i,(skin,title) in enumerate([('source','Original Date Line'),('daybreak','Daybreak'),('tide','Tide'),('lift','Lift')]):
  im=Image.open(q/(skin+'-'+name+'.png'));out.paste(im,(i*406,36));draw.text((i*406+12,10),title,fill='white')
 out.save(q/('compare-'+name+'.png'))
# Source/reference screenshot identity confirms the neutral comparison copy.
checks={}
for name in ['search','submit','states','01-event','review']:
 a=Image.open(q/f'source-{name}.png').convert('RGB');b=Image.open(q/f'original-{name}.png').convert('RGB');checks[name]=ImageChops.difference(a,b).getbbox()
(q/'reference-pixels.json').write_text(json.dumps(checks,indent=2));print('Reference pixel checks:',checks)
class Refs(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.scripts=0
 def handle_starttag(self,t,attrs):
  attrs=dict(attrs);self.scripts+=t=='script'
  for k in ['href','src']:
   if k in attrs:self.links.append(attrs[k])
errors=[];scripts=0;links=0
for f in p.rglob('*.html'):
 parser=Refs();parser.feed(f.read_text());scripts+=parser.scripts
 for value in parser.links:
  u=urlsplit(value)
  if u.scheme or not u.path:continue
  links+=1
  if not (f.parent/unquote(u.path)).exists():errors.append({'file':str(f),'link':value})
def l(c):
 c=[int(c[i:i+2],16)/255 for i in (1,3,5)];c=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in c];return sum(x*y for x,y in zip(c,[.2126,.7152,.0722]))
def ratio(a,b):a,b=sorted([l(a),l(b)]);return round((b+.05)/(a+.05),2)
colors=json.loads((p/'skins.json').read_text());contrast={}
for key,t in colors.items():
 contrast[key]={'text':ratio(t['primary'],t['base']),'secondary':ratio(t['secondary'],t['base']),'tertiary':ratio(t['tertiary'],t['base']),'accent':ratio(t['accent'],t['base']),'onAccent':ratio(t['accent'],t['onAccent']),'controlBorder':ratio(t['control'],t['field']),'success':ratio(t['success'],t['successBg']),'warning':ratio(t['warning'],t['warningBg']),'danger':ratio(t['danger'],t['dangerBg'])}
checks={'html_files':len(list(p.rglob('*.html'))),'links_checked':links,'scripts':scripts,'missing':errors,'contrast':contrast,'shared_css_unchanged':{f:hashlib.sha256((p/f).read_bytes()).hexdigest()==hashlib.sha256((p.parent/'date-line-ui-kit'/f).read_bytes()).hexdigest() for f in ['screens.css','themes.css','cards.css','fonts.css','ui.css','gallery.css']}}
(q/'structural-checks.json').write_text(json.dumps(checks,indent=2));print(checks)
