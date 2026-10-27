"""Close the ownership skip path and the remaining type/inset regressions."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

from contracts import ContractScan,registry_entries,registry_issues,style_ownership_issues
from compiler import load_themes
from test_buttons import rules

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]


class KitCloseoutContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))
        spec=importlib.util.spec_from_file_location('closeout_site',PROJECT/'site/tools/build.py')
        cls.site=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.site)
        cls.rendered=cls.site.outputs(*load_themes(ROOT/'tokens/themes.json'))

    def test_every_public_block_requires_complete_ownership(self):
        self.assertEqual(registry_issues(self.manifest,ROOT),[])
        self.assertEqual(len(registry_entries(self.manifest)),65)
        for group in ['components','supportingBlocks']:
            for index,entry in enumerate(self.manifest[group]):
                for key in ['source','htmlSource','fixture','contract','behavior','styleOwnership']:
                    mutated=copy.deepcopy(self.manifest);del mutated[group][index][key]
                    self.assertIn(entry['block']+': missing '+key,registry_issues(mutated,ROOT))

    def test_composition_owners_duplicates_and_invalid_homes_are_rejected(self):
        for block in self.manifest['compositions']:
            m=copy.deepcopy(self.manifest);del m['compositionContracts'][block]
            self.assertIn('Missing composition contract: '+block,registry_issues(m,ROOT))
        m=copy.deepcopy(self.manifest);m['supportingBlocks'].append(m['components'][0])
        self.assertIn('Duplicate registry owner: tide-button',registry_issues(m,ROOT))
        for path in ['missing.css','../../README.md','docs/FORMS.md']:
            m=copy.deepcopy(self.manifest);m['components'][0]['source']=path
            self.assertIn('tide-button: invalid source home',registry_issues(m,ROOT))
        m=copy.deepcopy(self.manifest);m['components'][0]['fixture']='../index.html'
        self.assertIn('tide-button: invalid fixture',registry_issues(m,ROOT))

    def test_no_public_block_silently_allows_consumer_type_overrides(self):
        for e in registry_entries(self.manifest):
            b=e['block'];css='.'+b+' { font-size: 9px; }'
            self.assertIn('Kit-owned selectors redefined in app CSS: '+b,style_ownership_issues(css,self.manifest))
        app='\n'.join(p.read_text(encoding='utf-8') for p in (PROJECT/'examples/events/src/styles').glob('*.css'))
        self.assertEqual(style_ownership_issues(app,self.manifest),[])

    def test_exceptions_cannot_conceal_grouped_or_extra_declarations(self):
        allowed='.host .tide-event-hero__toolbar, .host-print { display: none; }'
        self.assertEqual(style_ownership_issues(allowed,self.manifest),[])
        for css in [
            '.tide-event-hero__toolbar, .tide-event-hero__title { display: none; }',
            '.host .tide-event-hero__content { padding-block-start: 1px; }',
            '.host .tide-event-hero__toolbar { display: none; font-size: 9px; }',
            '.host :is(.tide-event-hero__toolbar, .tide-event-hero__title) { display: none; }',
        ]:
            self.assertIn('Kit-owned selectors redefined in app CSS: tide-event-hero',style_ownership_issues(css,self.manifest))
        self.assertEqual(style_ownership_issues('.host p:not(.tide-eyebrow) { font-size: 12px; }',self.manifest),[])

    def test_optical_values_are_named_and_viewports_do_not_change_type_density(self):
        css=(ROOT/'css/components.css').read_text(encoding='utf-8')
        for literal in ['font-size: 1.1875rem','font-size: 1.375rem','line-height: 1.2','letter-spacing: .22em','letter-spacing: -.01em']:
            self.assertNotIn(literal,css)
        for selector,declarations,context in rules(css):
            if '.tide-event-hero' in selector and any('width' in item for item in context):
                self.assertFalse(any(k in declarations for k in ['font-size','line-height','column-gap','padding']))
        title=next(d for s,d,c in rules(css) if '.tide-event-details__title' in s)
        self.assertEqual(title['line-height'],'var(--tide-leading-page)')
        self.assertIn('.tide-partner__title, .tide-partner h3',css)
        self.assertIn('.tide-fallback__title, .tide-fallback h2',css)
        self.assertNotIn('.tide-event-details p {',css)
        layout=(ROOT/'css/layout.css').read_text(encoding='utf-8')
        self.assertNotIn('.tide-page-body h2 {',layout)
        self.assertIn('.tide-page-body :where(h2:not([class]))',layout)

    def test_nested_venue_padding_is_explicit_and_default_is_preserved(self):
        css=(ROOT/'css/page-patterns.css').read_text(encoding='utf-8')
        profiles={s:d for s,d,c in rules(css) if s in ['.tide-venue-profile','.tide-venue-profile--flush-inline']}
        self.assertEqual(profiles['.tide-venue-profile']['padding'],'var(--tide-space-6)')
        self.assertEqual(profiles['.tide-venue-profile--flush-inline'],{'padding-inline':'0'})
        for recipe in ['venue.html','venue-empty.html']:
            self.assertIn('tide-venue-profile tide-venue-profile--flush-inline',(ROOT/'templates/frames'/recipe).read_text(encoding='utf-8'))

    def test_all_modes_have_real_native_context_and_hidden_fixtures(self):
        frames={p:html for p,html in self.rendered.items() if p.name=='kit-closeout.html'}
        self.assertEqual(len(frames),10)
        for path,html in frames.items():
            scan=ContractScan();scan.feed(html)
            self.assertEqual(len([n for n in scan.nodes if n['attrs'].get('data-closeout')]),30)
            ids=[n['attrs']['id'] for n in scan.nodes if 'id' in n['attrs']]
            self.assertEqual(len(ids),len(set(ids)))
            self.assertEqual(len([n for n in scan.nodes if n['tag']=='h1']),1)
            self.assertIn('href="../../extensions/panel.css"',html)
            self.assertIn('class="tide-doc-closeout tide-stack"',html)
            self.assertIn('<div hidden>',html)
            self.assertNotIn('{{',html)
            self.assertNotIn('<script',html)
            for node in scan.nodes:
                href=node['attrs'].get('href','')
                if href.startswith('#'):self.assertIn(href[1:],ids)

    def test_every_registered_fixture_actually_contains_its_block(self):
        for entry in registry_entries(self.manifest):
            fixture=entry['fixture']
            path=ROOT/'index.html' if fixture=='library' else ROOT/fixture if fixture.startswith('extensions/') else ROOT/'tide-dark/frames'/fixture
            self.assertIn(entry['block'],self.rendered[path],entry['block'])


if __name__=='__main__':unittest.main()
