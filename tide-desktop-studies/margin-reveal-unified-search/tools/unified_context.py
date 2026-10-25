"""Read-only preservation chain for the unified search refinement."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
BROWSE=PARENT/'margin-reveal-browse-first'
sys.path.insert(0,str(BROWSE/'tools'))
import browse_context as previous
APP=previous.APP

def verify():
    inventory=previous.verify()
    archive=BROWSE/'dist/margin-reveal-browse-first-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=BROWSE/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Browse-first release changed: '+name
    return {**inventory,'browseFirstFiles':len(files)}
