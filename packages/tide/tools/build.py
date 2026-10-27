"""Build the Tide CSS distribution; no archived inputs or site dependency."""
from pathlib import Path
import argparse
import json
import re
import sys
from compiler import load_themes, theme_styles

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
OUT=PROJECT/'build/tide'

def strip_css_comments(source):
    """Omit source commentary without rewriting CSS tokens, strings or URLs.

    Keep license/preserve comments. Readable canonical modules remain unchanged.
    This is deliberately not a CSS minifier.
    """
    tokens=re.compile(r'''\burl\((?:'(?:\\[\s\S]|[^'\\])*'|"(?:\\[\s\S]|[^"\\])*"|\\[\s\S]|[^'"\\)])*\)|'(?:\\[\s\S]|[^'\\])*'|"(?:\\[\s\S]|[^"\\])*"|/\*[\s\S]*?\*/''',re.I)
    def keep(match):
        value=match.group()
        return ' ' if value.startswith('/*') and not re.search(r'^/\*!|@license|@preserve',value,re.I) else value
    return tokens.sub(keep,source)

def outputs():
    _,resolved,audit=load_themes(ROOT/'tokens/themes.json')
    themes=theme_styles(resolved)
    modules=['reset','tokens','themes','base','layout','components','utilities']
    version=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))['version']
    bundle=[f'/* Generated Tide {version} entry point. Edit the named source modules, then build. */','@layer '+', '.join('tide.'+name for name in modules)+';']
    for name in modules:
        content=themes if name=='themes' else (ROOT/'css'/f'{name}.css').read_text(encoding='utf-8')
        if name=='components':content+='\n@layer extensions {\n'+(ROOT/'css/patterns.css').read_text(encoding='utf-8')+'\n'+(ROOT/'css/content.css').read_text(encoding='utf-8')+'\n'+(ROOT/'css/filter-panel.css').read_text(encoding='utf-8')+'\n'+(ROOT/'css/page-patterns.css').read_text(encoding='utf-8')+'\n}\n'
        bundle.append('@layer tide.'+name+' {\n'+strip_css_comments(content)+'\n}')
    files={OUT/'css/tide.css':('\n\n'.join(bundle)+'\n').encode(),OUT/'css/themes.css':themes.encode(),OUT/'tokens/resolved.json':(json.dumps(resolved,indent=2)+'\n').encode(),OUT/'tokens/primitives.json':(json.dumps(dict(re.findall(r'(--tide-[\w-]+):\s*([^;]+);',(ROOT/'css/tokens.css').read_text(encoding='utf-8'))),indent=2)+'\n').encode(),PROJECT/'build/reports/contrast.json':(json.dumps({'standard':'WCAG 2 relative luminance, sRGB','themes':audit},indent=2)+'\n').encode()}
    for folder in ('assets','licenses'):
        for p in (ROOT/folder).rglob('*'):
            if p.is_file():files[OUT/folder/p.relative_to(ROOT/folder)]=p.read_bytes()
    files[OUT/'component-manifest.json']=(ROOT/'component-manifest.json').read_bytes()
    return files

def build(check=False):
    files=outputs()
    for path,content in files.items():
        if check:assert path.is_file() and path.read_bytes()==content,'Stale kit output: '+str(path.relative_to(PROJECT))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
    print('Tide: paired themes, contrast gates and CSS distribution '+('verified.' if check else 'built.'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');build(parser.parse_args().check)
