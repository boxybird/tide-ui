"""Guard complete component adoption, plus historical alias regressions."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unittest

from html_templates import AppTemplates, ROOT
from build import review_document
from presentation_contract import Tree, strict_style_issues, primitive_markup_issues

KIT = ROOT.parents[1] / 'packages/tide'
sys.path.insert(0, str(KIT / 'tools'))
from contracts import VOID, style_ownership_issues

TYPE = {'font', 'font-family', 'font-size', 'font-style', 'font-weight',
        'line-height', 'letter-spacing', 'text-transform'}


class Classes(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.nodes = []; self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.nodes.append(set(dict(attrs).get('class', '').split()))


def style_rules(css, properties=None):
    """Read declarations through the app's ordinary grouping at-rules."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    cursor = 0
    while (start := css.find('{', cursor)) >= 0:
        selector = css[cursor:start].strip()
        depth, end = 1, start + 1
        while depth and end < len(css):
            depth += (css[end] == '{') - (css[end] == '}'); end += 1
        body = css[start + 1:end - 1]
        if selector.startswith('@'):
            yield from style_rules(body, properties)
        else:
            declarations = [part.strip() for part in body.split(';') if ':' in part
                            and (properties is None or part.split(':', 1)[0].strip() in properties)]
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
    for selector, declarations in style_rules(css, TYPE):
        for alias in set(re.findall(r'\.(tide-[\w-]+)', selector)) & aliases.keys():
            for shared in aliases[alias]:
                translated = re.sub(r'\.' + re.escape(alias) + r'(?![\w-])', '.' + shared, selector)
                issues += style_ownership_issues(translated + ' {' + declarations + '}', manifest)
    return sorted(set(issues))


class FooterElements(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.nodes = []; self.stack = []; self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        inside = 'tide-filter-panel__footer' in attrs.get('class', '').split() or any(flag for _, flag in self.stack)
        if inside:
            self.nodes.append(attrs)
        if tag not in VOID:
            self.stack.append((tag, inside))

    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def footer_alias_issues(html, css, manifest, private):
    """Check every property on footer/status/count aliases and the Reset hook.

    This focused guard supplements shared direct-selector checks; it is not a
    general selector engine. Private wrappers remain free to compose the slots.
    """
    slots = {'tide-filter-panel__footer', 'tide-filter-panel__status-row', 'tide-filter-panel__count'}
    aliases = {}; has_reset = False
    for attrs in FooterElements(html).nodes:
        classes = set(attrs.get('class', '').split())
        shared = classes & slots
        if 'data-filter-reset' in attrs:
            shared.add('tide-button'); has_reset = True
        for name in classes:
            if any(name == block or name.startswith((block+'__', block+'--')) for block in private):
                aliases.setdefault(name, set()).update(shared)
    issues = []
    for selector, declarations in style_rules(css):
        for alias in set(re.findall(r'\.(tide-[\w-]+)', selector)) & aliases.keys():
            for shared in aliases[alias]:
                translated = re.sub(r'\.'+re.escape(alias)+r'(?![\w-])', '.'+shared, selector)
                issues += style_ownership_issues(translated+' {'+declarations+'}', manifest)
        if has_reset and '[data-filter-reset]' in selector:
            translated = selector.replace('[data-filter-reset]', '.tide-button')
            issues += style_ownership_issues(translated+' {'+declarations+'}', manifest)
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

    def test_filter_footer_aliases_and_reset_hook_cannot_fork_shared_internals(self):
        html = '''<div class="tide-filter-panel__footer tide-app__footer-alias">
          <div class="tide-filter-panel__status-row tide-app__status-alias">
            <button class="tide-button" data-filter-reset>Reset</button>
            <p class="tide-filter-panel__count tide-app__count-alias">54 events</p>
          </div></div>'''
        for css in ('.tide-app__footer-alias { padding: 24px; }',
                    '.host .tide-app__status-alias { display: grid; }',
                    '.tide-app__count-alias { text-align: end; }',
                    '.host [data-filter-reset] { white-space: nowrap; }'):
            with self.subTest(css=css):
                self.assertTrue(footer_alias_issues(html, css, self.manifest, self.consumer['privateBlocks']))
        self.assertEqual(footer_alias_issues(html, '.tide-app__outer-wrapper { padding: 24px; }',
                                           self.manifest, self.consumer['privateBlocks']), [])

    def test_rendered_filter_footers_keep_kit_layout_and_private_wrapper_clearance_separate(self):
        html = '\n'.join(AppTemplates().pages().values())
        css = '\n'.join((ROOT / name).read_text(encoding='utf-8') for name in self.consumer['styleHome'])
        self.assertEqual(footer_alias_issues(html, css, self.manifest, self.consumer['privateBlocks']), [])

    def test_no_private_appearance_or_shared_interior_overrides(self):
        html = '\n'.join(AppTemplates().pages().values()) + review_document('')
        css = '\n'.join((ROOT / name).read_text(encoding='utf-8') for name in self.consumer['styleHome'])
        self.assertEqual(strict_style_issues(html, style_rules(css), self.consumer['privateBlocks']), [])

    def test_strict_boundary_rejects_lookalikes_aliases_context_and_shared_tokens(self):
        html = '<div class="tide-app__host"><div class="tide-field tide-app__alias"><label class="tide-field__label">Search</label></div></div>'
        for css in ('.tide-app__label { font-size: 12px; }',
                    '.tide-app__host { color: red; }',
                    '.tide-app__alias { gap: 0; }',
                    '.tide-app__host label { font-weight: 400; }',
                    '.tide-app__host :focus-visible { outline-offset: -2px; }',
                    ':root { --tide-font-size-body: 12px; }',
                    '.tide-field__label { padding: 0; }'):
            with self.subTest(css=css):
                self.assertTrue(strict_style_issues(html, style_rules(css), self.consumer['privateBlocks']))
        self.assertEqual(strict_style_issues(html, style_rules('.tide-app__host { padding: 24px; }'), self.consumer['privateBlocks']), [])

    def test_every_route_uses_canonical_primitives_and_field_structure(self):
        for route, html in AppTemplates().pages().items():
            with self.subTest(route=route):
                self.assertEqual(primitive_markup_issues(html), [])

    def test_search_label_outside_field_and_private_primitive_are_rejected(self):
        self.assertTrue(primitive_markup_issues('<label class="tide-field__label" for="q">Search</label><div class="tide-field"><input class="tide-field__control" id="q"></div>'))
        self.assertTrue(primitive_markup_issues('<button class="tide-app__button">Go</button><label class="tide-app__label">Search</label><input id="q">'))

    def test_cards_and_filter_footer_follow_current_recipe_structure(self):
        recipe = (KIT / 'templates/listing-card.html').read_text(encoding='utf-8')
        required = set(re.findall(r'\btide-event-card(?:__[\w-]+)?\b', recipe))
        for route, html in AppTemplates().pages().items():
            tree = Tree(html)
            cards = {id(node):set(node['classes']) for node in tree.nodes if 'tide-event-card' in node['classes']}
            for child in tree.nodes:
                for parent in child['parents']:
                    if id(parent) in cards:
                        cards[id(parent)].update(child['classes'])
            for node in tree.nodes:
                if 'tide-event-card' in node['classes']:
                    self.assertLessEqual(required, cards[id(node)], route)
                if 'tide-filter-panel__footer' in node['classes']:
                    self.assertEqual(node['tag'], 'footer', route)
                    self.assertIn('tide-filter-panel', node['parents'][-1]['classes'], route)


if __name__ == '__main__':
    unittest.main()
