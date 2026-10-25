from pathlib import Path
from PIL import Image, ImageDraw
from html.parser import HTMLParser
import hashlib, json, zipfile
root = Path(__file__).resolve().parents[1]
workspace = root.parent
lock = json.loads((workspace / "date-line-in-practice/baseline-lock.json").read_text())
failures = []
for item in lock["files"]:
    for relative in ("source", "copy"):
        target = workspace / "date-line-in-practice" / item[relative]
        if hashlib.sha256(target.read_bytes()).hexdigest() != item["sha256"]:
            failures.append(str(target))
for name in ("screens.css", "cards.css", "themes.css", "fonts.css"):
    if (root/name).read_bytes() != (workspace/"quiet-assembly"/name).read_bytes():
        failures.append(name)
if failures:
    raise ValueError("Preservation mismatch: " + repr(failures))

class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name not in ("href", "src") or not value or value.startswith(("#", "http:", "https:", "data:")):
                continue
            target = (self.file.parent / value.split("#")[0].split("?")[0]).resolve()
            if not target.exists():
                failures.append(str(target))
for page in root.rglob("*.html"):
    parser = Links()
    parser.file = page
    parser.feed(page.read_text(encoding="utf-8"))
if failures:
    raise ValueError("Missing local references: " + repr(failures))

board = Image.new("RGB", (1616, 900), "#101517")
draw = ImageDraw.Draw(board)
frames = [("THE LIST", "implementation-list.png"), ("OPENING / 25% TIME", "open-25.png"), ("OPENING / 65% TIME", "open-65.png"), ("THE EVENT", "implementation-event.png")]
for index, (label, filename) in enumerate(frames):
    image = Image.open(root/"qa"/filename).convert("RGB")
    draw.text((8+404*index, 12), label, fill="#edbd8b")
    board.paste(image, (8+404*index, 40))
board.save(root/"qa/motion-sequence.png")

archive = root / "date-line-continuity.zip"
files = [p for p in root.rglob("*") if p.is_file() and "qa" not in p.relative_to(root).parts and p.suffix not in (".zip", ".log") and p.name != ".preview.pid"]
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
    for file in files:
        bundle.write(file, "date-line-continuity/" + file.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as bundle:
    if bundle.testzip() is not None:
        raise ValueError("Archive CRC check failed")
result = {"approvedHashChecks":len(lock["files"])*2,"unchangedStylesheets":4,"localReferences":"passed","archiveFiles":len(files),"archiveBytes":archive.stat().st_size,"archiveCRC":"passed"}
(root/"qa/delivery-check.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
