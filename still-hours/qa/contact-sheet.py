"""Compose browser captures for review; this does not alter UI assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
root=Path(__file__).resolve().parent.parent
studies=json.loads((root/'studies.json').read_text())
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
pair_width=804
canvas=Image.new('RGB',(2424,1824),'#e9e9e0')
draw=ImageDraw.Draw(canvas)
for index,s in enumerate(studies):
    x=(index%3)*808+8; y=(index//3)*912
    draw.text((x,y+8),f'{s["id"]}  {s["name"]} / {s["font"]}',font=font,fill='#2b3028')
    for column,kind in enumerate(['list','event']):
        shot=Image.open(root/'qa'/f'{s["id"]}-{kind}.png').convert('RGB')
        assert shot.size==(390,844),shot.size
        canvas.paste(shot,(x+column*398,y+48))
canvas.save(root/'qa/six-pairs-contact-sheet.png')
# Hold both old and new examples at exactly the same native width.
compare=Image.new('RGB',(1616,912),'#e9e9e0');d=ImageDraw.Draw(compare)
for col,(folder,label) in enumerate([('refinements','Quiet Studies / 01 Soft Focus'),('still-hours','Still Hours / 01 Sage')]):
    x=8+col*808;d.text((x,8),label,font=font,fill='#2b3028')
    for i,kind in enumerate(['list','event']):
        image=Image.open(root.parent/folder/'qa'/f'01-{kind}.png').convert('RGB')
        compare.paste(image,(x+i*398,48))
compare.save(root/'qa/family-comparison.png')
print('Wrote six-pair and family-comparison contact sheets.')
