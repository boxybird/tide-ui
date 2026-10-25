"""Lock/verify the accepted venue study; all writes are outside frozen trees."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'venue-discovery'
LOCK=ROOT/'locks/venue-discovery-0.1.0.json'
EXPECTED_ARCHIVE='a0a892b9c355d5e85f0b84b73abe27ce391fb076087d95a955e2dfc3d684ac2f'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    original=json.loads((STUDY/'dist/inventory-0.1.0.json').read_text(encoding='utf-8'))['files']
    source={p.relative_to(STUDY).as_posix():digest(p) for p in sorted(STUDY.rglob('*')) if p.is_file() and 'dist' not in p.relative_to(STUDY).parts}
    assert source==original,'Venue study source/evidence differs from its preserved snapshot'
    assert digest(STUDY/'dist/venue-discovery-0.1.0.zip')==EXPECTED_ARCHIVE,'Venue archive changed'
    current={p.relative_to(STUDY).as_posix():digest(p) for p in sorted(STUDY.rglob('*')) if p.is_file()}
    if LOCK.exists():
        assert current==json.loads(LOCK.read_text(encoding='utf-8'))['files'],'Accepted venue study changed (including added/removed files)'
    else:
        assert len(current)==len(original)+3,'Unexpected files in venue snapshot directory'
        lock={'accepted':'2026-10-24','scope':'Complete preserved venue study; venue page/navigation required in the next app release. Approved baseline and kit remain untouched.','root':'venue-discovery','contract':'release-handoffs/VENUE-DISCOVERY.md','archiveSHA256':EXPECTED_ARCHIVE,'files':current}
        LOCK.write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
    spec=importlib.util.spec_from_file_location('venue_carry_forward_preservation',ROOT/'event-pressure-test/tools/check.py')
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    preserved=prior.preserve()
    report={'pass':True,'venueStudyFilesPreserved':len(current),'baselineFilesPreserved':preserved['lockedFiles'],'acceptedStickyFixFilesPreserved':preserved['acceptedStickyFixFiles'],'archiveSHA256':EXPECTED_ARCHIVE,'studyEdits':0,'kitEdits':0,'contract':'release-handoffs/VENUE-DISCOVERY.md'}
    qa=ROOT/'release-handoffs/qa';qa.mkdir(exist_ok=True)
    (qa/'venue-preservation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
