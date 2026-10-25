from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
root=Path(r'C:/Users/andre/Documents/ChatGPT/Burque Events Designs')
source=Image.open(root/'research/concepts/pocket-nights/03-pocket-texture-refined.png').convert('RGB')
print('source',source.size)
# Generated board contains two app states without OS chrome. Preserve aspect ratio.
w,h=source.size
panels=[source.crop((0,0,w//2-8,h)),source.crop((w//2+8,0,w,h))]
board=Image.new('RGB',(393*4+60,900),'#edf0f2')
draw=ImageDraw.Draw(board)
for i,(panel,name) in enumerate(zip(panels,['list','detail'])):
    scaled=ImageOps.contain(panel,(393,798))
    x=i*806
    draw.text((x+12,8),'Reference (native width; OS chrome excluded)',fill='black')
    board.paste(scaled,(x,45))
    shot=Image.open(root/f'burque-pocket/qa/{name}.png').convert('RGB')
    print(name,shot.size)
    draw.text((x+415,8),'Browser implementation: 393 x 852',fill='black')
    board.paste(shot,(x+403,35))
board.save(root/'burque-pocket/qa/comparison.png')
