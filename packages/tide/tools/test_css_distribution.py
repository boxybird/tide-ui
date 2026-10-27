"""Safety and rule parity of CSS distribution compaction."""
from pathlib import Path
import unittest

from build import strip_css_comments,outputs
from test_buttons import rules

ROOT=Path(__file__).resolve().parents[1]


class CssDistributionContracts(unittest.TestCase):
    def test_strings_urls_escapes_and_licenses_are_preserved(self):
        source='''/*! license */ /* ordinary */ a { content: "/* keep string */"; --quoted: 'a\\\'/* keep escaped */'; background: url(asset/*keep-url*/.svg); } /* @preserve keep */'''
        compact=strip_css_comments(source)
        self.assertNotIn('/* ordinary */',compact)
        for value in ['/*! license */','"/* keep string */"',"'a\\\'/* keep escaped */'",'url(asset/*keep-url*/.svg)','/* @preserve keep */']:
            self.assertIn(value,compact)
        self.assertEqual(strip_css_comments('screen/* split */and'), 'screen and')

    def test_every_canonical_module_keeps_the_same_rule_and_value_sequence(self):
        for source in (ROOT/'css').glob('*.css'):
            css=source.read_text(encoding='utf-8')
            self.assertEqual(list(rules(css)),list(rules(strip_css_comments(css))),source.name)

    def test_indentation_is_removed_without_rewriting_protected_text_or_tokens(self):
        source='a {\n    content: "first\\\n    second";\n    --message: "  text  ";\n    background: url("a  b.svg");\n    width: calc(100% - 1rem);\n  }'
        compact=strip_css_comments(source)
        self.assertIn('"first\\\n    second"',compact)
        self.assertIn('"  text  "',compact)
        self.assertIn('url("a  b.svg")',compact)
        self.assertIn('\nwidth: calc(100% - 1rem);\n}',compact)

    def test_generated_entry_keeps_header_layers_and_omits_source_commentary(self):
        css=next(data.decode() for path,data in outputs().items() if path.name=='tide.css')
        self.assertTrue(css.startswith('/* Generated Tide '))
        self.assertIn('@layer tide.components',css)
        self.assertNotIn('/* Feedback',css)
        self.assertIn('url(\'../assets/icons/ChevronDownIcon.svg\')',css)


if __name__=='__main__':unittest.main()
