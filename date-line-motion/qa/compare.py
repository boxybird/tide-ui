from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
import json
root = Path(__file__).resolve().parent
results = {}
board = Image.new("RGB", (1616, 900), "#101517")
draw = ImageDraw.Draw(board)
for index, state in enumerate(("list", "event")):
    source = Image.open(root / f"source-{state}.png").convert("RGB")
    actual = Image.open(root / f"implementation-{state}.png").convert("RGB")
    delta = ImageChops.difference(source, actual)
    mask = delta.convert("L").point(lambda p: 255 if p else 0)
    results[state] = {"size": list(source.size), "difference_bounds": delta.getbbox(), "changed_pixels": sum(mask.histogram()[1:])}
    for offset, (label, image) in enumerate((("APPROVED " + state.upper(), source), ("MOTION " + state.upper(), actual))):
        x = 8 + (index * 2 + offset) * 404
        draw.text((x, 12), label, fill="#edbd8b")
        board.paste(image, (x, 40))
board.save(root / "source-comparison.png")
(root / "pixel-comparison.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
