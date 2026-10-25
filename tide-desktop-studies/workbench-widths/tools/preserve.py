"""Read-only preservation of the complete app, kit and first desktop collection."""
from pathlib import Path
import hashlib
import json
import sys
from zipfile import ZipFile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(PARENT/'tools'))
from foundation import APP, lock


def preserve():
    lock()
    archive = PARENT/'dist/wide-open-desktop-studies-1.0.0.zip'
    digest = (archive.parent/(archive.name+'.sha256')).read_text().split()[0]
    if hashlib.sha256(archive.read_bytes()).hexdigest() != digest:
        raise ValueError('Original desktop-study archive changed.')
    with ZipFile(archive) as bundle:
        files = json.loads(bundle.read('RELEASE.json'))['files']
    for name, digest in files.items():
        path = PARENT/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Original desktop study changed: '+name)
    return len(files)


if __name__ == '__main__':
    print(f'{preserve()} original desktop-study files unchanged; app and kit locks pass.')
