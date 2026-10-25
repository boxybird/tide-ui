from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
import json
root = Path(__file__).resolve().parent
checks = {}
source = Image.open(root / "source-event.png").convert("RGB")
for mode in ("gather","aperture","shutter"):
    image = Image.open(root / (mode+"-event.png")).convert("RGB")
    checks[mode] = {"event_difference_bounds":ImageChops.difference(source,image).getbbox()}
checks["list"] = {"difference_bounds":ImageChops.difference(Image.open(root/"source-list.png").convert("RGB"),Image.open(root/"list.png").convert("RGB")).getbbox()}
board = Image.new("RGB",(1212,900),"#101517")
draw = ImageDraw.Draw(board)
for index,mode in enumerate(("gather","aperture","shutter")):
    draw.text((8+404*index,12),mode.upper()+" / IN MOTION",fill="#edbd8b")
    board.paste(Image.open(root/(mode+"-mid.png")).convert("RGB"),(8+404*index,40))
board.save(root/"motion-studies.png")
comparison = Image.new("RGB",(1616,900),"#101517")
draw = ImageDraw.Draw(comparison)
for index,(label,file) in enumerate((("APPROVED","source-event.png"),("GATHER","gather-event.png"),("APERTURE","aperture-event.png"),("SHUTTER","shutter-event.png"))):
    draw.text((8+404*index,12),label,fill="#edbd8b")
    comparison.paste(Image.open(root/file).convert("RGB"),(8+404*index,40))
comparison.save(root/"endpoint-comparison.png")
(root/"pixel-checks.json").write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
