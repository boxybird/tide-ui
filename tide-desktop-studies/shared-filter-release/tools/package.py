"""Package the independent consumer and successor kit without replacing releases."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
verification=json.loads((ROOT/'qa/verification.json').read_text(encoding='utf-8'))
browser=json.loads((ROOT/'qa/browser.json').read_text(encoding='utf-8'))
assert verification['pass'] and browser['pass'],'Release requires passing source/preservation and browser evidence'
subprocess.run([sys.executable,'-B','tools/build_app.py','--check'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'-B','tools/build.py','--check'],cwd=ROOT/'kit',check=True)
kit_archive=ROOT/'kit/dist/tide-ui-kit-1.3.0.zip'
assert kit_archive.is_file(),'Build the standalone kit package first'
dist=ROOT/'dist';dist.mkdir(exist_ok=True)
archive=dist/'tide-shared-filter-release-1.0.0.zip'
assert not archive.exists(),'Refusing to replace a release'
files={}
for p in sorted(ROOT.rglob('*')):
    rel=p.relative_to(ROOT)
    if not p.is_file() or rel.parts[0]=='dist' or '__pycache__' in rel.parts or p.suffix=='.pyc':continue
    if rel.parts[:2]==('kit','dist') and p!=kit_archive:continue
    files[rel.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
with ZipFile(archive,'w',compression=ZIP_DEFLATED) as bundle:
    for rel in files:bundle.write(ROOT/rel,rel)
    bundle.writestr('RELEASE.json',json.dumps({'release':'1.0.0','kit':'1.3.0','files':files},indent=2)+'\n')
with ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    for rel,digest in files.items():assert hashlib.sha256(bundle.read(rel)).hexdigest()==digest
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_name(archive.name+'.sha256').write_text(digest+'  '+archive.name+'\n',encoding='utf-8')
print(f'{archive.name}: {len(files)} files; hash inventory and CRC verified. SHA256 {digest}')
