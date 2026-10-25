"""Regression tests for the theme guarantees, not copies of component CSS."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from palette import contrast, from_hex, gamut, linear_rgb, resolve, checks
from build import load_themes


class ThemeTests(unittest.TestCase):
    def test_known_wcag_reference_values(self):
        self.assertAlmostEqual(contrast(from_hex('#ffffff'), from_hex('#000000')), 21, places=4)
        self.assertAlmostEqual(contrast(from_hex('#777777'), from_hex('#ffffff')), 4.4781, places=3)
        self.assertLess(contrast(from_hex('#777777'), from_hex('#ffffff')), 4.5)

    def test_srgb_gamut_mapping_preserves_lightness_and_hue(self):
        color = gamut([.7,.5,65])
        self.assertEqual(color[0],.7)
        self.assertEqual(color[2],65)
        self.assertLess(color[1],.5)
        self.assertTrue(all(-.00001 <= n <= 1.00001 for n in linear_rgb(color)))

    def test_background_changes_regenerate_surfaces_and_readable_pairs(self):
        original = resolve({'canvas':[.925,.06,65], 'accent':[.41,.105,340]})
        changed = resolve({'canvas':[.86,.12,45], 'accent':[.41,.105,340]})
        self.assertNotEqual(original['surface'],changed['surface'])
        self.assertNotEqual(original['field'],changed['field'])
        self.assertTrue(all(row['pass'] for row in checks(changed)))

    def test_foreground_polarity_follows_surface_not_mode_name(self):
        for canvas in ([.965,.05,95],[.925,.06,65],[.2,.02,240],[.32,.03,65]):
            with self.subTest(canvas=canvas):
                self.assertTrue(all(row['pass'] for row in checks(resolve({'canvas':canvas,'accent':[.6,.1,190]}))))

    def test_incompatible_surface_context_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'No common accessible foreground'):
            resolve({'canvas':[.05,0,0], 'accent':[.5,.05,200], 'overrides':{'surface':[.99,0,0]}})

    def test_all_shipped_themes_pass(self):
        _, resolved, audit = load_themes(Path(__file__).resolve().parents[1]/'tokens/themes.json')
        self.assertGreater(len(resolved),0)
        self.assertTrue(all(set(modes)=={'light','dark'} for modes in resolved.values()))
        self.assertTrue(all(row['pass'] for modes in audit.values() for rows in modes.values() for row in rows))

    def temporary_input(self, text):
        return load_themes(SimpleNamespace(read_text=lambda **options: text))

    def test_incomplete_mode_and_geometry_injection_are_rejected(self):
        base={'schemaVersion':1,'themes':{'sample':{'name':'Sample','description':'Test','light':{'canvas':[.9,.01,80],'accent':[.3,.01,180]}}}}
        with self.assertRaisesRegex(ValueError,'must include dark'):
            self.temporary_input(json.dumps(base))
        base['themes']['sample']['dark']=copy.deepcopy(base['themes']['sample']['light'])
        base['themes']['sample']['radius']=100
        with self.assertRaisesRegex(ValueError,'geometry cannot be themed'):
            self.temporary_input(json.dumps(base))

    def test_duplicate_names_and_unknown_roles_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'Duplicate JSON key'):
            self.temporary_input('{"schemaVersion":1,"schemaVersion":1,"themes":{}}')
        mode={'canvas':[.9,.01,80],'accent':[.3,.01,180],'overrides':{'font-size':[1,0,0]}}
        data={'schemaVersion':1,'themes':{'sample':{'name':'Sample','description':'Test','light':mode,'dark':mode}}}
        with self.assertRaisesRegex(ValueError,'Unknown semantic override'):
            self.temporary_input(json.dumps(data))


if __name__=='__main__': unittest.main()
