from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path('date-line-ui-kit').resolve()
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.scripts=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if tag=='script':self.scripts+=1
  for k in ('href','src'):
   if k in a:self.links.append(a[k])
errors=[];total=0;scripts=0
for f in root.rglob('*.html'):
 p=Links();p.feed(f.read_text(encoding='utf-8-sig'));scripts+=p.scripts
 if len(set(p.ids))!=len(p.ids):errors.append({'file':str(f.relative_to(root)),'error':'Duplicate IDs'})
 for value in p.links:
  u=urlsplit(value)
  if u.scheme or not u.path:continue
  total+=1
  target=(f.parent/unquote(u.path)).resolve()
  if not target.exists():errors.append({'file':str(f.relative_to(root)),'missing':value})
def lum(c):
 cs=[int(c[i:i+2],16)/255 for i in (1,3,5)]; cs=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in cs];return sum(a*b for a,b in zip(cs,[.2126,.7152,.0722]))
def ratio(a,b):a,b=sorted([lum(a),lum(b)]);return round((b+.05)/(a+.05),2)
checks={'primary':'#f0f1ed','secondary':'#b8bfc6','tertiary':'#939da6','success':'#b3d2bb','warning':'#e4c48f','danger':'#e6b1ad'}
result={'html_files':len(list(root.rglob('*.html'))),'local_references_checked':total,'scripts':scripts,'errors':errors,'contrast_on_canvas':{k:ratio(v,'#111517') for k,v in checks.items()},'field_border_contrast':ratio('#68747d','#171d20'),'primary_action_contrast':ratio('#111517','#edbd8b')}
(root/'qa/structural-checks.json').write_text(json.dumps(result,indent=2));print(result)
