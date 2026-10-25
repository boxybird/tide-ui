"""Portable source/reference archive; no dependencies or platform-specific build."""
from pathlib import Path
import hashlib
import zipfile

ROOT=Path(__file__).resolve().parents[1]
destination=ROOT/'dist';destination.mkdir(exist_ok=True)
archive=destination/'tide-responsive-app-1.0.3.zip'
files=[]
for p in ROOT.rglob('*'):
    rel=p.relative_to(ROOT)
    if not p.is_file() or 'dist' in rel.parts or '__pycache__' in rel.parts or p.suffix in {'.log','.pyc'}:continue
    files.append(p)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as out:
    for p in sorted(files):out.write(p,'tide-responsive-app/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as verify:
    if verify.testzip() is not None:raise ValueError('Archive integrity check failed')
    if 'tide-responsive-app/review.html' not in verify.namelist():raise ValueError('Review entry missing')
(destination/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(destination.glob('*.zip'))),encoding='utf-8')
print(f'{len(files)} files; {archive.stat().st_size:,} bytes; CRC verified.\n{archive}')
