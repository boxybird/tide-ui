"""Guard every preceding release; this sibling is the only write target."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
BARS=PARENT/'lineup-control-bars'
sys.path.insert(0,str(BARS/'tools'))
import bar_context as previous
LINEUP=previous.LINEUP
APP=previous.APP

def verify():
    inventory=previous.verify()
    archive=BARS/'dist/lineup-control-bars-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle: files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=BARS/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Preserved Control Bars changed: '+name
    return {**inventory,'controlBarFiles':len(files)}
