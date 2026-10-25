"""This sibling is writable; every preceding study remains a verified dependency."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
SLIDING=PARENT/'lineup-sliding-filters'
sys.path.insert(0,str(SLIDING/'tools'))
import slide_context as previous
APP=previous.APP

def verify():
    inventory=previous.verify()
    archive=SLIDING/'dist/lineup-sliding-filters-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle: files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=SLIDING/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Preserved Sliding Filters changed: '+name
    return {**inventory,'slidingFilterFiles':len(files)}
