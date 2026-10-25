"""Read preserved Lineup and earlier studies; write only this sibling."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
LINEUP=PARENT/'list-rhythm'
sys.path.insert(0,str(LINEUP/'tools'))
import context as previous
APP=previous.APP


def verify():
    inventory=previous.verify()
    archive=LINEUP/'dist/list-rhythm-1.1.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=LINEUP/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Preserved Lineup changed: '+name
    return {**inventory,'lineupFiles':len(files)}
