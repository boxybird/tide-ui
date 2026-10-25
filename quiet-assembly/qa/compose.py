"""Compose actual browser captures for design QA, without changing UI assets."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageStat
import json
root=Path(__file__).resolve().parent.parent
studies=json.loads((root/'studies.json').read_text())
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
canvas=Image.new('RGB',(2424,912),'#eeece7');draw=ImageDraw.Draw(canvas)
lists=Image.new('RGB',(1202,912),'#eeece7');ld=ImageDraw.Draw(lists)
compare=Image.new('RGB',(1616,2736),'#eeece7');cd=ImageDraw.Draw(compare)
details=Image.new('RGB',(1616,960),'#eeece7');dd=ImageDraw.Draw(details)
differences=[]
for i,s in enumerate(studies):
    sid=s['id'];x=8+i*808
    draw.text((x,8),f'{sid} {s["name"]} / {s["family"]}',font=font,fill='#292e30')
    for j,kind in enumerate(['list','event']):
        shot=Image.open(root/'qa'/f'{sid}-{kind}.png').convert('RGB')
        assert shot.size==(390,844),shot.size
        canvas.paste(shot,(x+j*398,48))
        if kind=='list':
            lists.paste(shot,(8+i*398,48));ld.text((8+i*398,8),f'{sid} {s["name"]}',font=font,fill='#292e30')
    old_id=['01','04','06'][i]
    y=i*912
    cd.text((8,y+8),f'Quiet Studies / {old_id}',font=font,fill='#292e30')
    cd.text((816,y+8),f'Quiet Assembly / {sid} {s["name"]}',font=font,fill='#292e30')
    for j,(folder,study_id) in enumerate([('refinements',old_id),('quiet-assembly',sid)]):
        for k,kind in enumerate(['list','event']):
            im=Image.open(root.parent/folder/'qa'/f'{study_id}-{kind}.png').convert('RGB')
            compare.paste(im,(8+j*808+k*398,y+48))
    old=Image.open(root.parent/'refinements/qa'/f'{old_id}-event.png').convert('RGB')
    new=Image.open(root/'qa'/f'{sid}-event.png').convert('RGB')
    diff=ImageChops.difference(old,new)
    differences.append({'study':sid,'reference':old_id,'event_pixel_equal':diff.getbbox() is None,'mean_channel_difference':ImageStat.Stat(diff).mean})
    # Focused same-size crops expose type, metadata rhythm and photo contrast.
    for j,(im,label) in enumerate([(old,f'Original {old_id}'),(new,f'New {sid}')]):
        dd.text((8+j*808,i*320+4),label,font=small,fill='#292e30')
        crop=im.crop((0,400,390,700))
        details.paste(crop,(8+j*808,i*320+24))
canvas.save(root/'qa/three-pairs.png');lists.save(root/'qa/three-lists.png')
compare.save(root/'qa/source-comparison.png');details.save(root/'qa/type-comparison.png')
(root/'qa/event-fidelity.json').write_text(json.dumps(differences,indent=2))
print(json.dumps(differences,indent=2))
