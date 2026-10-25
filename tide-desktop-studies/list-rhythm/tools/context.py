"""Read every preserved source; write only this new list-heading study."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT.parent
REFINEMENTS=PARENT/'half-split-refinements'
sys.path.insert(0,str(REFINEMENTS/'tools'))
import guard as prior
APP=prior.APP


def verify():
    inventories=prior.guard()
    archive=REFINEMENTS/'dist/half-split-refinements-1.0.0.zip'
    digest=(archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=digest:raise ValueError('Original refinement archive changed.')
    with ZipFile(archive) as bundle:files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=REFINEMENTS/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('Original refinement changed: '+name)
    return {**inventories,'refinementFiles':len(files)}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
