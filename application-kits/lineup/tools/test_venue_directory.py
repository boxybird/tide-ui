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
            row = next(node for node in nodes if node['attrs'].get('id')=='venue-'+venue_id)
            point = next(node for node in nodes if node['attrs'].get('id')=='map-'+venue_id)
            row_links = [node for node in nodes if node['tag']=='a' and row in node['parents']]
            point_links = [node for node in nodes if node['tag']=='a' and point in node['parents']]
            primary = [node for node in row_links if 'tide-event-card__link' in node['classes']]
            self.assertEqual(len(primary), 2)
            select = next(node for node in primary if any('tide-venue__select' in p['classes'] for p in node['parents']))
            open_venue = next(node for node in primary if any('tide-venue__open' in p['classes'] for p in node['parents']))
            self.assertEqual(select['attrs']['href'], '#map-'+venue_id)
            self.assertEqual(open_venue['attrs']['href'], venue_id+'.html')
            name = self.app.venues_by_id[venue_id]['name']
            count = sum(event['venue']==venue_id for event in self.app.events)
            self.assertEqual(open_venue['attrs']['aria-label'], f'View {name} and its {count} events')
            self.assertEqual(point_links[0]['attrs']['href'], '#venue-'+venue_id)
            self.assertIn('tide-photo-control', point_links[0]['classes'])
            panel_id='map-panel-'+venue_id
            trigger=next(node for node in nodes if node['tag']=='button' and point in node['parents'] and node['attrs'].get('popovertarget')==panel_id and not node['attrs'].get('popovertargetaction'))
            self.assertEqual(trigger['attrs']['aria-label'], 'Preview '+name)
            panel=next(node for node in nodes if node['attrs'].get('id')==panel_id)
            self.assertEqual(panel['attrs']['popover'], 'auto')
            self.assertEqual(panel['attrs']['role'], 'dialog')
            self.assertEqual(panel['attrs']['aria-labelledby'], 'map-panel-title-'+venue_id)
            self.assertTrue(any(node['classes']=={'tide-panel'} and panel in node['parents'] for node in nodes))
            self.assertTrue(any(node['tag']=='button' and node['attrs'].get('popovertarget')==panel_id and node['attrs'].get('popovertargetaction')=='hide' and panel in node['parents'] for node in nodes))
            self.assertTrue(any(node['tag']=='a' and node['attrs']['href']==venue_id+'.html' and panel in node['parents'] for node in nodes))
            self.assertEqual(row['attrs']['tabindex'], '-1')
            self.assertEqual(point['attrs']['tabindex'], '-1')
            self.assertTrue(any(node['attrs']['href']==venue_id+'.html' for node in row_links))
            self.assertTrue(any('tide-badge' in node['classes'] and row in node['parents'] for node in nodes))
            # Page-context Badge colors must not be placed on a dark map image.
            # Map selection text inherits the Photo control's reading role.
            self.assertFalse(any('tide-badge' in node['classes'] and point in node['parents'] for node in nodes))
        scripts=[node['attrs'] for node in nodes if node['tag']=='script']
        self.assertEqual(scripts, [{'type':'module','src':'{{MAP_ROOT}}/venue-map.mjs'}])
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

    def test_event_card_headings_follow_the_host_collection(self):
        for venue_id in self.app.venues_by_id:
            nodes=Tree(self.app.page(venue_id)).nodes
            titles=[node for node in nodes if 'tide-event-card__title' in node['classes']]
            self.assertTrue(titles)
            self.assertTrue(all(node['tag']=='h4' for node in titles), venue_id)
        for route in ('index', 'saved'):
            titles=[node for node in Tree(self.app.page(route)).nodes if 'tide-event-card__title' in node['classes']]
            self.assertTrue(all(node['tag']=='h4' for node in titles), route)
        with self.assertRaises(ValueError):
            self.app.card(self.app.events[0], '', heading_level='3 onclick=example')

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
        map_css=(ROOT/'src/map/venue-map.css').read_text(encoding='utf-8')
        self.assertEqual(declarations(map_css), declarations(compact_css(map_css)))
        source = '''/*! license */ .x { content: "a;  b\\\n    c"; background: url("a  b.svg"); /* omitted */ width: calc(100% - 1rem); }'''
        result = compact_css(source)
        self.assertIn('/*! license */', result)
        self.assertIn('"a;  b\\\n    c"', result)
        self.assertIn('url("a  b.svg")', result)
        self.assertIn('width:calc(100% - 1rem)', result)
        self.assertNotIn('omitted', result)


if __name__=='__main__':
    unittest.main()
