"""Preserve the previous smaller-screen proposal and the approved desktop."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
RESPONSIVE=PARENT/'margin-reveal-responsive-filters'
sys.path.insert(0,str(RESPONSIVE/'tools'))
import responsive_context as previous
APP=previous.APP

def verify():
    inventory=previous.verify()
    archive=RESPONSIVE/'dist/margin-reveal-responsive-filters-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=RESPONSIVE/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Previous responsive study changed: '+name
    return {**inventory,'responsiveFilterFiles':len(files)}
