from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib
p=Path('date-line-ui-kit/qa')
can=Image.new('RGB',(780,1740),'#111517');d=ImageDraw.Draw(can);checks={}
for i,name in enumerate(['list','event']):
 a=Image.open(p/f'source-{name}.png').convert('RGB');b=Image.open(p/f'{name}.png').convert('RGB');delta=ImageChops.difference(a,b)
 checks[name]={'size':a.size,'difference_box':delta.getbbox()};can.paste(a,(0,26+i*870));can.paste(b,(390,26+i*870));d.text((12,6+i*870),'Original Date Line / '+name,fill='white');d.text((402,6+i*870),'UI kit preserved copy / '+name,fill='white')
can.save(p/'source-comparison.png');(p/'pixel-checks.json').write_text(json.dumps(checks,indent=2))
can=Image.new('RGB',(1202,1792),'#111517');d=ImageDraw.Draw(can)
for i,(name,title) in enumerate([('search','Search & results'),('filters','Filters'),('submit','Submit an event'),('saved','Saved evenings'),('review','Review / no photo'),('states','Recovery & status')]):
 x=(i%3)*406;y=(i//3)*896;im=Image.open(p/f'{name}.png');can.paste(im,(x,y+36));d.text((x+12,y+10),title,fill='#edbd8b')
can.save(p/'screen-studies.png');print(checks)
checks={}
for name in ['screens.css','themes.css','cards.css','fonts.css','frames/01-list.html','frames/01-event.html']:
 checks[name]=hashlib.sha256((Path('quiet-assembly')/name).read_bytes()).hexdigest()==hashlib.sha256((Path('date-line-ui-kit')/name).read_bytes()).hexdigest()
(p/'preservation.json').write_text(json.dumps(checks,indent=2));print(checks)
