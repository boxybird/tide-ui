"""Compare approved pixels and compose actual browser screenshots for review."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageStat
import json,hashlib
root=Path(__file__).resolve().parent.parent
qa=root/'qa'
metrics=json.loads((qa/'browser-metrics-390.json').read_text())
def im(name):
    p=Image.open(qa/f'{name}.png').convert('RGB')
    assert p.size==(390,844),(name,p.size)
    return p
def equal(a,b):return ImageChops.difference(a,b).getbbox() is None
checks={
    'baseline_list_equals_approved':equal(im('approved-list'),im('baseline-list')),
    'baseline_event_equals_approved':equal(im('approved-event'),im('baseline-event')),
    'rough_upload_list_equals_approved':equal(im('approved-list'),im('rough-upload-list')),
    'advertising_event_opening_equals_approved':equal(im('approved-event'),im('local-partner-event')),
}
base=next(m for m in metrics if m['slug']=='baseline' and m['kind']=='list')
ads=next(m for m in metrics if m['slug']=='local-partner' and m['kind']=='list')
boundaries=[]
for i,(b,a) in enumerate(zip(base['cards'],ads['cards'])):
    def box(r):return(0,round(r['y']),390,round(r['bottom']))
    before=im('baseline-list').crop(box(b));after=im('local-partner-list').crop(box(a))
    diff=ImageChops.difference(before,after)
    rows=[y for y in range(diff.height) if diff.crop((0,y,390,y+1)).getbbox()]
    # A new adjacent surface changes raster blending at the shared edge. Keep
    # that evidence explicit; compare all original type and surface interiors.
    interior=(0,8,390,before.height-8)
    checks[f'ad_event_card_{i+1}_interior_pixels_unchanged']=equal(before.crop(interior),after.crop(interior))
    checks[f'ad_event_card_{i+1}_dimensions_unchanged']=b['width']==a['width'] and b['height']==a['height']
    boundaries.append({'card':i+1,'raw_crop_pixel_equal':not rows,'differing_rows':rows,'content_and_surface_interior_equal':checks[f'ad_event_card_{i+1}_interior_pixels_unchanged']})
base_event=next(m for m in metrics if m['slug']=='baseline' and m['kind']=='event')
rough=next(m for m in metrics if m['slug']=='rough-upload' and m['kind']=='event')
checks['rough_upload_foreground_geometry_type_color_unchanged']=base_event['foreground']==rough['foreground']
lock=json.loads((root/'baseline-lock.json').read_text())
hash_file=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks['approved_original_and_copies_match_all_source_hashes']=all(hash_file((root/f['source']).resolve())==f['sha256']==hash_file(root/f['copy']) for f in lock['files'])
result={'checks':checks,'ad_card_boundary_compositing':boundaries,'locked_files':len(lock['files']),'passed':all(checks.values())}
(qa/'preservation-results.json').write_text(json.dumps(result,indent=2))
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
preview=Image.new('RGB',(1202,912),'#eeece7');d=ImageDraw.Draw(preview)
for i,(file,label) in enumerate([('local-partner-list','01  Ad in the list'),('local-partner-event-scrolled','01  Event after scrolling'),('rough-upload-event','02  Rough organizer upload')]):
    d.text((8+i*398,8),label,font=font,fill='#292e30');preview.paste(im(file),(8+i*398,48))
preview.save(qa/'practical-elements.png')
compare=Image.new('RGB',(1616,912),'#eeece7');d=ImageDraw.Draw(compare)
for i,(file,label) in enumerate([('approved-list','Approved Date Line'),('local-partner-list','Same cards + ad'),('approved-event','Approved event opening'),('rough-upload-event','Same geometry + poor photo')]):
    d.text((8+i*402,8),label,font=small,fill='#292e30');compare.paste(im(file),(8+i*402,48))
compare.save(qa/'source-comparison.png')
pair=Image.new('RGB',(1616,912),'#eeece7');d=ImageDraw.Draw(pair)
for i,(slug,label) in enumerate([('local-partner','01 Local Partner'),('rough-upload','02 Rough Upload')]):
    d.text((8+i*808,8),label,font=font,fill='#292e30')
    for j,kind in enumerate(['list','event']):pair.paste(im(f'{slug}-{kind}'),(8+i*808+j*398,48))
pair.save(qa/'two-pairs.png')
print(json.dumps(result,indent=2))
raise SystemExit(not result['passed'])
