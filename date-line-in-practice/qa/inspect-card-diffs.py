from pathlib import Path
from PIL import Image,ImageChops
import json
qa=Path(__file__).resolve().parent
ms=json.loads((qa/'browser-metrics-390.json').read_text())
base=next(m for m in ms if m['slug']=='baseline' and m['kind']=='list')
ad=next(m for m in ms if m['slug']=='local-partner' and m['kind']=='list')
bi=Image.open(qa/'baseline-list.png').convert('RGB');ai=Image.open(qa/'local-partner-list.png').convert('RGB')
for i,(b,a) in enumerate(zip(base['cards'],ad['cards'])):
    bbox=lambda r:(0,round(r['y']),390,round(r['bottom']))
    d=ImageChops.difference(bi.crop(bbox(b)),ai.crop(bbox(a)))
    rows=[y for y in range(d.height) if d.crop((0,y,390,y+1)).getbbox()]
    print(i+1,'bbox',d.getbbox(),'rows',rows[:12], 'total differing rows',len(rows))
