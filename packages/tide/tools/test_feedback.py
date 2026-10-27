"""Guards for feedback type drift, neutral boundaries and native/static semantics."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

from contracts import ContractScan,style_ownership_issues
from test_buttons import rules

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
BLOCKS={'tide-badge','tide-notice','tide-toast','tide-empty'}


def drift_issues(css):
    protected={'font','font-family','font-size','font-style','font-weight','line-height','letter-spacing','text-transform',
               'padding','padding-inline','padding-inline-start','padding-block','gap','row-gap','column-gap',
               'border','border-width','border-inline-start','border-left','min-block-size'}
    issues=[]
    for selector,decl,context in rules(css):
        if not any('.'+b in selector for b in BLOCKS):continue
        status=bool(re.search(r'\.tide-badge--(?:success|warning|danger)',selector))
        transient=bool(re.search(r':(?:hover|active|focus|disabled)|\[aria-disabled',selector))
        if '.tide-badge' in selector and transient:issues.append((selector,'interactive badge'))
        foreign=bool(re.search(r'\.\w[\w-]*\s+\.tide-(?:badge|notice|toast|empty)(?![\w-])',selector))
        for prop in protected&decl.keys():
            if status or transient or foreign or context:issues.append((selector,prop))
        if selector=='.tide-notice' and ('padding-inline-start' in decl or 'border-left' in decl):issues.append((selector,'asymmetric notice'))
    return issues


class FeedbackContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css=(ROOT/'css/components.css').read_text(encoding='utf-8')
        cls.html=(ROOT/'templates/feedback.html').read_text(encoding='utf-8')
        cls.scan=ContractScan();cls.scan.feed(cls.html);cls.nodes=cls.scan.nodes

    def test_geometry_guards_catch_status_context_and_transient_drift(self):
        for regression in ['.tide-badge--danger { padding: 1rem; }',
                           '.tide-badge:hover { color: red; }',
                           '.reading .tide-notice { font-size: 20px; }',
                           '.tide-toast__action:hover { line-height: 18px; }',
                           '.tide-notice { padding-inline-start: 18px; }',
                           '@media (width < 400px) { .tide-empty { padding: 8px; } }']:
            self.assertTrue(drift_issues(regression),regression)
        self.assertEqual(drift_issues(self.css),[])

    def test_blocks_have_explicit_type_and_notice_has_uniform_padding(self):
        parsed=list(rules(self.css))
        for block in BLOCKS:
            decl={k:v for s,d,c in parsed if not c and '.'+block in [x.strip() for x in s.split(',')] for k,v in d.items()}
            for prop in ['font-family','font-style','font-size','font-weight','line-height','letter-spacing','text-transform']:
                self.assertIn(prop,decl,block)
            self.assertEqual(decl['font-family'],'var(--tide-font-family)')
            self.assertEqual(decl['font-style'],'normal')
            self.assertEqual(decl['text-transform'],'none')
        notice=next(d for s,d,c in parsed if s=='.tide-notice')
        self.assertEqual(notice['padding'],'var(--tide-space-4)')
        self.assertEqual(notice['border'],'var(--tide-border-width) solid var(--tide-color-border-strong)')
        for s,d,c in parsed:
            if s.startswith('.tide-badge--'):self.assertTrue(set(d)<={'background','color','border-color'},s)

    def test_empty_density_is_explicit_and_title_is_heading_independent(self):
        parsed=list(rules(self.css))
        self.assertTrue(any('.tide-empty__title' in s and '.tide-empty h2' in s for s,d,c in parsed))
        self.assertTrue(any(s=='.tide-empty--compact' and d.get('padding')=='var(--tide-space-6) var(--tide-space-4)' for s,d,c in parsed))
        self.assertNotRegex(self.css,r'\.tide-empty[^{}]*\{[^{}]*margin-block-start')
        empty=[n for n in self.nodes if 'tide-empty' in n['attrs'].get('class','').split() and 'hidden' not in n['attrs']]
        self.assertTrue(all('aria-labelledby' in n['attrs'] for n in empty))

    def test_status_is_static_and_errors_are_not_blanket_live_regions(self):
        for n in self.nodes:
            a=n['attrs'];classes=a.get('class','').split()
            if 'tide-badge' in classes:
                self.assertEqual(n['tag'],'span');self.assertNotIn('role',a);self.assertNotIn('tabindex',a);self.assertTrue(n['text'].strip())
            self.assertNotIn(a.get('role'),{'status','alert','button'})
        self.assertFalse(any(n['tag'] in {'script','button'} for n in self.nodes))
        self.assertNotRegex(self.html,r'onclick|aria-pressed|aria-live')

    def test_actions_and_hidden_states_use_native_semantics(self):
        ids={n['attrs']['id'] for n in self.nodes if 'id' in n['attrs']}
        hidden=[n for n in self.nodes if 'hidden' in n['attrs']]
        self.assertEqual(len(hidden),4)
        for n in self.nodes:
            a=n['attrs']
            if n['tag']=='a':
                self.assertTrue(n['text'].strip())
                if a.get('aria-disabled')=='true':self.assertNotIn('href',a)
                else:self.assertIn('href',a)
                if a.get('href','').startswith('#'):self.assertIn(a['href'][1:],ids)
        self.assertIn('display: none !important',(ROOT/'css/reset.css').read_text(encoding='utf-8'))

    def test_link_feedback_excludes_composed_button_anchors(self):
        parsed=list(rules(self.css))
        for s,d,c in parsed:
            if '.tide-toast > a' in s:
                self.assertIn(':not(.tide-button)',s)
        self.assertTrue(any(':hover' in s and d.get('color')=='var(--tide-color-accent-hover)' for s,d,c in parsed if 'tide-toast__action' in s))
        self.assertTrue(any(':active' in s and d.get('text-decoration-style')=='double' for s,d,c in parsed if 'tide-toast__action' in s))

    def test_ownership_and_state_sources_are_registered(self):
        manifest=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))
        for entry in manifest['components']:
            if entry['block'] in BLOCKS:
                self.assertEqual(entry['htmlSource'],'templates/feedback.html')
                self.assertEqual(entry['fixture'],'feedback-states.html')
                self.assertEqual(entry['styleOwnership'],'kit')
                self.assertTrue((ROOT/entry['contract']).is_file())
                self.assertTrue(style_ownership_issues('.'+entry['block']+' { padding: 3px; }',manifest))

    def test_all_theme_libraries_and_frames_share_the_canonical_matrix(self):
        spec=importlib.util.spec_from_file_location('feedback_site_build',PROJECT/'site/tools/build.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        from compiler import load_themes
        rendered=module.outputs(*load_themes(ROOT/'tokens/themes.json'))
        frames=[h for p,h in rendered.items() if p.name=='feedback-states.html']
        library_items=[(p,h) for p,h in rendered.items() if p.name=='index.html' and 'id="components"' in h]
        libraries=[h for p,h in library_items]
        self.assertEqual(len(frames),10);self.assertEqual(len(libraries),11)
        for html in frames+libraries:
            self.assertIn('id="feedback-toast-link"',html)
            self.assertNotIn('{{FEEDBACK_',html)
        for html in frames:self.assertIn('data-feedback-case="context-empty"',html)
        cases=module.feedback_cases(module.feedback(3),['badge-neutral','badge-success','badge-warning','badge-danger','notice-info','toast-action','empty-matches'])
        with self.assertRaisesRegex(ValueError,'Missing'):module.feedback_cases(module.feedback(3),['missing'])
        with self.assertRaisesRegex(ValueError,'Duplicate'):module.feedback_cases(cases['badge-neutral']*2,['badge-neutral'])
        for path,html in library_items:
            self.assertNotIn('data-feedback-case="context-empty"',html)
            prefix='tide-dark/frames/' if path==ROOT/'index.html' else 'frames/'
            for name,snippet in cases.items():
                self.assertTrue(snippet.replace('{{FRAMES}}',prefix) in html,'Canonical preview changed: '+path.name+' '+name)


if __name__=='__main__':unittest.main()
