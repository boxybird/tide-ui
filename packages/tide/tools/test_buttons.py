"""Regression contracts for the audited size/context/state failures.

Native browser measurements are recorded separately; these portable guards stop
implicit geometry overrides and missing specimens entering the normal build.
"""
import json
from pathlib import Path
import re
import unittest

from contracts import style_ownership_issues
from palette import contrast
from compiler import load_themes

ROOT = Path(__file__).resolve().parents[1]


def rules(css, context=()):
    """Read flat declaration rules through grouping at-rules, without dependencies."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    cursor = 0
    while (start := css.find('{', cursor)) >= 0:
        selector = css[cursor:start].strip()
        depth, end = 1, start + 1
        while depth and end < len(css):
            depth += (css[end] == '{') - (css[end] == '}')
            end += 1
        body = css[start + 1:end - 1]
        if selector.startswith('@'):
            yield from rules(body, context + (selector,))
        else:
            declarations = dict(part.strip().split(':', 1) for part in body.split(';') if ':' in part)
            yield selector, {k.strip(): v.strip() for k, v in declarations.items()}, context
        cursor = end


def geometry_issues(css):
    protected = {'font', 'font-family', 'font-style', 'font-size', 'font-weight', 'line-height', 'text-transform',
                 'letter-spacing', 'padding', 'padding-inline', 'padding-block',
                 'padding-inline-start', 'padding-inline-end', 'padding-block-start',
                 'padding-block-end', 'border', 'border-width', 'border-radius',
                 'min-block-size', 'block-size', 'inline-size', 'width', 'height'}
    bases = {'.tide-button', '.tide-icon-button', '.tide-photo-control'}
    issues = []
    for selector, declarations, context in rules(css):
        positive=re.sub(r':not\(\s*\.tide-(?:button|icon-button|photo-control)\s*\)','',selector)
        if not re.search(r'\.tide-(?:button|icon-button|photo-control)(?![\w-])|\.tide-(?:button|icon-button|photo-control)--', positive):
            continue
        if selector.endswith(' .tide-icon'):
            continue  # Icon descendants have their own dimensions.
        for name in protected & declarations.keys():
            if name == 'border' and any('forced-colors' in c for c in context):
                continue  # Same reserved border, system color only.
            base = all(s.strip() in bases for s in selector.split(','))
            sized = all(re.search(r'\.tide-(?:button--(?:compact|icon)|(?:icon-button|photo-control)--regular)(?![\w-])', s)
                        or s.strip() in {'.tide-icon-button', '.tide-photo-control'} for s in selector.split(','))
            full = selector == '.tide-button--full' and name == 'inline-size'
            if context or not (base or sized or full):
                issues.append((selector, name))
        if selector in {'.tide-button--plan', '.tide-button--spread', '.tide-button--spread, .tide-button--plan'}:
            issues.extend((selector, name) for name in declarations if name.startswith('margin'))
    return issues


class ButtonContracts(unittest.TestCase):
    def test_component_exclusions_do_not_count_as_button_overrides(self):
        self.assertEqual(geometry_issues('.tide-toast > a:where(:not(.tide-button)) { min-block-size: 44px; font-size: 14px; }'),[])

    def test_current_geometry_has_no_implicit_viewport_emphasis_or_context_overrides(self):
        for source in (ROOT/'css').glob('*.css'):
            with self.subTest(source=source.name):
                self.assertEqual(geometry_issues(source.read_text(encoding='utf-8')), [])

    def test_guards_detect_the_audited_regressions(self):
        for regression in [
            '.tide-button--quiet { padding-inline: .5rem; }',
            '.tide-button--plan { font-weight: 650; border: 0; }',
            '@media (width < 350px) { .tide-button { padding-inline: 1rem; } }',
            '.reading-context .tide-button { font-size: 1rem; }',
            '.tide-button--plan { margin-block-start: 1.5rem; }',
        ]:
            with self.subTest(regression=regression):
                self.assertTrue(geometry_issues(regression))

    def test_default_type_is_explicit_and_size_changes_are_opt_in(self):
        css = (ROOT/'css/components.css').read_text(encoding='utf-8')
        base = next(d for s, d, c in rules(css) if s == '.tide-button, .tide-icon-button, .tide-photo-control' and not c)
        self.assertIn('var(--tide-button-font-size)', base['font-size'])
        self.assertIn('var(--tide-button-leading)', base['line-height'])
        self.assertIn('var(--tide-button-font-weight)', base['font-weight'])
        self.assertEqual(base['font-style'], 'normal')
        self.assertEqual(base['text-transform'], 'none')
        self.assertTrue(any(s == '.tide-button--compact' for s, _, _ in rules(css)))
        spread = next(d for s, d, _ in rules(css) if s == '.tide-button--spread')
        self.assertLessEqual(set(spread), {'justify-content', 'text-align'})

    def test_button_and_photo_ownership_cannot_be_bypassed_by_consumers(self):
        manifest = json.loads((ROOT/'component-manifest.json').read_text(encoding='utf-8'))
        for block in ['tide-button', 'tide-icon-button', 'tide-photo-control']:
            with self.subTest(block=block):
                self.assertEqual(style_ownership_issues('.'+block+' { padding: 99rem; }', manifest),
                                 ['Kit-owned selectors redefined in app CSS: '+block])
        self.assertEqual(style_ownership_issues('.tide-app__actions { gap: 1rem; }', manifest), [])
        entries = manifest['components'] + manifest['supportingBlocks']
        for block in ['tide-button', 'tide-icon-button', 'tide-photo-control']:
            entry = next(e for e in entries if e['block'] == block)
            for field in ['source', 'htmlSource', 'contract']:
                self.assertTrue((ROOT/entry[field].split('#')[0]).is_file(), (block, field))
            self.assertEqual(entry['fixture'], 'button-states.html')

    def test_authored_state_matrix_covers_each_emphasis_and_disabled_precedence(self):
        html = (ROOT/'templates/buttons.html').read_text(encoding='utf-8')
        for variant in ['primary', 'secondary', 'quiet']:
            for state in ['rest', 'pressed', 'disabled', 'pressed-disabled']:
                self.assertIn('data-button-case="'+variant+'-'+state+'"', html)
        for case in ['spread', 'plan', 'compact', 'body-context', 'reading-context', 'emphasis-context',
                     'icon-regular', 'icon-compact', 'icon-pressed-disabled',
                     'photo-compact', 'photo-regular', 'photo-pressed-disabled', 'disabled-link']:
            self.assertIn('data-button-case="'+case+'"', html)
        self.assertNotIn('focus-sample', html)
        self.assertNotIn('<script', html)

    def test_hover_and_active_colors_are_distinct_and_both_readable_in_all_modes(self):
        _, themes, _ = load_themes(ROOT/'tokens/themes.json')
        for theme, modes in themes.items():
            for mode, roles in modes.items():
                with self.subTest(theme=theme, mode=mode):
                    self.assertNotEqual(roles['accent-hover'], roles['accent-active'])
                    self.assertGreaterEqual(contrast(roles['on-accent'], roles['accent-active']), 4.5)
                    self.assertNotEqual(roles['photo-accent-hover'], roles['photo-accent-active'])
                    self.assertGreaterEqual(contrast(roles['on-photo-accent'], roles['photo-accent-active']), 4.5)

    def test_forced_colors_uses_the_same_selected_selector_for_all_action_families(self):
        css = (ROOT/'css/components.css').read_text(encoding='utf-8')
        selected = [s for s, d, c in rules(css) if any('forced-colors' in x for x in c)
                    and "[aria-pressed='true']" in s and 'outline' in d]
        self.assertEqual(len(selected), 1)
        for block in ['tide-button', 'tide-icon-button', 'tide-photo-control']:
            self.assertIn('.'+block, selected[0])

    def test_selected_active_feedback_can_override_hover_at_equal_specificity(self):
        css = (ROOT/'css/components.css').read_text(encoding='utf-8')
        hover = next(s for s, d, _ in rules(css) if ':hover' in s and 'box-shadow' in d)
        active = next(s for s, d, _ in rules(css) if ':active' in s and 'box-shadow' in d)
        self.assertEqual(hover.replace(':hover', ':active'), active)


if __name__ == '__main__':
    unittest.main()
