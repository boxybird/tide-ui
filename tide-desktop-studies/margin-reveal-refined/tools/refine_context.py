"""Preserve the selected Margin Reveal release and its entire dependency chain."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
MARGIN=PARENT/'contained-margin-filters'
sys.path.insert(0,str(MARGIN/'tools'))
import margin_context as previous
APP=previous.APP

def verify():
    inventory=previous.verify()
    archive=MARGIN/'dist/contained-margin-filters-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=MARGIN/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Selected Margin Reveal changed: '+name
    return {**inventory,'marginRevealFiles':len(files)}
