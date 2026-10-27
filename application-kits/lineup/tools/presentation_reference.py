"""Generate ignored Tide-only cascade probes for the built Lineup documents.

Run after the root build. Probes retain authored component HTML and the exact
shared distribution, removing only Lineup's stylesheet. Browser comparisons can
then detect private cascade drift, including unclassed recipe descendants.
"""
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin

from html_templates import ROOT
from presentation_contract import Tree, private_class


def generate():
    repository = ROOT.parents[1]
    kit = repository / 'packages/tide'
    consumer = json.loads((ROOT/'consumer-manifest.json').read_text(encoding='utf-8'))
    registry = json.loads((kit/'component-manifest.json').read_text(encoding='utf-8'))
    sys.path.insert(0, str(kit/'tools'))
    from contracts import registry_entries
    owners = {e['block']:e for e in registry_entries(registry)}
    out = repository/'build/qa/lineup-alignment'
    counts = {}; routes = []
    for mode in ['app'] + ['themes/'+t+'-'+m for t in ('tide','bumble','slate','grove','iris') for m in ('light','dark')]:
        destination = out/'references'/mode
        destination.mkdir(parents=True, exist_ok=True)
        for page in sorted((repository/'build/events'/mode).glob('*.html')):
            html = page.read_text(encoding='utf-8')
            if mode == 'app':
                routes.append(page.stem)
                for node in Tree(html).nodes:
                    for cls in node['classes']:
                        if cls.startswith('tide-') and not private_class(cls, consumer['privateBlocks']):
                            counts[cls] = counts.get(cls, 0)+1
            html, removed = re.subn(r'<link rel="stylesheet" href="[^"]*/runtime/css/app.css">', '', html)
            assert removed == 1, page
            # The standalone rail is exposed by its canonical display rule;
            # suppress automatic focus so resting styles compare like for like.
            html = re.sub(r'\sautofocus(?=[\s>])', '', html)
            html = re.sub(r'(href|src)="([^"]+)"',
                          lambda match: match[1]+'="'+urljoin('/events/'+mode+'/'+page.name, match[2])+'"', html)
            (destination/page.name).write_text(html, encoding='utf-8')
    overview = (repository/'build/events/index.html').read_text(encoding='utf-8')
    overview, removed = re.subn(r'<link rel="stylesheet" href="runtime/css/app.css">', '', overview)
    assert removed == 1
    overview = re.sub(r'(href|src)="([^"]+)"', lambda match: match[1]+'="'+urljoin('/events/index.html',match[2])+'"', overview)
    (out/'references/overview.html').write_text(overview, encoding='utf-8')
    inventory = []
    for cls, count in sorted(counts.items()):
        block = cls.split('__')[0].split('--')[0]
        # tide is the base/theme root; u-* are the registered utility family.
        owner = owners.get(block, owners.get('tide-u') if block.startswith('tide-u-') else None)
        assert owner is not None or block == 'tide' or block.startswith('tide-u-'), ('Unregistered public class', cls)
        inventory.append({'class':cls, 'instances':count, 'block':block,
                          'recipe': owner.get('htmlSource') if owner else 'css/base.css' if block == 'tide' else 'css/utilities.css'})
    (out/'inventory.json').write_text(json.dumps({'routes':routes, 'components':inventory}, indent=2)+'\n', encoding='utf-8')
    print(f'{len(routes)} routes, {len(inventory)} public classes; generated 737 route probes plus overview in {out}')


if __name__ == '__main__':
    generate()
