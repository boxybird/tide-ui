"""Native directory journeys, fixture truth and unchanged CSS declarations."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import unittest

from html_templates import AppTemplates, ROOT
from presentation_contract import Tree
from css_distribution import compact_css
from test_presentation import style_rules


class VenueDirectoryContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = AppTemplates()

    def test_every_venue_has_a_real_document_and_matching_event_count(self):
        counts = Counter(event['venue'] for event in self.app.events)
        self.assertEqual(set(counts), set(self.app.venues_by_id))
        for venue_id, count in counts.items():
            html = self.app.page(venue_id)
            nodes = Tree(html).nodes
            cards = [node for node in nodes if 'tide-event-card' in node['classes']]
            self.assertEqual(len(cards), count)
            self.assertTrue(all(node['attrs'].get('data-venue')==venue_id for node in cards))
            self.assertEqual(sum(node['tag']=='h1' for node in nodes), 1)
            self.assertTrue(any(node['attrs'].get('id')=='results' for node in nodes))

    def test_map_and_rows_have_native_destinations_per_venue(self):
        html = self.app.page('venues')
        nodes = Tree(html).nodes
        ids = [node['attrs']['id'] for node in nodes if node['attrs'].get('id')]
        self.assertEqual(len(ids), len(set(ids)))
        for venue_id in self.app.venues_by_id:
            target = 'venue-map-card-'+venue_id
            triggers = [node for node in nodes if node['attrs'].get('popovertarget')==target and node['attrs'].get('popovertargetaction')!='hide']
            self.assertEqual(len(triggers), 1)
            self.assertTrue(any(node["attrs"].get("href")=="#map-"+venue_id for node in nodes))
            self.assertTrue(all(node['tag']=='button' for node in triggers))
            panel = next(node for node in nodes if node['attrs'].get('id')==target)
            self.assertIn('tide-panel', panel['classes'])
            self.assertEqual(panel['attrs']['popover'], 'auto')
            self.assertIn(venue_id+'.html#results', html)
        self.assertFalse(any(node['tag']=='script' for node in nodes))
        self.assertNotIn('style=', html)

    def test_search_uses_the_native_field_and_get_contract(self):
        nodes = Tree(self.app.page('venues')).nodes
        form = next(node for node in nodes if node['attrs'].get('id')=='venue-search-form')
        self.assertEqual(form['attrs']['action'], 'venues.html')
        self.assertEqual(form['attrs']['method'], 'get')
        self.assertEqual(form['attrs']['role'], 'search')
        controls = [node for node in nodes if node['tag']=='input']
        self.assertEqual(len(controls), 1)
        self.assertEqual(controls[0]['attrs']['name'], 'q')
        self.assertEqual(controls[0]['attrs']['type'], 'search')
        self.assertIn('tide-field__control', controls[0]['classes'])
        self.assertTrue(any(node['tag']=='label' and node['attrs'].get('for')==controls[0]['attrs']['id'] for node in nodes))

    def test_venue_text_escapes_and_image_sources_are_restricted(self):
        venue = deepcopy(self.app.venues[0])
        venue['name'] = '<script>not markup</script>'
        html = self.app.partial('venue-directory-row', self.app.venue_values(venue))
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)

    def test_asset_provenance_and_current_image_budget(self):
        records = json.loads((ROOT/'data/venue-images.json').read_text(encoding='utf-8'))['images']
        self.assertEqual(len(records), 7)
        for record in records:
            data = (ROOT/'src/runtime'/record['served']).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), record['servedSha256'])
            self.assertLessEqual(len(data), 200000)

    def test_distribution_compaction_preserves_all_application_rules(self):
        manifest = json.loads((ROOT/'consumer-manifest.json').read_text(encoding='utf-8'))
        css = '\n'.join((ROOT/name).read_text(encoding='utf-8') for name in manifest['styleHome'])
        def declarations(source):
            return [(selector, [tuple(part.strip() for part in declaration.split(':', 1))
                                for declaration in body.split(';')])
                    for selector, body in style_rules(source)]
        self.assertEqual(declarations(css), declarations(compact_css(css)))
        source = '''/*! license */ .x { content: "a;  b\\\n    c"; background: url("a  b.svg"); /* omitted */ width: calc(100% - 1rem); }'''
        result = compact_css(source)
        self.assertIn('/*! license */', result)
        self.assertIn('"a;  b\\\n    c"', result)
        self.assertIn('url("a  b.svg")', result)
        self.assertIn('width:calc(100% - 1rem)', result)
        self.assertNotIn('omitted', result)


if __name__=='__main__':
    unittest.main()
