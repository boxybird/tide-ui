"""Build all registered modes from one HTML/runtime source; never writes dependencies."""
from pathlib import Path
import argparse
import json
import os
import re
from html_templates import AppTemplates
from css_distribution import compact_css

ROOT = Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
KIT=PROJECT/'build/tide'
OUT=PROJECT/'build/events'
THEMES = json.loads((PROJECT/'packages/tide/tokens/themes.json').read_text(encoding='utf-8'))['themes']
MODES = [(theme, mode) for theme in THEMES for mode in ('light','dark')]

def relative(target, parent):
    return os.path.relpath(target, parent).replace('\\', '/')

def review_document(buttons):
    """Starter overview: private host outside the canonical Stack recipe."""
    return '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lineup application kit · Tide</title><link rel="stylesheet" href="../tide/css/tide.css"><link rel="stylesheet" href="runtime/css/app.css"></head><body class="tide"><main class="tide-app__review"><div class="tide-stack"><p class="tide-eyebrow">Lineup · application kit · option 1</p><h1 class="tide-page-intro__title">A familiar lineup. A place to explore.</h1><p>Lineup is layout family option 1: an independently versioned application kit derived from Tide UI. Burque Events supplies its sample content. The UI kit remains the source of truth; application layout and page composition live separately.</p><div class="tide-row"><a class="tide-button" href="app/index.html">Open the app</a><a class="tide-button tide-button--secondary" href="app/sunshine-theater.html">Explore Sunshine Theater</a></div><div class="tide-notice"><strong>54 authored sample events</strong><p>The original 48 examples plus six fictional Sunshine Theater shows. Venue facts are attributed separately; this is a local HTML release with no live listings, accounts or submissions.</p></div><section class="tide-stack"><h2 class="tide-event-details__section-title">Theme variants</h2><div class="tide-row">'''+buttons+'''</div><p class="tide-caption">Each theme includes the full lineup, event pages, venue information, Saved, submission layout and Help.</p></section><section class="tide-stack"><h2 class="tide-event-details__section-title">Reference layouts</h2><p>Alternate result layouts for kit review. These destinations are separate from the application navigation; search integration is described in the handoff contract.</p><nav class="tide-row" aria-label="Global result references"><a class="tide-link" href="app/search-music.html">Music</a><a class="tide-link" href="app/search-comedy.html">Comedy</a><a class="tide-link" href="app/search-workshop.html">Workshops</a><a class="tide-link" href="app/search-empty.html">Empty results</a></nav><nav class="tide-row" aria-label="Venue result references"><a class="tide-link" href="app/sunshine-theater-comedy.html">Venue: Comedy</a><a class="tide-link" href="app/sunshine-theater-workshop.html">Venue: Workshops</a><a class="tide-link" href="app/sunshine-theater-empty.html">Venue: Empty results</a></nav></section><p><a class="tide-link" href="README.md">Release notes and build instructions</a> · <a class="tide-link" href="docs/COMPONENT-OWNERSHIP.md">Component and behavior ownership</a> · <a class="tide-link" href="docs/STARTER.md">Consumer starting point</a> · <a class="tide-link" href="docs/HANDOFF.md">Handoff and integration contract</a> · <a class="tide-link" href="docs/AUDIT.md">Application audit</a> · <a class="tide-link" href="qa/VERIFICATION.md">Verification record</a></p></div></main></body></html>'''

def build(check=False):
    expected = {}
    for source in sorted((ROOT / 'src/runtime').rglob('*')):
        if source.is_file():
            expected[OUT / 'runtime' / source.relative_to(ROOT / 'src/runtime')] = source.read_bytes()
    manifest = json.loads((ROOT/'consumer-manifest.json').read_text(encoding='utf-8'))
    kit_manifest = json.loads((PROJECT/'packages/tide/component-manifest.json').read_text(encoding='utf-8'))
    assert manifest['kitVersion'] == kit_manifest['version'], 'Review the application against the current Tide version and update kitVersion.'
    behavior_sources = [ROOT/name for name in manifest['behaviorHome']]
    assert not behavior_sources and not list((ROOT/'src/runtime').rglob('*.js')), 'Browser JavaScript is forbidden in the native example.'
    css_sources = [ROOT/name for name in manifest['styleHome']]
    assert set(css_sources) == set((ROOT/'src/styles').glob('*.css')), 'Register every app stylesheet in consumer-manifest.json, in cascade order.'
    css = '/* App composition only; generated from src/styles/. */\n' + compact_css('\n'.join(source.read_text(encoding='utf-8') for source in css_sources))
    expected[OUT/'runtime/css/app.css'] = css.encode('utf-8')
    # Consume the existing public extension byte-for-byte. Its source remains in
    # Tide; only this application's generated dependency copy is emitted here.
    expected[OUT/'runtime/css/tide-panel.css'] = (PROJECT/'packages/tide/extensions/panel.css').read_bytes()
    templates = AppTemplates()
    rendered_pages = templates.pages()
    destinations = [(OUT / 'app', 'bumble', 'dark')] + [(OUT / 'themes' / (t+'-'+m), t, m) for t,m in MODES]
    for directory, theme, mode in destinations:
        for name, text in rendered_pages.items():
            text = re.sub(r'data-theme="[^"]+"', 'data-theme="'+theme+'"', text, count=1)
            text = re.sub(r'data-mode="[^"]+"', 'data-mode="'+mode+'"', text, count=1)
            text = text.replace('{{KIT_CSS}}', relative(KIT/'css/tide.css', directory))
            text = text.replace('{{KIT_NAV_CSS}}', relative(KIT/'extensions/navigation.css', directory))
            text = text.replace('{{KIT_PANEL_CSS}}', relative(OUT/'runtime/css/tide-panel.css', directory))
            text = text.replace('{{APP_CSS}}', relative(OUT / 'runtime/css/app.css', directory))
            text = text.replace('{{KIT_ASSETS}}', relative(KIT/'assets', directory))
            text = re.sub(r'((?:href|src)=")(js/[^"<>]+|assets/[^"<>]+)(")',
                          lambda m:m[1]+relative(OUT / 'runtime' / m[2], directory)+m[3], text)
            text = text.replace('data-state-key="app-release-1.1.0"','data-state-key="app-release-1.1.0-'+theme+'-'+mode+'"')
            expected[directory / name] = text.encode('utf-8')
    buttons = ''.join('<a class="tide-button tide-button--secondary" href="themes/'+t+'-'+m+'/index.html">'+t.title()+' '+m+'</a>' for t,m in MODES)
    review = review_document(buttons)
    review=review.replace('</head>','<link rel="preload" href="../tide/assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin></head>')
    expected[OUT / 'index.html'] = review.encode('utf-8')
    for p in [ROOT/'README.md',ROOT/'design-qa.md',*(ROOT/'docs').rglob('*')]:
        if not p.is_file():continue
        content=p.read_bytes()
        if p.suffix=='.md':
            content=p.read_text(encoding='utf-8').replace('../../../docs/','../../docs/').replace('../../../packages/tide/docs/','../../site/docs/').encode('utf-8')
        expected[OUT/p.relative_to(ROOT)]=content
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
    print(('Checked' if check else 'Built')+f' {len(rendered_pages)*len(destinations)} app pages (default + {len(MODES)} modes), one review, and one shared runtime.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
