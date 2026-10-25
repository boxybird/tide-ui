"""Archive this sibling only after source and browser checks pass."""
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
import json
import sys
sys.dont_write_bytecode=True
from width_context import ROOT,verify
if __name__=='__main__':
    preserved=verify()
    for name in ('source-check.json','browser-check.json'):assert json.loads((ROOT/'qa'/name).read_text(encoding='utf-8'))['pass']
    archive=ROOT/'dist/contained-widths-search-1.0.0.zip'
    assert not archive.exists(),'Never overwrite a preserved release.'
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and 'dist' not in p.relative_to(ROOT).parts and '__pycache__' not in p.relative_to(ROOT).parts}
    release={'name':'Contained · Width & Search','version':'1.0.0','date':'2026-10-23','variants':['1216px','1280px','1344px'],'searchLayouts':['Below / full width','Below / compact','Beside / original'],'preserved':preserved,'dependencyNote':'Requires preserved adjacent app and study dependencies via existing local port4187 server.','files':files}
    archive.parent.mkdir(exist_ok=True)
    with ZipFile(archive,'w',ZIP_DEFLATED) as bundle:
        for name in files:bundle.write(ROOT/name,name)
        bundle.writestr('RELEASE.json',json.dumps(release,indent=2)+'\n')
    with ZipFile(archive) as bundle:
        for name,digest in files.items():assert hashlib.sha256(bundle.read(name)).hexdigest()==digest
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    (archive.parent/(archive.name+'.sha256')).write_text(digest+'  '+archive.name+'\n',encoding='utf-8')
    verify();print(json.dumps({'files':len(files),'archive':str(archive),'sha256':digest},indent=2))
