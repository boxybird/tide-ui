"""Progressive-enhancement and package boundaries for the page recipes."""
from pathlib import Path
import unittest

from contracts import ContractScan
from build import outputs

ROOT = Path(__file__).resolve().parents[1]


class PageRecipeContracts(unittest.TestCase):
    def test_validation_remains_usable_before_the_enhancement_runs(self):
        scan = ContractScan()
        scan.feed((ROOT/'templates/frames/form-validation.html').read_text(encoding='utf-8'))
        form = next(n for n in scan.nodes if n['tag']=='form')
        self.assertNotIn('novalidate', form['attrs'])
        controls = [n for n in scan.nodes if n['tag']=='input']
        self.assertTrue(all('required' in n['attrs'] for n in controls))
        self.assertTrue(all('aria-invalid' not in n['attrs'] for n in controls))
        self.assertTrue(all('aria-describedby' in n['attrs'] for n in controls))
        disclosure = next(n for n in scan.nodes if n['tag']=='details')
        self.assertIn('open', disclosure['attrs'])
        summary = next(n for n in scan.nodes if 'tide-error-summary' in n['attrs'].get('class','').split())
        self.assertEqual(summary['tag'], 'section')
        self.assertIn('aria-labelledby', summary['attrs'])
        self.assertIn('hidden', summary['attrs'])
        self.assertNotEqual(summary['attrs'].get('role'), 'alert')
        self.assertEqual(summary['attrs']['tabindex'], '-1')

    def test_documentation_demos_do_not_enter_the_css_distribution(self):
        files = outputs()
        self.assertFalse(any(p.suffix=='.js' for p in files))
        css = next(content.decode('utf-8') for p, content in files.items() if p.name=='tide.css')
        self.assertIn('.tide-venue-profile', css)
        self.assertIn('.tide-error-summary', css)
        self.assertNotIn('recipe-demos.js', css)


if __name__=='__main__':
    unittest.main()
