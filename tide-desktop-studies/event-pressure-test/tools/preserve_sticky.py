"""Record the accepted 0.1.1 fix without rewriting its source or snapshot."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[1]
inventory=root/'dist/inventory-0.1.1.json'
original=json.loads(inventory.read_text(encoding='utf-8'))['files']
files={}
for name,digest in original.items():
    if name in ('css/pressure.css','tools/build.py') or (name.startswith('qa/sticky-handoff/') and Path(name).suffix in ('.png','.json')):
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'Accepted fix changed: '+name
        files[name]=digest
archive='dist/event-pressure-test-0.1.1.zip'
expected='b0a0ff76ccde6dd85d501e8715a6de629cbec7f1b3126de68268df647f595d21'
assert hashlib.sha256((root/archive).read_bytes()).hexdigest()==expected,'Accepted snapshot changed'
for name in (archive,'dist/event-pressure-test-0.1.1.sha256','dist/inventory-0.1.1.json'):
    files[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
lock={'accepted':'2026-10-24','scope':'Sticky heading layering only; required in the next app release. Baseline and UI kit remain frozen.','root':'event-pressure-test','contract':'release-handoffs/STICKY-HEADINGS.md','files':dict(sorted(files.items()))}
target=root.parent/'locks/event-pressure-test-sticky-0.1.1.json'
serialized=json.dumps(lock,indent=2)+'\n'
if target.exists():
    assert target.read_text(encoding='utf-8')==serialized,'Existing acceptance lock differs; preserve it rather than overwriting'
else:target.write_text(serialized,encoding='utf-8')
print(json.dumps({'acceptedFixFiles':len(files),'archiveSHA256':expected,'lock':str(target)},indent=2))
