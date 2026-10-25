"""Create an immutable local archive with an exact frozen kit dependency."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import io
import json
import posixpath

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT.parent/'shared-filter-release/kit'

def sha(content):
    return hashlib.sha256(content).hexdigest()

def main():
    source=json.loads((ROOT/'qa/checks.json').read_text(encoding='utf-8'))
    browser=json.loads((ROOT/'qa/browser-checks.json').read_text(encoding='utf-8'))
    assert source['pass'] and browser['pass'], 'Complete source and browser checks before packaging.'
    contents={}
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and 'dist' not in p.relative_to(ROOT).parts and '__pycache__' not in p.parts:
            contents[ROOT.name+'/'+p.relative_to(ROOT).as_posix()]=p.read_bytes()
    for p in sorted(KIT.rglob('*')):
        if p.is_file():contents['shared-filter-release/kit/'+p.relative_to(KIT).as_posix()]=p.read_bytes()
    class References(HTMLParser):
        def handle_starttag(self,tag,attrs):
            for key,value in attrs:
                if key not in ('href','src','action') or not value:continue
                url=urlsplit(value)
                if url.scheme or url.netloc or not url.path:continue
                target=posixpath.normpath(posixpath.join(posixpath.dirname(self.name),unquote(url.path)))
                assert target in contents, 'Archive missing runtime reference: '+self.name+' -> '+value
    for name,content in contents.items():
        if name.endswith('.html') and (name==ROOT.name+'/index.html' or name.startswith((ROOT.name+'/app/',ROOT.name+'/themes/'))):
            parser=References();parser.name=name;parser.feed(content.decode('utf-8'))
    inventory={name:sha(value) for name,value in contents.items()}
    record={'appVersion':'1.1.0','kitVersion':'1.3.0','date':'2026-10-25','entry':ROOT.name+'/index.html','dependency':'Exact frozen Tide kit snapshot; no source edits','files':inventory}
    contents['RELEASE.json']=(json.dumps(record,indent=2)+'\n').encode('utf-8')
    buffer=io.BytesIO()
    with ZipFile(buffer,'w',compression=ZIP_DEFLATED,compresslevel=9) as bundle:
        for name,content in sorted(contents.items()):
            info=ZipInfo(name,(2026,10,25,0,0,0));info.compress_type=ZIP_DEFLATED
            bundle.writestr(info,content,compress_type=ZIP_DEFLATED,compresslevel=9)
    payload=buffer.getvalue();dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    archive=dist/'burque-app-1.1.0.zip'
    if archive.exists():assert archive.read_bytes()==payload,'Versioned archive is immutable. Use a new version for changed content.'
    else:archive.write_bytes(payload)
    with ZipFile(archive) as bundle:
        assert all(sha(bundle.read(name))==digest for name,digest in inventory.items())
    (dist/'inventory-1.1.0.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    (dist/'burque-app-1.1.0.sha256').write_text(sha(payload)+'  burque-app-1.1.0.zip\n',encoding='utf-8')
    print(json.dumps({'archive':archive.name,'sha256':sha(payload),'files':len(contents),'bytes':len(payload)},indent=2))

if __name__=='__main__':main()
