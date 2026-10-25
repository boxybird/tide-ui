"""Preserve this study as a snapshot without writing to its dependencies."""
from pathlib import Path
import hashlib
import json
import zipfile
root=Path(__file__).resolve().parents[1]
dist=root/'dist';version='0.1.0'
archive=dist/f'venue-discovery-{version}.zip'
if archive.exists():raise SystemExit('Snapshot exists; choose a new version instead of overwriting it.')
files=sorted(p for p in root.rglob('*') if p.is_file() and 'dist' not in p.relative_to(root).parts and '__pycache__' not in p.parts)
inventory={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
dist.mkdir(exist_ok=True)
(dist/f'inventory-{version}.json').write_text(json.dumps({'version':version,'kind':'Venue discovery study; not an approved app or kit release','runtimeDependency':'Existing sibling shared-filter-release/kit/; serve from the desktop-studies root. This snapshot is not a standalone deployment.','files':inventory},indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,Path('venue-discovery')/p.relative_to(root))
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
(dist/f'venue-discovery-{version}.sha256').write_text(sha+'  '+archive.name+'\n',encoding='utf-8')
print(json.dumps({'files':len(files),'archive':archive.name,'sha256':sha},indent=2))
