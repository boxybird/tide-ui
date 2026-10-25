"""Build the kit, reference site and example from this checkout only."""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def build(check=False):
    for source in ('packages/tide/tools/build.py','site/tools/build.py','examples/events/tools/build.py'):
        subprocess.run([sys.executable,'-B',str(ROOT/source),*(['--check'] if check else [])],cwd=ROOT,check=True)
    for source in (ROOT/'docs').rglob('*'):
        if not source.is_file():continue
        target=ROOT/'build/docs'/source.relative_to(ROOT/'docs')
        if check:assert target.is_file() and target.read_bytes()==source.read_bytes(),'Stale documentation copy: '+str(target.relative_to(ROOT))
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');build(parser.parse_args().check)
