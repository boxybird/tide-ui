"""Extend preservation through Reading Widths; write only to this new sibling."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
READING=PARENT/'lineup-reading-widths'
sys.path.insert(0,str(READING/'tools'))
import room_context as previous
APP=previous.APP
SLIDING=previous.SLIDING

def verify():
    inventory=previous.verify()
    archive=READING/'dist/lineup-reading-widths-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=READING/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Preserved Reading Widths changed: '+name
    return {**inventory,'readingWidthFiles':len(files)}
