"""Recover the exact approved 1.0.3 package into a browsable frozen baseline."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
destination=ROOT/'versions/1.0.3'
prefix='tide-responsive-app/'
files={}
with zipfile.ZipFile(ROOT/'dist/tide-responsive-app-1.0.3.zip') as archive:
    if archive.testzip() is not None:raise ValueError('Baseline archive failed CRC validation')
    for info in archive.infolist():
        if info.is_dir():continue
        if not info.filename.startswith(prefix):raise ValueError('Unexpected baseline archive root')
        relative=info.filename[len(prefix):]
        target=(destination/relative).resolve()
        target.relative_to(destination.resolve()) # Reject paths escaping the intended directory.
        data=archive.read(info)
        if target.exists() and target.read_bytes()!=data:raise ValueError('Frozen baseline differs: '+relative)
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
        files[relative]=hashlib.sha256(data).hexdigest()
(ROOT/'qa/iteration-1.0.3-lock.json').write_text(json.dumps(files,indent=2)+'\n',encoding='utf-8')
print(f'Frozen 1.0.3: {len(files)} files verified. Browse versions/1.0.3/index.html.')
