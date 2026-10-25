from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
p=Path(r'C:/Users/andre/Documents/ChatGPT/Burque Events Designs/refinements')
studies=json.loads((p/'studies.json').read_text())
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
out=Image.new('RGB',(3*406,2*550),'#e9e7e2');d=ImageDraw.Draw(out)
for i,s in enumerate(studies):
 x=(i%3)*406;y=(i//3)*550
 d.text((x+8,y+8),s['id']+' / '+s['name'],font=font,fill='#292e30')
 a=Image.open(p/'qa'/f'{s["id"]}-list.png').convert('RGB').crop((0,140,390,320))
 b=Image.open(p/'qa'/f'{s["id"]}-event.png').convert('RGB').crop((0,416,390,724))
 out.paste(a,(x+8,y+36));out.paste(b,(x+8,y+224))
out.save(p/'qa/type-details.png')
