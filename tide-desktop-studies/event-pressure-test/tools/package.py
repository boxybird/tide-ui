"""Snapshot this experiment; no writes to its frozen baseline dependency."""
from pathlib import Path
import hashlib
import json
import zipfile

root=Path(__file__).resolve().parents[1]
version='0.1.1'
archive=root/'dist'/f'event-pressure-test-{version}.zip'
if archive.exists():raise SystemExit('Snapshot already exists; choose a new version rather than overwriting it.')
files=sorted(p for p in root.rglob('*') if p.is_file() and 'dist' not in p.relative_to(root).parts and '__pycache__' not in p.parts)
inventory={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
dist=root/'dist';dist.mkdir(exist_ok=True)
manifest={'version':version,'kind':'UI pressure-test experiment, not an approved baseline','baseline':'../shared-filter-release/ (283-file frozen release)','runtimeDependency':'Keep the existing sibling shared-filter-release/kit/ and the local study server; this is a study snapshot, not a standalone deployment.','files':inventory}
(dist/f'inventory-{version}.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,Path('event-pressure-test')/p.relative_to(root))
checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
(dist/f'event-pressure-test-{version}.sha256').write_text(checksum+'  '+archive.name+'\n',encoding='utf-8')
print(json.dumps({'files':len(files),'archive':archive.name,'sha256':checksum},indent=2))
