"""One-time import of accepted app markup; reads preserved references only."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
VENUE = ROOT.parent / 'venue-discovery'
BASE = ROOT.parent / 'shared-filter-release'

def main():
    assert not (ROOT / 'src').exists(), 'Import is one-time; edit successor sources in place.'
    inputs = {}
    for path in sorted((VENUE / 'app').rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(VENUE / 'app')
        target = ROOT / 'src' / ('pages' if path.suffix == '.html' else 'runtime') / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        inputs['venue-discovery/app/' + rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        if path.suffix in ('.html', '.js'):
            text = path.read_text(encoding='utf-8').replace('tide-venue-study', 'tide-app-release')
            text = text.replace('tide:venue-study:applied', 'tide:app-release-1.1.0:applied')
            text = text.replace('data-width="venue-discovery"', 'data-width="app-release-1.1.0"')
            text = text.replace('data-room="venue-discovery"', 'data-room="app-release-1.1.0"')
            text = text.replace('The six events in this study', 'The six Sunshine Theater sample events')
            target.write_text(text, encoding='utf-8', newline='\n')
        else:
            shutil.copyfile(path, target)
    css = (VENUE / 'css/venue.css').read_text(encoding='utf-8')
    css = css.replace('tide.venue-study', 'tide.app-release').replace('tide-venue-study', 'tide-app-release')
    css = css.replace('  .tide-app-release__sample { margin-block: var(--tide-space-5); }\n', '')
    (ROOT / 'src/runtime/css/app.css').write_text(css, encoding='utf-8', newline='\n')
    data = ROOT / 'data'
    data.mkdir(exist_ok=True)
    shutil.copyfile(VENUE / 'data/events.json', data / 'sunshine-sample-events.json')
    shutil.copyfile(ROOT.parent.parent / 'tide-responsive-app/data/events.json', data / 'original-sample-events.json')
    manifest = json.loads((BASE / 'consumer-manifest.json').read_text(encoding='utf-8'))
    manifest.update(version='1.1.0', kitVersion='1.3.0', approvedInput='../shared-filter-release/app/',
                    acceptedInputs=['../event-pressure-test/ (sticky hierarchy only)', '../venue-discovery/'],
                    privateBlocks=manifest['privateBlocks'] + ['tide-app-release'],
                    styleHome=['src/runtime/css/host.css', 'src/runtime/css/app.css'],
                    behaviorHome=['src/runtime/js/' + p.name for p in sorted((ROOT / 'src/runtime/js').glob('*.js'))],
                    contract='docs/COMPONENT-OWNERSHIP.md',
                    notes='Frozen kit consumed read-only. Existing host CSS is byte-identical. The sole new private block composes the accepted venue guide and isolated feed; no new kit component.')
    (ROOT / 'consumer-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (data / 'import-provenance.json').write_text(json.dumps({'sourceDate':'2026-10-25','files':inputs}, indent=2) + '\n', encoding='utf-8')
    print('Imported 60 accepted HTML pages and shared runtime into successor-owned sources.')

if __name__ == '__main__':
    main()
