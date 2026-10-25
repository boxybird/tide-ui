"""Package the current refinement without replacing prior release archives."""
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
import json
import sys
sys.dont_write_bytecode=True
from unified_context import ROOT,verify
if __name__=='__main__':
    preserved=verify()
    for name in ('source-check.json','browser-check.json','spacing-1.0.1.json','gutter-1.0.2.json'):assert json.loads((ROOT/'qa'/name).read_text(encoding='utf-8'))['pass']
    for version in ('1.0.0','1.0.1'):
        baseline=ROOT/f'dist/margin-reveal-unified-search-{version}.zip'
        baseline_digest=hashlib.sha256(baseline.read_bytes()).hexdigest()
        assert baseline_digest==(baseline.parent/(baseline.name+'.sha256')).read_text().split()[0]
        with ZipFile(baseline) as bundle:
            for name,digest in json.loads(bundle.read('RELEASE.json'))['files'].items():assert hashlib.sha256(bundle.read(name)).hexdigest()==digest
        preserved['unifiedSearch'+version.replace('.','')+'Archive']=baseline_digest
    archive=ROOT/'dist/margin-reveal-unified-search-1.0.2.zip'
    assert not archive.exists(),'Never overwrite a release.'
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and 'dist' not in p.relative_to(ROOT).parts and '__pycache__' not in p.relative_to(ROOT).parts}
    archive.parent.mkdir(exist_ok=True)
    with ZipFile(archive,'w',ZIP_DEFLATED) as bundle:
        for name in files:bundle.write(ROOT/name,name)
        bundle.writestr('RELEASE.json',json.dumps({'name':'Margin Reveal · Unified search','version':'1.0.2','date':'2026-10-24','preserved':preserved,'dependencyNote':'Requires adjacent preserved studies and app on the local server.','files':files},indent=2)+'\n')
    with ZipFile(archive) as bundle:
        for name,digest in files.items():assert hashlib.sha256(bundle.read(name)).hexdigest()==digest
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    (archive.parent/(archive.name+'.sha256')).write_text(digest+'  '+archive.name+'\n',encoding='utf-8')
    verify();print(json.dumps({'files':len(files),'archive':str(archive),'sha256':digest},indent=2))
