"""Freeze the user-approved release; review artifacts live outside its tree."""
from pathlib import Path
from zipfile import ZipFile
import hashlib
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
STUDIES=ROOT.parent
BASE=STUDIES/'shared-filter-release'
LOCK=STUDIES/'locks/shared-filter-release-1.0.0.json'
sys.path.insert(0,str(BASE/'tools'))
from check import preservation

def inventory():
    return {p.relative_to(BASE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(BASE.rglob('*')) if p.is_file()}

def main():
    preceding=preservation()
    archive=BASE/'dist/tide-shared-filter-release-1.0.0.zip'
    checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert checksum==archive.with_name(archive.name+'.sha256').read_text().split()[0]
    with ZipFile(archive) as bundle:
        files=json.loads(bundle.read('RELEASE.json'))['files']
        for name,digest in files.items():
            assert hashlib.sha256(bundle.read(name)).hexdigest()==digest
            assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,'Release changed: '+name
    files=inventory()
    record={'name':'Shared Filters baseline','approved':'2026-10-24','kitVersion':'1.3.0',
            'releaseVersion':'1.0.0','root':'tide-desktop-studies/shared-filter-release',
            'archiveSha256':checksum,'files':files}
    if LOCK.exists():assert json.loads(LOCK.read_text(encoding='utf-8'))==record,'Approved baseline changed'
    else:LOCK.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    report={'pass':True,'name':record['name'],'kitVersion':'1.3.0','lockedFiles':len(files),
            'archiveSha256':checksum,'precedingPreservation':preceding}
    (ROOT/'qa/preservation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='precedingPreservation'},indent=2))

if __name__=='__main__':main()
