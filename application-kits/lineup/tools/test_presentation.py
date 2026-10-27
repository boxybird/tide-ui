"""Guard consumer typography even when a private alias targets a kit element."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unittest

from html_templates import AppTemplates, ROOT

KIT = ROOT.parents[1] / 'packages/tide'
sys.path.insert(0, str(KIT / 'tools'))
from contracts import style_ownership_issues

TYPE = {'font', 'font-family', 'font-size', 'font-style', 'font-weight',
        'line-height', 'letter-spacing', 'text-transform'}


class Classes(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.nodes = []; self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.nodes.append(set(dict(attrs).get('class', '').split()))


def typed_rules(css):
    """Read type declarations through the app's ordinary grouping at-rules."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    cursor = 0
    while (start := css.find('{', cursor)) >= 0:
        selector = css[cursor:start].strip()
        depth, end = 1, start + 1
        while depth and end < len(css):
            depth += (css[end] == '{') - (css[end] == '}'); end += 1
        body = css[start + 1:end - 1]
        if selector.startswith('@'):
            yield from typed_rules(body)
        else:
            declarations = [part.strip() for part in body.split(';') if ':' in part and part.split(':', 1)[0].strip() in TYPE]
            if declarations:
                yield selector, '; '.join(declarations)
        cursor = end


def alias_type_issues(html, css, manifest, private):
    def is_private(name):
        return any(name == block or name.startswith((block + '__', block + '--')) for block in private)
    aliases = {}
    for classes in Classes(html).nodes:
        shared = {name for name in classes if name.startswith('tide-') and not is_private(name)}
        for name in filter(is_private, classes):
            aliases.setdefault(name, set()).update(shared)
    issues = []
    for selector, declarations in typed_rules(css):
        for alias in set(re.findall(r'\.(tide-[\w-]+)', selector)) & aliases.keys():
            for shared in aliases[alias]:
                translated = re.sub(r'\.' + re.escape(alias) + r'(?![\w-])', '.' + shared, selector)
                issues += style_ownership_issues(translated + ' {' + declarations + '}', manifest)
    return sorted(set(issues))


class PresentationContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((KIT / 'component-manifest.json').read_text(encoding='utf-8'))
        cls.consumer = json.loads((ROOT / 'consumer-manifest.json').read_text(encoding='utf-8'))

    def test_private_alias_and_context_cannot_bypass_kit_type_ownership(self):
        for html, css in [
            ('<h2 class="tide-results__count tide-lineup__title">54 events</h2>', '.tide-lineup__title { font-size: 28px; }'),
            ('<h3 class="tide-event-group__title tide-lineup__month-title">October</h3>', '.host .tide-lineup__month-title { font-size: 16px; }'),
            ('<div class="tide-page-intro tide-app__intro"><p>Copy</p></div>', '.tide-app__intro p:not(.tide-eyebrow) { font-size: 12px; }'),
        ]:
            with self.subTest(css=css):
                self.assertTrue(alias_type_issues(html, css, self.manifest, self.consumer['privateBlocks']))

    def test_all_rendered_routes_keep_private_aliases_out_of_kit_type(self):
        html = '\n'.join(AppTemplates().pages().values())
        css = '\n'.join((ROOT / name).read_text(encoding='utf-8') for name in self.consumer['styleHome'])
        self.assertEqual(alias_type_issues(html, css, self.manifest, self.consumer['privateBlocks']), [])


if __name__ == '__main__':
    unittest.main()
