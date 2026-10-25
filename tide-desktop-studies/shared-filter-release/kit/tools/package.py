"""Create a portable source/reference archive using only the standard library."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
destination=ROOT/'dist'
destination.mkdir(exist_ok=True)
version=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))['version']
archive=destination/f'tide-ui-kit-{version}.zip'
if archive.exists():raise SystemExit('Refusing to replace an existing release: '+str(archive))
files=[]
for path in ROOT.rglob('*'):
    relative=path.relative_to(ROOT)
    if not path.is_file() or relative.parts[0]=='dist' or '__pycache__' in relative.parts:
        continue
    if path.suffix in {'.log','.pyc'}:
        continue
    files.append(path)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as output:
    for path in sorted(files):output.write(path,'tide-ui-kit/'+path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as verify:
    if verify.testzip() is not None:raise ValueError('Archive integrity check failed.')
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(destination/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(destination.glob('*.zip'))),encoding='utf-8')
print(f'{archive.name}: {len(files)} files; {archive.stat().st_size:,} bytes. CRC verified.')
