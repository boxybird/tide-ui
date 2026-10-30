"""Native result journeys retain their venue and its information on recovery."""
import re
import unittest
from urllib.parse import urlsplit

from html_templates import AppTemplates
from test_html_templates import Elements
from test_utility_pages import Document


class VenueScopeContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = AppTemplates()
        cls.routes = {name:page for name,page in cls.app.routes.items() if page.get('venue')=='sunshine-theater'}

    def test_reference_result_routes_stay_scoped_without_a_tutorial_menu(self):
        for route,page in self.routes.items():
            source = self.app.page(route)
            self.assertNotIn('sample result states', source)
            self.assertNotIn('href="sunshine-theater-empty.html"', source)
            for destination in self.app.routes[page['venue']]['resultRoutes'].values():
                target = self.app.routes[destination]
                self.assertEqual((target['collection'], target['venue']), ('venue', 'sunshine-theater'))
        venue = [e for e in self.app.events if e['venue']=='sunshine-theater']
        self.assertEqual(len(venue), 6)
        self.assertTrue(all(e['category']=='music' for e in venue))

    def test_empty_views_keep_information_and_scoped_reset_return_and_form(self):
        for route,page in self.routes.items():
            source = self.app.page(route)
            doc = Document(source)
            ids = {attrs['id']:(tag,attrs) for tag,attrs in doc.nodes if 'id' in attrs}
            parsed = Elements(source)
            self.assertEqual(len(parsed.cards), 0 if page.get('sampleFilter',{}).get('empty') else 6)
            self.assertEqual(ids['venue-scope'][1]['value'], 'sunshine-theater')
            self.assertEqual(ids['event-search-form'][1]['action'], 'sunshine-theater.html')
            self.assertIn('venue-information', ids)
            self.assertIn('hidden', ids['preview-state'][1])
            self.assertEqual('hidden' in ids['empty-results'][1], bool(parsed.cards))
            self.assertIn('href="#venue-information">Venue details</a>', source)
            photo = next(attrs for tag,attrs in doc.nodes if tag=='img' and 'tide-venue__photo' in attrs.get('class',''))
            self.assertEqual(photo['src'], self.app.venues_by_id['sunshine-theater']['image'])
            reset = next((tag,attrs) for tag,attrs in doc.nodes if 'data-filter-reset' in attrs)
            self.assertEqual((reset[0], reset[1]['href']), ('a', 'sunshine-theater.html'))
            empty = re.search(r'<div class="tide-empty" id="empty-results".*?</div>', source, re.S)[0]
            recovery = next(attrs['href'] for tag,attrs in Document(empty).nodes if tag=='a')
            self.assertEqual(urlsplit(recovery).path, 'sunshine-theater.html')
            self.assertIn('href="index.html">All events across Albuquerque</a>', source)

    def test_browse_heading_is_unique_and_outside_the_popover(self):
        for route,page in self.app.routes.items():
            if page.get('collection') not in ('all','venue'):
                continue
            source = self.app.page(route)
            doc = Document(source)
            self.assertEqual(sum(tag=='h1' for tag,attrs in doc.nodes), 1, route)
            self.assertEqual(sum(attrs.get('id')=='results-title' for tag,attrs in doc.nodes), 1, route)
            self.assertNotIn('lineup-filters', Elements(source).ancestors['results-title'])

    def test_global_reset_remains_native_without_reference_state_links(self):
        source = self.app.page('index')
        reset = next((tag,attrs) for tag,attrs in Document(source).nodes if 'data-filter-reset' in attrs)
        self.assertEqual((reset[0], reset[1]['type'], reset[1]['form']), ('button', 'reset', 'event-search-form'))
        for route in ('search-music', 'search-comedy', 'search-workshop', 'search-empty'):
            self.assertNotIn('href="'+route+'.html"', source)

    def test_all_venue_and_event_journeys_keep_their_scope_and_original_detail(self):
        for route in set(self.app.venues_by_id) | set(self.app.by_id):
            event = self.app.by_id.get(route)
            venue_id = event['venue'] if event else route
            venue = self.app.venues_by_id[venue_id]
            expected = {item['id'] for item in self.app.events if item['venue']==venue_id}
            source = self.app.page(route)
            parsed = Elements(source)
            self.assertEqual({card['aria-labelledby'].removeprefix('card-') for card in parsed.cards}, expected, route)
            self.assertEqual(len(parsed.cards), len(expected), route)
            self.assertEqual({card['data-venue'] for card in parsed.cards}, {venue_id}, route)
            ids = {attrs['id']:(tag,attrs) for tag,attrs in Document(source).nodes if 'id' in attrs}
            self.assertEqual(ids['venue-scope'][1]['value'], venue_id)
            self.assertEqual(ids['event-search-form'][1]['action'], route+'.html')
            self.assertEqual(ids['event-query'][1]['placeholder'], 'Event or artist')
            self.assertIn('Events at '+venue['name'], source)
            self.assertIn('tide-app--columns', source)
            self.assertIn('href="'+venue_id+'.html">All venue events</a>', source)
            self.assertIn('href="index.html">All events across Albuquerque</a>', source)
            reset = next(attrs for tag,attrs in Document(source).nodes if 'data-filter-reset' in attrs)
            self.assertEqual(reset['href'], route+'.html')
            if event:
                self.assertEqual(parsed.current, [route])
                self.assertIn(self.app.details.render(event, 1), source)
                self.assertIn('href="'+venue_id+'.html#venue-information">Venue details</a>', source)
            else:
                self.assertEqual(parsed.current, [])
                self.assertIn('venue-information', ids)
                photo = next(attrs for tag,attrs in Document(source).nodes if tag=='img' and 'tide-venue__photo' in attrs.get('class',''))
                self.assertEqual(photo['src'], venue['image'])
                self.assertIn('href="#venue-information">Venue details</a>', source)
        self.assertEqual(len(Elements(self.app.page('index')).cards), 54)


if __name__ == '__main__':
    unittest.main()
