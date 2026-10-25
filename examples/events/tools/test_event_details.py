"""Detail content stays escaped, accessible and reusable across native routes."""
from copy import deepcopy
from html.parser import HTMLParser
import unittest

from html_templates import AppTemplates, ROOT


class DetailDocument(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.nodes=[]; self.by_id={}; self.duplicates=[]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.nodes.append((tag, attrs))
        if attrs.get('id'):
            if attrs['id'] in self.by_id: self.duplicates.append(attrs['id'])
            self.by_id[attrs['id']]=(tag, attrs)


class DetailContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=AppTemplates()

    def test_one_document_recipe_generates_all_original_routes(self):
        pages=self.app.pages()
        self.assertEqual(set(pages), {slug+'.html' for slug in self.app.by_id} | {slug+'.html' for slug in self.app.routes})
        self.assertEqual(len(pages), 60)
        self.assertEqual({p.name for p in (ROOT/'src/pages').glob('*.html')}, {page['source'] for page in self.app.routes.values() if page.get('source')})

    def test_each_event_has_one_page_title_and_stable_anchor_hierarchy(self):
        for slug in self.app.by_id:
            with self.subTest(slug=slug):
                doc=DetailDocument(self.app.page(slug))
                self.assertFalse(doc.duplicates)
                self.assertEqual(sum(tag=='h1' for tag, attrs in doc.nodes), 1)
                self.assertEqual(doc.by_id['event-title'][0], 'h1')
                self.assertEqual(doc.by_id['story-title'][0], 'h2')
                self.assertEqual(doc.by_id['attendance'][0], 'h3')
                self.assertEqual(doc.by_id['attendance'][1]['tabindex'], '-1')

    def test_default_and_saved_previews_shift_headings_without_duplicate_data(self):
        for route, selected in [('index','high-desert-signal'), ('search','high-desert-signal'), ('saved','ink-after-dark')]:
            with self.subTest(route=route):
                doc=DetailDocument(self.app.page(route))
                self.assertEqual(doc.by_id['event-title'][0], 'h2')
                self.assertEqual(doc.by_id['story-title'][0], 'h3')
                self.assertEqual(doc.by_id['attendance'][0], 'h4')
                self.assertEqual(self.app.routes[route]['selected'], selected)

    def test_venue_links_and_distinct_controls_remain_intact(self):
        full=DetailDocument(self.app.details.render(self.app.by_id['ink-after-dark'], 1))
        concise=DetailDocument(self.app.details.render(self.app.by_id['high-desert-signal'], 1))
        self.assertTrue(any(attrs.get('href')=='saved.html' for tag, attrs in full.nodes))
        self.assertFalse(any(attrs.get('href')=='saved.html' for tag, attrs in concise.nodes))
        self.assertIn('venue-information', concise.by_id)
        self.assertTrue(any(attrs.get('href')=='sunshine-theater.html' for tag, attrs in concise.nodes))
        self.assertNotIn('tabindex', full.by_id['event-title'][1])
        self.assertEqual(concise.by_id['event-title'][1]['tabindex'], '-1')

    def test_authored_timestamps_keep_daylight_saving_offsets_and_ranges(self):
        full=DetailDocument(self.app.details.render(self.app.by_id['the-imperfect-print'], 1))
        self.assertTrue(any(attrs.get('datetime')=='2026-11-12T18:00:00-07:00' for tag, attrs in full.nodes))
        concise=DetailDocument(self.app.details.render(self.app.by_id['high-desert-signal'], 1))
        self.assertTrue(any(attrs.get('datetime')=='2026-10-30T22:30:00-06:00' for tag, attrs in concise.nodes))

    def test_prose_and_photo_alt_are_escaped_in_their_own_contexts(self):
        event=deepcopy(self.app.by_id['ink-after-dark'])
        event['detail']['lead']='<script>alert(1)</script> & an example'
        event['detail']['image']['alt']='" onerror="alert(1)'
        source=self.app.details.render(event, 1)
        self.assertNotIn('<script>', source)
        self.assertIn('&lt;script&gt;', source)
        image=next(attrs for tag, attrs in DetailDocument(source).nodes if tag=='img')
        self.assertEqual(image['alt'], event['detail']['image']['alt'])
        self.assertNotIn('onerror', image)

    def test_raw_html_blocks_and_unsafe_links_are_rejected(self):
        event=deepcopy(self.app.by_id['high-desert-signal'])
        event['detail']['sections'][0]['blocks']=[{'type':'raw-html','text':'<script></script>'}]
        with self.assertRaisesRegex(ValueError, 'Unsupported detail block'):
            self.app.details.render(event, 1)
        event['detail']['sections'][0]['blocks']=[{'type':'link','href':'javascript:alert(1)','label':'Example'}]
        with self.assertRaisesRegex(ValueError, 'Unsupported detail link target'):
            self.app.details.render(event, 1)

    def test_invalid_heading_levels_and_image_sources_fail(self):
        event=deepcopy(self.app.by_id['ink-after-dark'])
        with self.assertRaisesRegex(ValueError, 'Detail heading level'):
            self.app.details.render(event, 4)
        event['detail']['image']['src']='javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'Unsupported sample detail image'):
            self.app.details.render(event, 1)


if __name__=='__main__':
    unittest.main()
