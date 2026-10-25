"""Compile paired OKLCH themes and static HTML fixtures. No runtime framework.

python tools/build.py          validate, then write all generated outputs
python tools/build.py --check validate and detect stale generated outputs
"""
from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import re
import sys

PROJECT=Path(__file__).resolve().parents[2]
ROOT=PROJECT/"packages/tide"
SITE=PROJECT/"site"
OUT=PROJECT/"build/site"
sys.path.insert(0,str(ROOT/"tools"))

from palette import css
from compiler import load_themes, theme_styles
from content import help_content
from filter_panel import specimen

SECTIONS = ['top', 'foundations', 'components', 'content-pages', 'screens', 'coverage', 'tokens', 'themes', 'extend']


def picker(themes, selected, mode, prefix):
    out = ['<section class="tide-theme-picker" aria-label="Theme and appearance"><p>Theme / appearance</p>']
    for section in SECTIONS:
        out.append(f'<div class="tide-theme-picker__links" data-for="{section}">')
        for key, theme in themes.items():
            for appearance in ('light', 'dark'):
                current = ' aria-current="page"' if key == selected and appearance == mode else ''
                out.append(f'<a href="{prefix}{key}-{appearance}/index.html#{section}"{current}>{escape(theme["name"])} · {appearance.title()}</a>')
        out.append('</div>')
    out.append('</section>')
    return ''.join(out)


def heading(number, label, title, description):
    return f'<div class="tide-doc-heading"><div><p class="tide-eyebrow">{number} / {label}</p><h2>{title}</h2></div><p>{description}</p></div>'


def code(value):
    return '<pre class="tide-doc-code"><code>' + escape(value) + '</code></pre>'


def adopted_patterns(level):
    fragment=(ROOT/'templates/adopted-patterns.html').read_text(encoding='utf-8')
    svg=(ROOT/'assets/icons/ChevronDownIcon.svg').read_text(encoding='utf-8')
    svg=re.sub(r'<svg[^>]*>', '<svg class="tide-icon tide-expandable__icon" viewBox="0 0 15 15" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">', svg)
    svg=re.sub(r'fill="#[0-9a-fA-F]+"','fill="currentColor"',svg)
    for key,value in {'{{PANEL_LEVEL}}':str(level),'{{GROUP_LEVEL}}':str(level+1),'{{CARD_LEVEL}}':str(level+2),'{{DISCLOSURE_ICON}}':svg}.items():fragment=fragment.replace(key,value)
    return fragment


def contracts(themes, resolved, selected, mode, base):
    role_groups = {
        'Surfaces': ['canvas','surface','raised','field'],
        'Text': ['text-primary','text-secondary','text-muted','text-label'],
        'Actions': ['accent','on-accent','accent-hover','focus'],
        'Boundaries': ['border-subtle','border-strong','border-control'],
        'Selection': ['selected-surface','selected-text','selected-border'],
        'Status': [f'status-{status}-{suffix}' for status in ('success','warning','danger') for suffix in ('text','surface','border')],
    }
    out = ['<section class="tide-doc-section" id="tokens">', heading('05','Tokens','Names that describe the job.','Components consume stable semantic roles. Mode-specific values live behind those roles, so the HTML stays the same.')]
    out.append('<div class="tide-doc-grid"><article class="tide-doc-panel"><h3>Three levels, one direction</h3><ol class="tide-doc-rules"><li><strong>Primitives</strong> set fixed font, spacing, radius, target and border rules.</li><li><strong>Semantic roles</strong> describe canvas, content, actions, selection and status.</li><li><strong>Component tokens</strong> alias those roles only when a component needs a documented extension point.</li></ol></article><article class="tide-doc-panel"><h3>A mode is not a theme</h3><p class="tide-u-muted">Tide, Summer and Bumble are themes. Light, dark and system are appearance modes. Choose each independently on the root element.</p>')
    out.append(code('<html lang="en" data-theme="tide" data-mode="dark">\n  <body class="tide">…</body>\n</html>'))
    out.append('</article></div><div class="tide-doc-panel tide-u-mt-8"><h3>Public color contract</h3><p class="tide-caption">Current view: '+escape(themes[selected]['name'])+' / '+mode.title()+'. Names are identical in every theme and mode.</p><table class="tide-doc-table"><thead><tr><th scope="col">Family</th><th scope="col">Component-facing token</th><th scope="col">Resolved value</th></tr></thead><tbody>')
    for group, roles in role_groups.items():
        for i, role in enumerate(roles):
            out.append('<tr><td>'+escape(group if i == 0 else '')+'</td><td><code>--tide-color-'+role+'</code></td><td><code>'+css(resolved[selected][mode][role])+'</code></td></tr>')
    out.append('</tbody></table></div></section>')
    out.extend(['<section class="tide-doc-section" id="themes">',heading('06','Themes',f'{len(themes)} themes. {len(themes)*2} considered modes.','A theme may change colors and texture strength. Type, spacing, corners, structure and control sizes remain fixed.'),'<div class="tide-doc-theme-grid">'])
    for key, theme in themes.items():
        out.append('<article class="tide-doc-panel"><h3>'+escape(theme['name'])+'</h3><p class="tide-caption">'+escape(theme['description'])+'</p><div class="tide-doc-theme-pair">')
        for appearance in ('light','dark'):
            out.append(f'<a href="{base}{key}-{appearance}/index.html#components">{appearance.title()}</a>')
        out.append('</div></article>')
    out.append('</div><div class="tide-doc-grid tide-u-mt-8"><article class="tide-doc-panel"><h3>The background is part of the contract</h3><p class="tide-u-muted">A new canvas seed regenerates its surfaces, readable text, control edges, status text and focus colors. The compiler measures the actual foreground/background pairs before writing CSS.</p><p class="tide-caption tide-u-mt-7">Normal text ≥ 4.5:1. Meaningful control edges and focus ≥ 3:1. Decorative panel rules are intentionally quieter.</p></article><article class="tide-doc-panel"><h3>System appearance, without JavaScript</h3><p class="tide-u-muted">Use <code>data-mode="system"</code>, or omit data-mode. Native color-scheme and light-dark() follow the device preference. Explicit light or dark overrides it.</p><p class="tide-u-mt-7"><a class="tide-link" href="'+base+'system.html">Open the system-mode example</a></p></article></div></section>')
    out.extend(['<section class="tide-doc-section" id="extend">',heading('07','Extend','A repeatable way to grow.','Add a theme or a component without editing the existing component definitions or changing the selected visual foundation.'),'<div class="tide-doc-grid"><article class="tide-doc-panel"><h3>Add a theme</h3><ol class="tide-doc-rules"><li>Add a named entry in <code>tokens/themes.json</code>, including light and dark canvas/accent seeds.</li><li>Run <code>python tools/build.py</code>. Surfaces and foregrounds are resolved together.</li><li>Review both modes, all states and the contrast report. Commit source and generated CSS together.</li></ol><p class="tide-caption tide-u-mt-7">The gate rejects missing modes, duplicate names, invalid colors and failing pairs. A direct CSS override bypasses that guarantee.</p></article><article class="tide-doc-panel"><h3>Add a component</h3><ol class="tide-doc-rules"><li>Use a new BEM block: <code>.tide-panel</code>, its elements and explicit modifiers.</li><li>Consume the existing semantic roles and spacing tokens. Add a new role only when no existing role fits.</li><li>Put the addition in a later component layer; document its states and add a fixture in every theme/mode.</li></ol></article></div><article class="tide-doc-panel tide-u-mt-8"><h3>Example: a new panel, with no core mutation</h3>'])
    out.append(code('@layer tide.components.extensions {\n  .tide-panel {\n    --tide-panel-background: var(--tide-color-surface);\n    --tide-panel-padding: var(--tide-space-6);\n    display: grid;\n    gap: var(--tide-space-3);\n    padding: var(--tide-panel-padding);\n    border: var(--tide-border-hairline);\n    border-radius: var(--tide-radius-panel);\n    background: var(--tide-panel-background);\n    color: var(--tide-color-text-primary);\n  }\n}'))
    out.append('<p class="tide-caption tide-u-mt-7"><a class="tide-link" href="'+base+'extensions/index.html">Open the working panel example</a>. Keep new rules inside the named layer. Do not override a theme with component selectors.</p></article><p class="tide-u-mt-8"><a class="tide-link" href="'+base+'README.md">Implementation guide</a> · <a class="tide-link" href="'+base+'docs/THEMING.md">Theme authoring</a> · <a class="tide-link" href="'+base+'docs/COMPONENTS.md">Component inventory</a> · <a class="tide-link" href="'+base+'docs/COMPATIBILITY.md">Browser support and verification</a></p></section>')
    return ''.join(out)


def document(body, title, theme, mode, prefix, docs=False):
    return '<!doctype html>\n<html lang="en"'+(' class="tide-frame"' if not docs else '')+' data-theme="'+theme+'" data-mode="'+mode+'">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>'+escape(title)+'</title>\n<link rel="preload" href="'+prefix+'assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="'+prefix+'css/tide.css">\n'+('<link rel="stylesheet" href="'+prefix+'css/docs.css">\n' if docs else '')+'</head>\n'+body+'\n</html>\n'


def outputs(themes, resolved, audit):
    result={}
    version=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))['version']
    extra = '\n'.join(f".tide-library:has(#{section}:target) .tide-theme-picker__links[data-for='{section}'] {{ display:grid; }}" for section in SECTIONS[1:])
    result[ROOT/'css/docs-navigation.css'] = '@layer tide.docs {\n'+extra+'\n}\n'
    template = (ROOT/'templates/library.html').read_text(encoding='utf-8').replace('{{ADOPTED_PATTERNS}}',adopted_patterns(3)).replace('{{FILTER_PANEL}}',specimen(4))
    for key, theme in themes.items():
        for mode in ('light','dark'):
            for at_root in ([False, True] if key == 'tide' and mode == 'dark' else [False]):
                folder = ROOT if at_root else ROOT/f'{key}-{mode}'
                base = '' if at_root else '../'
                frame_prefix = 'tide-dark/frames/' if at_root else 'frames/'
                body = template.replace('{{THEME_PICKER}}', picker(themes,key,mode,base)).replace('{{CONTRACT_SECTIONS}}', contracts(themes,resolved,key,mode,base))
                for token, value in {'{{ASSETS}}':base+'assets/','{{FRAMES}}':frame_prefix,'{{BASE}}':base,'{{THEME_NAME}}':escape(theme['name']),'{{MODE_NAME}}':mode.title(),'{{KIT_VERSION}}':version}.items(): body=body.replace(token,value)
                body=body.replace('One structure. Three themes.',f'One structure. {len(themes)} themes.')
                html = document(body, f'Tide UI kit · {theme["name"]} / {mode.title()}', key,mode,base,True)
                html = html.replace('</head>','<link rel="stylesheet" href="'+base+'css/docs-navigation.css">\n</head>')
                result[folder/'index.html'] = html
            for source in (ROOT/'templates/frames').glob('*.html'):
                body = source.read_text(encoding='utf-8').replace('{{ADOPTED_PATTERNS}}',adopted_patterns(2)).replace('{{FILTER_PANEL}}',specimen()).replace('{{HELP_CONTENT}}',help_content({'BROWSE':'01-list.html','SEARCH':'search.html','SUBMIT':'submit.html','EVENT':'01-event.html'})).replace('{{ASSETS}}','../../assets/').replace('{{FRAMES}}','')
                title = source.stem.replace('-',' ').title() + ' · ' + theme['name'] + ' / ' + mode.title()
                result[ROOT/f'{key}-{mode}'/'frames'/source.name] = document(body,title,key,mode,'../../',docs=source.name in ('app-patterns.html','filter-panel.html'))
    system = '<body class="tide tide-screen tide-screen--kit"><main class="tide-page-body tide-page-body--spaced tide-stack"><p class="tide-eyebrow">System appearance</p><h1>Day or night.</h1><p>This page has no mode-switching JavaScript. Change your operating system appearance to test it.</p><div class="tide-notice"><strong>The same roles, in both modes.</strong><p>Native form controls and page surfaces use the active color scheme.</p></div><div class="tide-field"><label class="tide-field__label" for="sample">A native control</label><input class="tide-field__control" id="sample" value="Ink After Dark"></div><a class="tide-button" href="index.html#themes">Back to the kit</a></main></body>'
    result[ROOT/'system.html'] = document(system,'Tide · System appearance','tide','system','')
    panel=(ROOT/'templates/panel.html').read_text(encoding='utf-8')
    for key, theme in themes.items():
        for mode in ('light','dark'):
            links='<nav class="tide-row" aria-label="Panel theme fixtures">'
            for other, meta in themes.items():
                for appearance in ('light','dark'):
                    current=' aria-current="page"' if key==other and mode==appearance else ''
                    links+=f'<a class="tide-chip" href="{other}-{appearance}.html"{current}>{escape(meta["name"])} / {appearance}</a>'
            links+='</nav>'
            body=panel.replace('{{THEME}}',key).replace('{{MODE}}',mode).replace('{{PANEL_LINKS}}',links)
            html=document(body,'Tide · Panel extension / '+theme['name']+' / '+mode,key,mode,'../').replace('</head>','<link rel="stylesheet" href="panel.css">\n</head>')
            result[ROOT/'extensions'/f'{key}-{mode}.html']=html
            if key=='summer' and mode=='light':result[ROOT/'extensions/index.html']=html
    return result


def build(check=False):
    import os
    themes,resolved,audit=load_themes(ROOT/'tokens/themes.json')
    rendered=outputs(themes,resolved,audit)
    files={}
    for path,content in rendered.items():
        target=OUT/path.relative_to(ROOT)
        if path.suffix=='.html':
            # All documentation pages consume the one built kit.
            content=re.sub(r'((?:href|src)=")((?:\.\./)*)(css/tide\.css|assets/[^"<>]+)(")',lambda m:m[1]+os.path.relpath(PROJECT/'build/tide'/m[3],target.parent).replace('\\','/')+m[4],content)
        files[target]=content.encode('utf-8')
    files[OUT/'css/docs.css']=(SITE/'css/docs.css').read_bytes()
    files[OUT/'extensions/panel.css']=(ROOT/'extensions/panel.css').read_bytes()
    for p in (ROOT/'docs').glob('*.md'):files[OUT/'docs'/p.name]=p.read_bytes()
    files[OUT/'README.md']=(ROOT/'README.md').read_bytes()
    files[OUT/'tokens/resolved.json']=(PROJECT/'build/tide/tokens/resolved.json').read_bytes()
    files[OUT/'screen-map.json']=(SITE/'screen-map.json').read_bytes()
    for path,content in files.items():
        if check:assert path.is_file() and path.read_bytes()==content,'Stale documentation output: '+str(path.relative_to(PROJECT))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
    print('Reference site: all six theme/mode libraries and screen specimens '+('verified.' if check else 'built.'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');build(parser.parse_args().check)
