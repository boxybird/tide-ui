"""Build all six modes from one HTML/runtime source; never writes dependencies."""
from pathlib import Path
import argparse
import json
import os
import re
from html_templates import AppTemplates

ROOT = Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
KIT=PROJECT/'build/tide'
OUT=PROJECT/'build/events'
MODES = [(theme, mode) for theme in ('tide','summer','bumble') for mode in ('light','dark')]

def relative(target, parent):
    return os.path.relpath(target, parent).replace('\\', '/')

def build(check=False):
    expected = {}
    for source in sorted((ROOT / 'src/runtime').rglob('*')):
        if source.is_file():
            expected[OUT / 'runtime' / source.relative_to(ROOT / 'src/runtime')] = source.read_bytes()
    manifest = json.loads((ROOT/'consumer-manifest.json').read_text(encoding='utf-8'))
    css_sources = [ROOT/name for name in manifest['styleHome']]
    assert set(css_sources) == set((ROOT/'src/styles').glob('*.css')), 'Register every app stylesheet in consumer-manifest.json, in cascade order.'
    css = '/* App composition only; generated from src/styles/. */\n' + '\n'.join(source.read_text(encoding='utf-8') for source in css_sources)
    expected[OUT/'runtime/css/app.css'] = css.encode('utf-8')
    templates = AppTemplates()
    rendered_pages = templates.pages()
    destinations = [(OUT / 'app', 'bumble', 'dark')] + [(OUT / 'themes' / (t+'-'+m), t, m) for t,m in MODES]
    for directory, theme, mode in destinations:
        for name, text in rendered_pages.items():
            text = re.sub(r'data-theme="[^"]+"', 'data-theme="'+theme+'"', text, count=1)
            text = re.sub(r'data-mode="[^"]+"', 'data-mode="'+mode+'"', text, count=1)
            text = text.replace('{{KIT_CSS}}', relative(KIT/'css/tide.css', directory))
            text = text.replace('{{APP_CSS}}', relative(OUT / 'runtime/css/app.css', directory))
            text = text.replace('{{KIT_ASSETS}}', relative(KIT/'assets', directory))
            text = re.sub(r'((?:href|src)=")(js/[^"<>]+|assets/[^"<>]+)(")',
                          lambda m:m[1]+relative(OUT / 'runtime' / m[2], directory)+m[3], text)
            text = text.replace('data-state-key="app-release-1.1.0"','data-state-key="app-release-1.1.0-'+theme+'-'+mode+'"')
            expected[directory / name] = text.encode('utf-8')
    buttons = ''.join('<a class="tide-button tide-button--secondary" href="themes/'+t+'-'+m+'/index.html?preview-filters=open">'+t.title()+' '+m+'</a>' for t,m in MODES)
    review = '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Burque events example · Tide</title><link rel="stylesheet" href="../tide/css/tide.css"><link rel="stylesheet" href="runtime/css/app.css"></head><body class="tide"><main class="tide-app__review tide-stack"><p class="tide-eyebrow">Burque events · reference example</p><h1 class="tide-page-intro__title">A familiar lineup. A place to explore.</h1><p>The approved app layout, accepted sticky-heading correction and Sunshine Theater venue journey, together in a separate successor. The maintained Tide kit is shared by this example and the component reference site.</p><div class="tide-row"><a class="tide-button" href="app/index.html?preview-filters=open">Open the app</a><a class="tide-button tide-button--secondary" href="app/sunshine-theater.html?preview-filters=open">Explore Sunshine Theater</a></div><div class="tide-notice"><strong>54 authored sample events</strong><p>The original 48 examples plus six fictional Sunshine Theater shows. Venue facts are attributed separately; this is a local HTML release with no live listings, accounts or submissions.</p></div><section class="tide-stack"><h2 class="tide-event-details__section-title">Same app, six theme/mode examples</h2><div class="tide-row">'''+buttons+'''</div><p class="tide-caption">Every example includes the full list, native event URLs, venue journey, search and filters, saved/submission samples and help page.</p></section><section class="tide-stack"><h2 class="tide-event-details__section-title">Try the accepted patterns</h2><ol><li>Scroll the list across October and November: date headings pass behind the permanent desktop lineup summary.</li><li>Open <a class="tide-link" href="app/high-desert-signal.html?inspect=1&amp;preview-filters=open">High Desert Signal</a>, follow its Sunshine Theater link, then choose another show.</li><li>On the venue page, try <a class="tide-link" href="app/sunshine-theater.html?q=Signal">one result</a>, <a class="tide-link" href="app/sunshine-theater.html?q=ink">no results</a> and Reset all. Use All events to leave venue scope.</li><li>Resize to tablet or phone to use the existing search/filter flyout and the phone venue-details jump.</li></ol></section><p><a class="tide-link" href="README.md">Release notes and build instructions</a> · <a class="tide-link" href="docs/COMPONENT-OWNERSHIP.md">Component and behavior ownership</a> · <a class="tide-link" href="qa/VERIFICATION.md">Verification record</a></p></main></body></html>'''
    expected[OUT / 'index.html'] = review.encode('utf-8')
    for p in [ROOT/'README.md',*(ROOT/'docs').glob('*.md')]:expected[OUT/p.relative_to(ROOT)]=p.read_bytes()
    expected[OUT/'README.md']=(ROOT/'README.md').read_text(encoding='utf-8').replace('../../docs/','../docs/').encode('utf-8')
    for p in (PROJECT/'docs/migration').iterdir():
        if p.is_file():expected[OUT/'qa'/p.name]=p.read_bytes()
    for path, content in expected.items():
        if check:
            assert path.is_file() and path.read_bytes() == content, 'Stale output: '+str(path.relative_to(PROJECT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    generated = {p for folder in ('app','themes','runtime') for p in (OUT/folder).rglob('*') if p.is_file()}
    assert generated == {p for p in expected if p.relative_to(OUT).parts[0] in ('app','themes','runtime')}, 'Unexpected generated file; investigate rather than deleting silently.'
    print(('Checked' if check else 'Built')+' 420 app pages (default + six modes), one review, and one shared runtime.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
