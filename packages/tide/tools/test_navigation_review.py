"""The opt-in navigation recipe reuses action geometry and keeps defaults intact."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

from compiler import load_themes
from contracts import ContractScan
from palette import contrast
from test_buttons import rules

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]


class NavigationReviewContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('navigation_review_site',PROJECT/'site/tools/build.py')
        cls.site=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.site)
        cls.rendered=cls.site.outputs(*load_themes(ROOT/'tokens/themes.json'))
        cls.proposal=(PROJECT/'site/css/navigation-review.css').read_text(encoding='utf-8')
        cls.navigation=(ROOT/'extensions/navigation.css').read_text(encoding='utf-8')

    def test_proposal_styles_are_loaded_only_by_ten_review_documents(self):
        pages=[p for p,html in self.rendered.items() if 'href="../../css/navigation-review.css"' in html]
        self.assertEqual(len(pages),10)
        self.assertTrue(all(p.name=='navigation-review.html' for p in pages))
        for source in (ROOT/'css').glob('*.css'):
            self.assertNotIn('tide-doc-navigation',source.read_text(encoding='utf-8'))
        for source in (PROJECT/'application-kits/lineup/src').rglob('*'):
            if source.suffix in ('.css','.html'):
                self.assertNotIn('tide-doc-navigation',source.read_text(encoding='utf-8'))

    def test_navigation_reuses_compact_actions_and_keeps_native_semantics(self):
        for path,html in self.rendered.items():
            if path.name!='navigation-review.html':continue
            scan=ContractScan();scan.feed(html)
            nodes={n['attrs']['id']:n for n in scan.nodes if 'id' in n['attrs']}
            self.assertEqual(len([n for n in scan.nodes if n['tag']=='h1']),1)
            for key in ['after-current','after-other','lab-nav-rest','lab-nav-current']:
                node=nodes[key]
                self.assertEqual(node['tag'],'a')
                self.assertTrue({'tide-button','tide-button--quiet','tide-button--compact'} <= set(node['attrs']['class'].split()))
                self.assertIn('href',node['attrs'])
                self.assertNotIn('aria-pressed',node['attrs'])
            self.assertEqual(nodes['after-current']['attrs']['aria-current'],'page')
            self.assertIn('tide-button--secondary',nodes['after-saved']['attrs']['class'])
            self.assertNotIn('href',nodes['lab-nav-disabled']['attrs'])
            self.assertEqual(nodes['lab-nav-disabled']['attrs']['aria-disabled'],'true')
            self.assertEqual(nodes['relative-selected']['attrs']['aria-pressed'],'true')

    def test_proposed_current_state_does_not_override_geometry_or_focus(self):
        permitted={'box-shadow','border-color'}
        for selector,decl,context in rules(self.navigation):
            if not re.search(r'\.tide-button--navigation(?![\w-])',selector):continue
            self.assertTrue(all(k.startswith('--tide-action-') or k in permitted for k in decl),selector)
        self.assertNotIn(':focus',self.navigation)
        self.assertNotIn('aria-pressed',self.navigation)
        self.assertNotIn('data-review-state',self.navigation)
        self.assertIn("[href]:not([aria-disabled='true'])",self.navigation)
        self.assertIn('@layer tide.components {',self.navigation)
        self.assertNotIn('tide-button--navigation',self.proposal)

    def test_selected_colors_and_source_icon_stay_in_the_existing_system(self):
        _,themes,_=load_themes(ROOT/'tokens/themes.json')
        for modes in themes.values():
            for roles in modes.values():
                self.assertGreaterEqual(contrast(roles['selected-text'],roles['selected-surface']),4.5)
        self.assertIn('var(--tide-color-selected-surface)',self.navigation)
        self.assertIn('var(--tide-color-selected-text)',self.navigation)
        self.assertIn("assets/icons/BookmarkIcon.svg",(PROJECT/'site/tools/build.py').read_text(encoding='utf-8'))
        manifest=json.loads((PROJECT/'site/component-manifest.json').read_text(encoding='utf-8'))
        self.assertIn('css/navigation-review.css',manifest['reviewStyles'])
        self.assertIn('tide-doc-navigation',manifest['privateBlocks'])

    def test_navigation_variants_have_canonical_owners_and_remain_opt_in(self):
        manifest=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))
        for block,variant in [('tide-button','navigation'),('tide-site-header','centered')]:
            entry=next(e for e in manifest['components'] if e['block']==block)
            self.assertIn(variant,entry['variants'])
            self.assertIn('extensions/navigation.css',entry['supportingSources'])
        for p,html in self.rendered.items():
            if p.name=='navigation-review.html':
                self.assertIn('href="../../extensions/navigation.css"',html)
                self.assertIn('tide-site-header__leading',html)
                self.assertIn('tide-site-header__primary',html)
                self.assertIn('tide-site-header__utility',html)
        for source in (ROOT/'css').glob('*.css'):
            self.assertNotIn('tide-site-header--centered',source.read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
