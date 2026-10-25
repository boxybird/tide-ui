"""Read-only access and complete preservation locks for the approved foundation."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
APP = ROOT/'base' if (ROOT/'base').is_dir() else ROOT.parent/'tide-responsive-app'


def hashes(folder):
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file()}


def lock():
    for name, folder in [('app-1.3.1', APP), ('kit-1.2.1', APP/'kit')]:
        path = ROOT/'locks'/f'{name}.json'
        current = hashes(folder)
        if path.exists():
            previous = json.loads(path.read_text(encoding='utf-8'))
            if previous != current:
                changed = sorted(k for k in previous.keys() | current.keys() if previous.get(k) != current.get(k))
                raise ValueError(f'Frozen {name} changed: '+', '.join(changed))
        else:
            raise ValueError('Missing preservation lock: '+str(path))
    return True


if __name__ == '__main__':
    if '--initialize' in sys.argv:
        (ROOT/'locks').mkdir(parents=True, exist_ok=True)
        for name, folder in [('app-1.3.1', APP), ('kit-1.2.1', APP/'kit')]:
            path = ROOT/'locks'/f'{name}.json'
            if path.exists():
                raise SystemExit('Refusing to replace an existing lock: '+str(path))
            files = hashes(folder)
            path.write_text(json.dumps(files, indent=2)+'\n', encoding='utf-8')
            print(f'{name}: locked {len(files)} files.')
    else:
        lock()
        print('App 1.3.1 and kit 1.2.1 remain byte-identical.')
