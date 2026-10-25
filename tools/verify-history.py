"""Optional Git-object archive verification; never needed by normal builds."""
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    record=json.loads((ROOT/'docs/migration/history.json').read_text(encoding='utf-8'))
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    tag=record['tag']
    assert git('rev-parse',tag+'^{commit}')==record['commit'],'History tag commit changed'
    assert git('rev-parse',tag+'^{tree}')==record['tree'],'History tree changed'
    assert len(git('ls-tree','-r','--name-only',tag).splitlines())==record['trackedFiles'],'History file inventory changed'
    result=subprocess.run(['git','fsck','--full','--no-reflogs'],cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    print(f'{tag}: {record["trackedFiles"]} preserved files; commit/tree identity and Git object integrity verified.')

if __name__=='__main__':main()
