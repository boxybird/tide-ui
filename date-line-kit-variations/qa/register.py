from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
p=Path('date-line-kit-variations');q=p/'qa';src=Path('date-line-ui-kit')
proof={}
for skin in ['original','daybreak','tide','lift']:
 folder=p if skin=='original' else p/skin;checks={}
 for f in (src/'frames').glob('*.html'):
  def normalized(path):
   s=path.read_text(encoding='utf-8-sig');b=re.search(r'<body[^>]*>([\s\S]*)</body>',s)[1];return re.sub(r'(?:\.\./)*assets/','ASSETS/',b)
  checks[f.name]=normalized(f)==normalized(folder/'frames'/f.name)
 proof[skin]=checks
(q/'fixture-lock.json').write_text(json.dumps(proof,indent=2))
# Crop-free composition of the three actual native-width screens.
out=Image.new('RGB',(1202,880),'#111517');d=ImageDraw.Draw(out)
for i,(key,title) in enumerate([('daybreak','01 / Daybreak'),('tide','02 / Tide'),('lift','03 / Lift')]):
 out.paste(Image.open(q/(key+'-search.png')),(i*406,36));d.text((i*406+12,10),title,fill='white')
out.save(q/'preview.png')
def valid_utf8(path):
 try: path.read_text(encoding='utf-8-sig'); return True
 except UnicodeDecodeError: return False
def read_text(path): return path.read_text(encoding='utf-8-sig') if valid_utf8(path) else path.read_text(encoding='cp1252')
p=Path('research/design-sets.json');data=json.loads(p.read_text(encoding='utf-8-sig') if valid_utf8(p) else p.read_text(encoding='cp1252'));data['updated']='2026-10-22'
if not any(x.get('name')=='Date Line Appearance Studies' for x in data['sets']): data['sets'].append({'name':'Date Line Appearance Studies','date':'2026-10-22','description':'Three complete UI kit skins with identical components, content, typography, spacing, sizing, screens and coverage. Original Date Line kit retained as a comparison.','path':'date-line-kit-variations/index.html','url':'http://127.0.0.1:4183/','options':[{'number':1,'name':'Daybreak','style':'Light, warm white/lilac with plum actions.'},{'number':2,'name':'Tide','style':'Dark navy/teal, squared edges.'},{'number':3,'name':'Lift','style':'Charcoal/lavender, raised panels and controls.'}],'status':'New comparison set; no favorite chosen.'})
data['preferences']['current_constraint']='Compare complete UI kits using the same Foundations / Components / Screens / Coverage presentation. Preserve component markup, content, typography, spacing, targets and behavior; vary palette, radii and elevation only. Static HTML/CSS.'
data['preferences']['ui_kit_presentation']='User loves the sidebar and zoomed-out kit presentation. Complete kit is the comparison unit; keep the exact inventory and screen coverage consistent across visual variations.'
data['preferences']['selected_direction']['next']='Compare Daybreak, Tide and Lift as full kits, keeping the original Date Line kit as reference.'
p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=Path('AGENTS.md');s=read_text(p);s+='\n- Latest comparison request (2026-10-22): user loves the UI kit sidebar (Foundations, Components, Screens, Coverage) and wants complete kit variations. Preserve exact component structure, content, type scale, spacing, control sizing and behavior; palette, radius and depth are the explicit variables. New collection: date-line-kit-variations/ on port4183, original reference + Daybreak (light/plum), Tide (dark/teal/squared), Lift (dark/lavender/raised). No new favorite chosen.\n';p.write_text(s,encoding='utf-8')
p=Path('research/source-notes.txt');s=read_text(p);s+='\n2026-10-22 — Date Line Appearance Studies: full-kit comparison, not isolated card variants. User explicitly permits palette, edge and depth experiments while retaining all primitives/inventory. Same shared source kit, 3 paint-only stylesheets; no new assets or product flows. Port4183.\n';p.write_text(s,encoding='utf-8')
print('All body fixture checks:',all(all(x.values()) for x in proof.values()))
