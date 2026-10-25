"""Read-only guards for the selected refinement and its complete release chain."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
REFINED=PARENT/'margin-reveal-refined'
sys.path.insert(0,str(REFINED/'tools'))
import refine_context as previous
APP=previous.APP

def verify():
    inventory=previous.verify()
    archive=REFINED/'dist/margin-reveal-refined-1.0.0.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=REFINED/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Selected refinement changed: '+name
    return {**inventory,'marginRefinedFiles':len(files)}
