from PIL import Image, ImageChops, ImageDraw
from pathlib import Path
import json
p=Path('date-line-gather-playground/qa')
out=Image.new('RGB',(780,1740),'#101517');d=ImageDraw.Draw(out)
results={}
for i,name in enumerate(['list','event']):
 a=Image.open(p/('source-'+name+'.png')).convert('RGB'); b=Image.open(p/(name+'.png')).convert('RGB')
 out.paste(a,(0,i*870+26));out.paste(b,(390,i*870+26));d.text((10,i*870+6),'Original Gather / '+name,fill='white');d.text((400,i*870+6),'Amplified / '+name,fill='white')
 diff=ImageChops.difference(a,b);results[name]={'size':a.size,'difference_bbox':diff.getbbox(),'changed_pixels':sum(any(c for c in v) for v in diff.getdata())}
out.save(p/'endpoint-comparison.png');(p/'pixel-checks.json').write_text(json.dumps(results,indent=2));print(results)
