"""Build reproducible downloadable artifacts; no publishing or source-tree ZIPs."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib
import io
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def archive(name,files):
    record={key:hashlib.sha256(value).hexdigest() for key,value in sorted(files.items())}
    files={**files,'RELEASE.json':(json.dumps({'files':record},indent=2)+'\n').encode()}
    buffer=io.BytesIO()
    with ZipFile(buffer,'w',compression=ZIP_DEFLATED) as bundle:
        for path,content in sorted(files.items()):
            info=ZipInfo(path,(2026,10,25,0,0,0));info.compress_type=ZIP_DEFLATED
            info.create_system=3;info.external_attr=0o100644 << 16
            bundle.writestr(info,content,compress_type=ZIP_DEFLATED,compresslevel=9)
    payload=buffer.getvalue();target=ROOT/'dist'/name;target.parent.mkdir(exist_ok=True)
    if target.exists():assert target.read_bytes()==payload,'Existing versioned artifact differs. Increment version before replacing '+name
    else:target.write_bytes(payload)
    with ZipFile(target) as bundle:
        assert bundle.testzip() is None
        assert all(hashlib.sha256(bundle.read(key)).hexdigest()==value for key,value in record.items())
    return hashlib.sha256(payload).hexdigest()+'  '+name

def main():
    # Validate the current build, including inputs, before creating artifacts.
    subprocess.run([sys.executable,'-B',str(ROOT/'tools/check.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    version=json.loads((ROOT/'packages/tide/component-manifest.json').read_text(encoding='utf-8'))['version']
    files={}
    for p in (ROOT/'build/tide').rglob('*'):
        if p.is_file():files['tide/'+p.relative_to(ROOT/'build/tide').as_posix()]=p.read_bytes()
    for folder in ('css','templates','docs','extensions'):
        for p in (ROOT/'packages/tide'/folder).rglob('*'):
            if p.is_file():files['tide/'+p.relative_to(ROOT/'packages/tide').as_posix()]=p.read_bytes()
    files['tide/README.md']=(ROOT/'packages/tide/README.md').read_bytes()
    files['tide/LICENSE']=(ROOT/'LICENSE').read_bytes()
    rows=[archive('tide-ui-kit-'+version+'.zip',files)]
    reference={}
    for folder in ('tide','site','events','docs'):
        for p in (ROOT/'build'/folder).rglob('*'):
            if p.is_file():reference['reference/'+p.relative_to(ROOT/'build').as_posix()]=p.read_bytes()
    app_version=json.loads((ROOT/'examples/events/consumer-manifest.json').read_text(encoding='utf-8'))['version']
    # The consuming example can ship a patch without changing the kit version.
    rows.append(archive('tide-ui-reference-kit-'+version+'-events-'+app_version+'.zip',reference))
    (ROOT/'dist/SHA256SUMS.txt').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print('\n'.join(rows))

if __name__=='__main__':main()
