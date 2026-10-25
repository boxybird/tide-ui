"""Save this isolated study without rewriting or repackaging the foundation."""
import hashlib
import json
import sys
from zipfile import ZIP_DEFLATED, ZipFile

sys.dont_write_bytecode = True
from foundation import ROOT, lock
from build import outputs


def main():
    lock()
    for name, html in outputs().items():
        if (ROOT/name).read_text(encoding='utf-8') != html:
            raise ValueError('Stale study document: '+name)
    if not json.loads((ROOT/'qa/source-check.json').read_text())['pass']:
        raise ValueError('Source checks must pass before saving a release.')
    files = {p.relative_to(ROOT).as_posix(): p for p in sorted(ROOT.rglob('*'))
             if p.is_file() and not {'dist','__pycache__'}.intersection(p.relative_to(ROOT).parts)}
    hashes = {name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in files.items()}
    manifest = {'name':'Wide Open desktop studies', 'version':'1.0.0',
                'dependency':'Adjacent tide-responsive-app, frozen at app 1.3.1 / kit 1.2.1',
                'files':hashes}
    destination = ROOT/'dist'; destination.mkdir(exist_ok=True)
    archive = destination/'wide-open-desktop-studies-1.0.0.zip'
    with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as bundle:
        for name,path in files.items(): bundle.write(path,name)
        bundle.writestr('RELEASE.json',json.dumps(manifest,indent=2)+'\n')
    with ZipFile(archive) as bundle:
        if bundle.testzip(): raise ValueError('Archive integrity check failed.')
        for name,digest in hashes.items():
            if hashlib.sha256(bundle.read(name)).hexdigest() != digest:
                raise ValueError('Archived bytes differ: '+name)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination/(archive.name+'.sha256')).write_text(digest+'  '+archive.name+'\n',encoding='utf-8')
    lock()
    print(f'Saved and verified {len(files)} study files: {archive.name} ({archive.stat().st_size:,} bytes).')
    print('Approved app and kit remain unchanged; archive dependency is recorded in RELEASE.json.')


if __name__ == '__main__': main()
