"""Write here only; verify the full preceding preservation chain."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
SPACES=PARENT/'lineup-filter-spaces'
sys.path.insert(0,str(SPACES/'tools'))
import space_context as previous
BARS=previous.BARS
APP=previous.APP

def verify():
    inventory=previous.verify()
    archive=SPACES/'dist/lineup-filter-spaces-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=SPACES/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Preserved Filter Spaces changed: '+name
    return {**inventory,'filterSpaceFiles':len(files)}
