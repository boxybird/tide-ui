from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
root=Path(r'C:/Users/andre/Documents/ChatGPT/Burque Events Designs')
p=root/'refinements/qa'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
studies=json.loads((root/'refinements/studies.json').read_text())
board=Image.new('RGB',(3*808,2*912),'#e9e7e2');d=ImageDraw.Draw(board)
for i,s in enumerate(studies):
    x=(i%3)*808;y=(i//3)*912
    d.text((x+12,y+12),s['id']+'  '+s['name']+' / '+s['font'],fill='#292e30',font=font)
    for j,kind in enumerate(['list','event']):
        im=Image.open(p/(s['id']+'-'+kind+'.png')).convert('RGB')
        board.paste(im,(x+8+j*396,y+48))
board.save(p/'six-pairs-contact-sheet.png')
old1=Image.open(root/'burque-pocket/qa/list.png').convert('RGB').crop((0,54,393,818)).resize((390,758))
old2=Image.open(root/'burque-pocket/qa/detail.png').convert('RGB').crop((0,54,393,818)).resize((390,758))
comparison=Image.new('RGB',(1620,920),'#e9e7e2');dr=ImageDraw.Draw(comparison)
for j,(im,label) in enumerate([(old1,'Earlier app / list'),(Image.open(p/'01-list.png'),'Refinement 01 / list'),(old2,'Earlier app / event'),(Image.open(p/'01-event.png'),'Refinement 01 / event')]):
    dr.text((j*405+8,10),label,fill='#292e30',font=font)
    comparison.paste(im,(j*405,54))
comparison.save(p/'source-comparison.png')
