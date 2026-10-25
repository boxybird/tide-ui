"""Only this sibling is writable; extend every previous release lock."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
WIDTHS=PARENT/'contained-widths-search'
sys.path.insert(0,str(WIDTHS/'tools'))
import width_context as previous
APP=previous.APP
SLIDING=previous.SLIDING
READING=previous.READING

def verify():
    inventory=previous.verify()
    archive=WIDTHS/'dist/contained-widths-search-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=WIDTHS/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Preserved Width & Search changed: '+name
    return {**inventory,'containedWidthFiles':len(files)}
