"""Listing drift, native markup and the kit/consumer presentation boundary."""
from datetime import date,datetime
import importlib.util
import json
from pathlib import Path
import re
import unittest

from contracts import ContractScan,style_ownership_issues,VOID
from listing_specimens import listings,card,date_block
from test_buttons import rules

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
BLOCKS={'tide-event-card','tide-date','tide-event-group','tide-results'}


class Tree(ContractScan):
    def handle_starttag(self,tag,attrs):
        ancestors=tuple(self.stack);super().handle_starttag(tag,attrs);self.nodes[-1]['ancestors']=ancestors


def drift_issues(css):
    protected={'font','font-family','font-size','font-style','font-weight','line-height','letter-spacing','text-transform',
               'padding','padding-block','padding-inline','gap','column-gap','row-gap','margin-block-start','min-inline-size','min-block-size'}
    issues=[]
    for selector,decl,context in rules(css):
        if not any('.'+b in selector for b in BLOCKS):continue
        state=bool(re.search(r':(?:hover|active|focus)|--in-view',selector))
        foreign=bool(re.search(r'\.[\w-]+\s+\.tide-(?:event-card|date|event-group|results)(?![\w-])',selector))
        if state or foreign or context:issues.extend((selector,p) for p in protected&decl.keys())
    return issues


class ListingContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=listings(2);cls.tree=Tree();cls.tree.feed(cls.html);cls.nodes=cls.tree.nodes
        cls.manifest=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))

    def test_state_context_and_breakpoint_geometry_guards(self):
        for css in ['.tide-event-card--in-view { padding: 8px; }','.reading .tide-date { font-size: 24px; }',
                    '.tide-event-card:has(a:hover) .tide-event-card__title { line-height: 40px; }',
                    '@media (width < 350px) { .tide-event-card__meta { column-gap: 12px; } }']:
            self.assertTrue(drift_issues(css),css)
        for source in (ROOT/'css').glob('*.css'):
            self.assertEqual(drift_issues(source.read_text(encoding='utf-8')),[],source.name)

    def test_each_root_owns_all_type_properties(self):
        parsed=list(rules((ROOT/'css/components.css').read_text(encoding='utf-8')))
        for block in BLOCKS:
            decl={k:v for s,d,c in parsed if not c and '.'+block in [x.strip() for x in s.split(',')] for k,v in d.items()}
            for prop in ['font-family','font-style','font-size','line-height','font-weight','letter-spacing','text-transform']:
                self.assertIn(prop,decl,block)
            self.assertEqual(decl['font-family'],'var(--tide-font-family)')
            self.assertEqual(decl['font-style'],'normal')
            self.assertEqual(decl['text-transform'],'none')

    def test_dates_have_valid_full_labels_and_decorative_fragments(self):
        dates=[n for n in self.nodes if 'tide-date' in n['attrs'].get('class','').split()]
        self.assertGreaterEqual(len(dates),20)
        for n in dates:
            self.assertEqual(n['tag'],'time');d=date.fromisoformat(n['attrs']['datetime'])
            self.assertIn(str(d.year),n['attrs']['aria-label'])
            self.assertTrue(all(c['attrs'].get('aria-hidden')=='true' for c in self.nodes
                                if n in c['ancestors'] and any(x in c['attrs'].get('class','').split() for x in ['tide-date__day','tide-date__parts'])))
        self.assertIn('Friday, January 1, 2027',date_block('boundary','2027-01-01'))
        for n in self.nodes:
            if n['tag']=='time':datetime.fromisoformat(n['attrs']['datetime'])
        unknown=card('unknown-test',4,iso=None,start=None)
        self.assertNotIn('<time',unknown);self.assertIn('Date to be confirmed',unknown)
        self.assertIn('var(--tide-date-day-min)',(ROOT/'css/components.css').read_text(encoding='utf-8'))

    def test_card_links_labels_and_independent_actions_are_native(self):
        ids=[n['attrs']['id'] for n in self.nodes if 'id' in n['attrs']]
        self.assertEqual(len(ids),len(set(ids)))
        for n in self.nodes:
            a=n['attrs']
            if 'aria-labelledby' in a:self.assertTrue(all(ref in ids for ref in a['aria-labelledby'].split()))
            if n['tag']=='a':
                self.assertFalse(any(p['tag'] in {'a','button'} for p in n['ancestors']))
                self.assertTrue(a.get('aria-label') or n['text'].strip())
                if a.get('href','').startswith('#'):self.assertIn(a['href'][1:],ids)
            self.assertNotIn(a.get('role'),{'button','tab','status','alert'})
            self.assertNotIn('aria-selected',a)
        unavailable=card('unavailable-test',4,available=False)
        self.assertNotIn('tide-event-card__link',unavailable)
        layered=card('action-test',4,action=True,status='')
        self.assertIn('href="#listing-saved-target"',layered)
        self.assertIn('href="#listing-detail-target"',layered)

    def test_group_counts_and_navigation_match_visible_authored_cards(self):
        for group in [n for n in self.nodes if 'tide-event-group' in n['attrs'].get('class','').split()]:
            cards=[n for n in self.nodes if n['tag']=='article' and n['ancestors'][-1] is group and 'hidden' not in n['attrs']]
            count=next(n for n in self.nodes if group in n['ancestors'] and 'tide-event-group__count' in n['attrs'].get('class','').split())
            self.assertEqual(count['text'].strip(),f'{len(cards)} event'+('' if len(cards)==1 else 's'))
        self.assertNotIn('href="#listing-hidden-month"',self.html)
        self.assertIn('.tide-event-card:not([hidden]) ~ .tide-event-card:not([hidden])',(ROOT/'css/components.css').read_text(encoding='utf-8'))
        css=(ROOT/'css/components.css').read_text(encoding='utf-8')
        self.assertTrue(any(s=='.tide-event-card__separator' and d.get('display')=='none' for s,d,c in rules(css)))
        self.assertNotIn('tide-event-card__separator',(ROOT/'templates/listing-card.html').read_text(encoding='utf-8'))

    def test_ownership_allows_only_documented_preview_presentation(self):
        for allowed in ['.host .tide-event-card__status { display: none; }',
                        '.host .tide-event-card__status { display: inline-flex; }',
                        '.host .tide-event-card--in-view { outline: none; }']:
            self.assertEqual(style_ownership_issues(allowed,self.manifest),[])
        for forbidden in ['.host .tide-event-card__status { display: none; padding: 8px; }',
                          '.host .tide-event-card__title { font-size: 12px; }',
                          '.tide-event-card { padding: 8px; }',
                          '.host .tide-event-card--in-view { outline: 8px solid red; }']:
            self.assertIn('Kit-owned selectors redefined in app CSS: tide-event-card',style_ownership_issues(forbidden,self.manifest))
        app='\n'.join(p.read_text(encoding='utf-8') for p in (PROJECT/'examples/events/src/styles').glob('*.css'))
        self.assertEqual(style_ownership_issues(app,self.manifest),[])

    def test_registered_css_html_contracts_exist(self):
        entries=[e for e in self.manifest['components'] if e['block'] in BLOCKS]
        entries.append(self.manifest['compositionContracts']['tide-results'])
        for e in entries:
            self.assertEqual(e['styleOwnership'],'kit');self.assertEqual(e['fixture'],'listing-states.html')
            for path in [e['source'],e['htmlSource'],e['contract'],*e.get('supportingSources',[])]:self.assertTrue((ROOT/path).is_file(),path)

    def test_authored_values_escape_and_invalid_recipes_fail(self):
        html=card('escape-test',4,title='<em>Title</em>',venue='A & B',price='"Free"')
        self.assertIn('&lt;em&gt;Title&lt;/em&gt;',html);self.assertIn('A &amp; B',html)
        with self.assertRaises(ValueError):card('bad"key',4)
        with self.assertRaises(ValueError):date_block('invalid','2026-02-31')
        self.assertNotIn('<script',self.html)
        self.assertNotIn('aria-live',self.html)

    def test_all_theme_frames_and_library_links_are_current(self):
        spec=importlib.util.spec_from_file_location('listing_site_build',PROJECT/'site/tools/build.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        from compiler import load_themes
        rendered=module.outputs(*load_themes(ROOT/'tokens/themes.json'))
        frames=[h for p,h in rendered.items() if p.name=='listing-states.html']
        libraries=[h for p,h in rendered.items() if p.name=='index.html' and 'id="components"' in h]
        self.assertEqual(len(frames),10);self.assertEqual(len(libraries),11)
        for html in frames:
            self.assertIn('id="listing-action-action"',html);self.assertNotIn('{{LISTING_',html)
        for html in libraries:self.assertIn('listing-states.html',html)


if __name__=='__main__':unittest.main()
