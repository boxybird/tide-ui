"""Preserve every previously shipped source file, app and kit."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
WIDTHS = PARENT/'workbench-widths'
sys.path.insert(0,str(WIDTHS/'tools'))
spec = importlib.util.spec_from_file_location('prior_guard',WIDTHS/'tools/preserve.py')
prior = importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
APP = prior.APP


def guard():
    original = prior.preserve()
    archive = WIDTHS/'dist/workbench-widths-1.0.0.zip'
    expected = (archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
        raise ValueError('Preserved width-study archive changed.')
    with ZipFile(archive) as bundle: files=json.loads(bundle.read('RELEASE.json'))['files']
    for name,digest in files.items():
        path=WIDTHS/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError('Preserved width study changed: '+name)
    return {'desktopStudyFiles':original,'widthStudyFiles':len(files),'appFiles':980,'kitFiles':180}


if __name__=='__main__': print(json.dumps(guard(),indent=2))
