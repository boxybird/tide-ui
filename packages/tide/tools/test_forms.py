"""Regression contracts for inherited control type and conflicting form states.

Rendered/native behavior is measured separately. These guards catch the audited
source failures without requiring browser dependencies in the normal check.
"""
import json
from pathlib import Path
import re
import unittest

from contracts import ContractScan, style_ownership_issues
from test_buttons import rules

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
BLOCKS = {'tide-field', 'tide-choice', 'tide-chip', 'tide-upload', 'tide-expandable', 'tide-error-summary'}


def geometry_issues(css):
    """A form state/context must not redefine its component's density or type."""
    protected = {'font', 'font-family', 'font-style', 'font-size', 'font-weight', 'line-height',
                 'letter-spacing', 'text-transform', 'padding', 'padding-inline', 'padding-inline-end', 'padding-block',
                 'min-block-size', 'block-size', 'border', 'border-width', 'border-radius'}
    issues = []
    for selector, declarations, context in rules(css):
        if selector.endswith('::after'):
            continue  # Decorative chevron has its own dimensions.
        if not re.search(r'\.tide-(field__(?:control|label|hint|error)|fieldset__legend|choice|chip|expandable__summary|upload input|error-summary)(?![\w-])', selector):
            continue
        # Native control type selects geometry; interaction state and reading context do not.
        for name in protected & declarations.keys():
            if name=='border' and any('forced-colors' in c for c in context) and declarations[name]=='var(--tide-border-width) solid ButtonText':
                continue  # Preserve the same reserved border with the system color.
            if context or re.search(r':(?:hover|active|disabled|has|where|user-invalid)|\[aria-invalid', selector):
                issues.append((selector, name))
            if re.search(r'\.[\w-]+\s+\.tide-(?:field__(?:control|label|hint|error)|fieldset__legend|choice|chip|expandable__summary|error-summary)', selector):
                issues.append((selector, name))
    return issues


class FormContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = (ROOT/'css/components.css').read_text(encoding='utf-8')
        cls.fragment = (ROOT/'templates/controls.html').read_text(encoding='utf-8')
        cls.scan = ContractScan(); cls.scan.feed(cls.fragment)
        cls.nodes = cls.scan.nodes
        cls.ids = {n['attrs']['id']: n for n in cls.nodes if 'id' in n['attrs']}

    def test_geometry_guards_detect_context_state_and_viewport_regressions(self):
        for css in ['.reading .tide-field__control { font-size: 12px; }',
                    '.reading .tide-field__label { font-weight: 700; }',
                    '.tide-chip:has(input:checked) { padding: 4px; }',
                    '.tide-chip:hover { border: 0; }',
                    '.tide-expandable__summary:hover { border-width: 2px; }',
                    '@media (width < 400px) { .tide-choice { min-block-size: 32px; } }']:
            self.assertTrue(geometry_issues(css), css)
        for source in (ROOT/'css').glob('*.css'):
            self.assertEqual(geometry_issues(source.read_text(encoding='utf-8')), [], source.name)

    def test_every_text_surface_declares_its_type_independently(self):
        parsed=list(rules(self.css+(ROOT/'css/patterns.css').read_text(encoding='utf-8')+(ROOT/'css/page-patterns.css').read_text(encoding='utf-8')))
        for selector in ['.tide-field__control', '.tide-field__label', '.tide-field__hint', '.tide-field__error', '.tide-fieldset__legend', '.tide-choice', '.tide-chip', '.tide-expandable__summary', '.tide-upload input', '.tide-error-summary']:
            declarations={k:v for s,d,c in parsed if not c and selector in [x.strip() for x in s.split(',')] for k,v in d.items()}
            for name in ['font-family','font-style','font-size','font-weight','line-height','letter-spacing','text-transform']:
                self.assertIn(name,declarations,(selector,name))
            self.assertEqual(declarations['font-family'],'var(--tide-font-family)')
            self.assertEqual(declarations['font-style'],'normal')
            self.assertEqual(declarations['text-transform'],'none')

    def test_invalid_and_disabled_rules_have_equal_specificity_and_disabled_is_last(self):
        parsed=[(s,d) for s,d,c in rules(self.css) if not c]
        for block, prop in [('tide-field__control','border-color'),('tide-chip','background'),('tide-choice','color'),('tide-upload','border-style')]:
            invalid=[i for i,(s,d) in enumerate(parsed) if s.startswith('.'+block+':where(') and "[aria-invalid='true']" in s and prop in d]
            disabled=[i for i,(s,d) in enumerate(parsed) if s.startswith('.'+block+':where(') and ':disabled' in s and prop in d]
            self.assertTrue(invalid and disabled,block)
            self.assertGreater(min(disabled),max(invalid),block)
        self.assertNotIn('[disabled]',self.css)  # :disabled also covers inherited fieldset state.
        self.assertNotRegex(self.css,r'(?<![\w-]):invalid\b')
        self.assertIn(':user-invalid',self.css)
        for block in ['tide-chip','tide-choice','tide-upload']:
            self.assertIn('.'+block+':where(:has(input:disabled))',self.css) if block!='tide-chip' else self.assertIn(':has(input:disabled)',self.css)

    def test_labels_descriptions_and_error_links_resolve_to_actual_controls(self):
        ids=[n['attrs']['id'] for n in self.nodes if 'id' in n['attrs']]
        self.assertEqual(len(ids),len(set(ids)))
        for node in self.nodes:
            attrs=node['attrs']
            for ref in attrs.get('aria-describedby','').split():
                self.assertIn(ref,self.ids)
                self.assertTrue(self.ids[ref]['text'].strip())
            if attrs.get('aria-invalid')=='true':
                self.assertTrue(any('tide-field__error' in self.ids[ref]['attrs'].get('class','').split() for ref in attrs.get('aria-describedby','').split()))
            if node['tag'] in {'input','select','textarea'}:
                label=any(n['tag']=='label' and n['attrs'].get('for')==attrs.get('id') for n in self.nodes) if 'id' in attrs else False
                if attrs.get('type') not in {'checkbox','radio'}:self.assertTrue(label,attrs)
            if node['tag']=='a' and attrs.get('href','').startswith('#control-'):
                self.assertIn(attrs['href'][1:],self.ids)
        for ref in ['control-email-error-field','control-upload-invalid']:
            self.assertIn(self.ids[ref]['tag'],{'input','select','textarea'})
            self.assertEqual(self.ids[ref]['attrs']['aria-invalid'],'true')

    def test_required_and_reviewed_states_are_distinct_native_html(self):
        required=[n for n in self.nodes if 'required' in n['attrs']]
        self.assertEqual(len(required),2)
        self.assertTrue(all('aria-invalid' not in n['attrs'] for n in required))
        self.assertTrue(any(n['tag']=='button' and n['attrs'].get('type')=='reset' for n in self.nodes))
        self.assertTrue(all('novalidate' not in n['attrs'] for n in self.nodes if n['tag']=='form'))
        self.assertFalse(any(n['tag']=='script' for n in self.nodes))
        self.assertNotIn('aria-expanded',self.fragment)
        self.assertNotIn('role="alert"',self.fragment)
        self.assertFalse(any(n['tag']=='a' and n['attrs'].get('aria-disabled')=='true' and 'href' in n['attrs'] for n in self.nodes))

    def test_matrix_contains_the_audited_combinations(self):
        cases={n['attrs']['data-control-case'] for n in self.nodes if 'data-control-case' in n['attrs']}
        for case in ['readonly','disabled-select','invalid-disabled','choice-disabled-checked','choice-fieldset-disabled','chip-disabled-checked','chip-fieldset-disabled','chip-invalid','upload-invalid','upload-invalid-disabled','upload-required','summary-custom','context-text','context-choice','context-chip','context-summary','context-upload']:
            self.assertIn(case,cases)

    def test_disclosure_indicator_has_a_distributed_fallback_without_duplication(self):
        css=(ROOT/'css/patterns.css').read_text(encoding='utf-8')
        self.assertIn('.tide-expandable__summary:not(:has(.tide-expandable__icon))::after',css)
        self.assertIn('mask: var(--tide-control-chevron)',css)
        self.assertIn("--tide-control-chevron: url('../assets/icons/ChevronDownIcon.svg')",(ROOT/'css/tokens.css').read_text(encoding='utf-8'))
        self.assertTrue((ROOT/'assets/icons/ChevronDownIcon.svg').is_file())
        self.assertIn('.tide-expandable[open] > .tide-expandable__summary::after',css)
        self.assertIn('.tide-expandable[open] > .tide-expandable__summary .tide-expandable__icon',css)

    def test_select_indicator_keeps_native_semantics_and_listbox_exclusion(self):
        parsed=list(rules(self.css))
        selector,decl,_=next((s,d,c) for s,d,c in parsed if 'select.tide-field__control' in s and d.get('appearance')=='none')
        self.assertIn('.tide-field > select',selector)
        self.assertIn(":not([multiple], [size]:not([size='1']))",selector)
        self.assertEqual(decl['padding-inline-end'],'var(--tide-control-trailing-space)')
        _,marker,_=next((s,d,c) for s,d,c in parsed if s.startswith('.tide-field:has(') and 'mask' in d)
        self.assertEqual(marker['pointer-events'],'none')
        self.assertEqual(marker['grid-area'],decl['grid-area'])
        self.assertEqual(marker['mask'],'var(--tide-control-chevron) center / contain no-repeat')
        summary=next(d for s,d,c in rules((ROOT/'css/patterns.css').read_text(encoding='utf-8')) if s=='.tide-expandable__summary')
        tokens=next(d for s,d,c in rules((ROOT/'css/tokens.css').read_text(encoding='utf-8')) if s==':root')
        self.assertEqual(summary['min-block-size'],'var(--tide-size-control)')
        self.assertEqual(summary['padding'],'var(--tide-field-padding-block) var(--tide-control-inset-inline)')
        self.assertEqual(summary['line-height'],'var(--tide-leading-body)')
        self.assertEqual(tokens['--tide-field-padding-inline'],'var(--tide-control-inset-inline)')
        listbox=self.ids['control-listbox']['attrs']
        self.assertIn('multiple',listbox)
        self.assertEqual(listbox['size'],'3')
        self.assertEqual(self.ids['control-size-select']['attrs']['size'],'1')
        self.assertTrue(any(n['attrs'].get('dir')=='rtl' for n in self.nodes))

    def test_chip_active_feedback_follows_the_native_input_on_keyboard_press(self):
        active=[(s,d) for s,d,c in rules(self.css) if not c and s.startswith('.tide-chip:') and ':active' in s]
        self.assertEqual(len(active),2)
        self.assertTrue(all(':has(input:active)' in s for s,d in active))
        self.assertTrue(any('box-shadow' in d and 'var(--tide-focus-width)' in d['box-shadow'] for s,d in active))

    def test_registered_ownership_rejects_private_component_overrides(self):
        manifest=json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))
        entries={e['block']:e for e in manifest['components']}
        for block in BLOCKS:
            entry=entries[block]
            self.assertEqual(entry['htmlSource'],'templates/controls.html')
            self.assertEqual(entry['fixture'],'form-states.html')
            self.assertEqual(entry['styleOwnership'],'kit')
            self.assertTrue((ROOT/entry['contract']).is_file())
            self.assertTrue(style_ownership_issues('.'+block+' { padding: 3px; }',manifest))

    def test_shared_fragment_is_rendered_in_every_library_and_matrix(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('form_site_build',PROJECT/'site/tools/build.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        from compiler import load_themes
        rendered=module.outputs(*load_themes(ROOT/'tokens/themes.json'))
        matrices=[html for path,html in rendered.items() if path.name=='form-states.html']
        libraries=[html for path,html in rendered.items() if path.name=='index.html' and 'id="components"' in html]
        self.assertEqual(len(matrices),10)
        self.assertEqual(len(libraries),11)
        for html in matrices+libraries:
            self.assertIn('id="control-invalid-disabled"',html)
            self.assertIn('class="tide-icon tide-expandable__icon"',html)
            self.assertNotIn('{{CONTROL_',html)


if __name__=='__main__':unittest.main()
