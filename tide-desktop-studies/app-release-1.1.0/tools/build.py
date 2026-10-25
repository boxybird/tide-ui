"""Build all six modes from one HTML/runtime source; never writes dependencies."""
from pathlib import Path
import argparse
import os
import re

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT.parent / 'shared-filter-release/kit'
MODES = [(theme, mode) for theme in ('tide','summer','bumble') for mode in ('light','dark')]

def relative(target, parent):
    return os.path.relpath(target, parent).replace('\\', '/')

def build(check=False):
    expected = {}
    for source in sorted((ROOT / 'src/runtime').rglob('*')):
        if source.is_file():
            expected[ROOT / 'runtime' / source.relative_to(ROOT / 'src/runtime')] = source.read_bytes()
    destinations = [(ROOT / 'app', 'bumble', 'dark')] + [(ROOT / 'themes' / (t+'-'+m), t, m) for t,m in MODES]
    for directory, theme, mode in destinations:
        for source in sorted((ROOT / 'src/pages').glob('*.html')):
            text = source.read_text(encoding='utf-8')
            text = re.sub(r'data-theme="[^"]+"', 'data-theme="'+theme+'"', text, count=1)
            text = re.sub(r'data-mode="[^"]+"', 'data-mode="'+mode+'"', text, count=1)
            text = text.replace('../../shared-filter-release/kit/', relative(KIT, directory) + '/')
            text = text.replace('../css/venue.css', relative(ROOT / 'runtime/css/app.css', directory))
            text = re.sub(r'((?:href|src)=")(css/host\.css|js/[^"<>]+|assets/[^"<>]+)(")',
                          lambda m:m[1]+relative(ROOT / 'runtime' / m[2], directory)+m[3], text)
            text = text.replace('data-width="app-release-1.1.0"','data-width="app-release-1.1.0-'+theme+'-'+mode+'"')
            text = text.replace('data-room="app-release-1.1.0"','data-room="app-release-1.1.0-'+theme+'-'+mode+'"')
            expected[directory / source.name] = text.encode('utf-8')
    buttons = ''.join('<a class="tide-button tide-button--secondary" href="themes/'+t+'-'+m+'/index.html?preview-filters=open">'+t.title()+' '+m+'</a>' for t,m in MODES)
    review = '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>App release 1.1.0 · Burque</title><link rel="stylesheet" href="../shared-filter-release/kit/css/tide.css"><link rel="stylesheet" href="runtime/css/host.css"><link rel="stylesheet" href="runtime/css/app.css"></head><body class="tide"><main class="tide-app-release__review tide-stack"><p class="tide-eyebrow">App release 1.1.0 · local review</p><h1 class="tide-page-intro__title">A familiar lineup. A place to explore.</h1><p>The approved app layout, accepted sticky-heading correction and Sunshine Theater venue journey, together in a separate successor. Tide kit 1.3.0 and all preserved versions remain unchanged.</p><div class="tide-row"><a class="tide-button" href="app/index.html?preview-filters=open">Open the app</a><a class="tide-button tide-button--secondary" href="app/sunshine-theater.html?preview-filters=open">Explore Sunshine Theater</a></div><div class="tide-notice"><strong>54 authored sample events</strong><p>The original 48 examples plus six fictional Sunshine Theater shows. Venue facts are attributed separately; this is a local HTML release with no live listings, accounts or submissions.</p></div><section class="tide-stack"><h2 class="tide-event-details__section-title">Same app, six theme/mode examples</h2><div class="tide-row">'''+buttons+'''</div><p class="tide-caption">Every example includes the full list, native event URLs, venue journey, search and filters, saved/submission samples and help page.</p></section><section class="tide-stack"><h2 class="tide-event-details__section-title">Try the accepted patterns</h2><ol><li>Scroll the list across October and November: date headings pass behind the permanent desktop lineup summary.</li><li>Open <a class="tide-link" href="app/high-desert-signal.html?inspect=1&amp;preview-filters=open">High Desert Signal</a>, follow its Sunshine Theater link, then choose another show.</li><li>On the venue page, try <a class="tide-link" href="app/sunshine-theater.html?q=Signal">one result</a>, <a class="tide-link" href="app/sunshine-theater.html?q=ink">no results</a> and Reset all. Use All events to leave venue scope.</li><li>Resize to tablet or phone to use the existing search/filter flyout and the phone venue-details jump.</li></ol></section><p><a class="tide-link" href="README.md">Release notes and build instructions</a> · <a class="tide-link" href="docs/COMPONENT-OWNERSHIP.md">Component and behavior ownership</a> · <a class="tide-link" href="qa/VERIFICATION.md">Verification record</a></p></main></body></html>'''
    expected[ROOT / 'index.html'] = review.encode('utf-8')
    for path, content in expected.items():
        if check:
            assert path.is_file() and path.read_bytes() == content, 'Stale output: '+str(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    generated = {p for folder in ('app','themes','runtime') for p in (ROOT/folder).rglob('*') if p.is_file()}
    assert generated == {p for p in expected if p != ROOT/'index.html'}, 'Unexpected generated file; investigate rather than deleting silently.'
    print(('Checked' if check else 'Built')+' 420 app pages (default + six modes), one review, and one shared runtime.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
