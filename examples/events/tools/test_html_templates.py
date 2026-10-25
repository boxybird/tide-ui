"""Contracts for escaped values, complete routes and selected/scoped lists."""
from copy import deepcopy
from html.parser import HTMLParser
import unittest

from html_templates import AppTemplates, ROOT, expand


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.cards = []; self.current = []; self.inputs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        if 'tide-event-card' in classes:
            self.cards.append(attrs)
        if 'tide-event-card--in-view' in classes:
            self.current.append(attrs['aria-labelledby'].removeprefix('card-'))
        if tag=='input':
            self.inputs.append(attrs.get('id'))


class TemplateContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = AppTemplates()

    def test_every_event_route_selects_its_own_card_once(self):
        for slug in self.app.by_id:
            with self.subTest(slug=slug):
                parsed = Elements(self.app.page(ROOT/'src/pages'/(slug+'.html')))
                self.assertEqual(len(parsed.cards), 54)
                self.assertEqual(parsed.current, [slug])
                for control in ('event-query', 'event-from', 'event-to', 'venue-scope'):
                    self.assertEqual(parsed.inputs.count(control), 1)

    def test_venue_and_saved_collections_reuse_canonical_cards(self):
        venue = Elements(self.app.page(ROOT/'src/pages/sunshine-theater.html'))
        self.assertEqual(len(venue.cards), 6)
        self.assertEqual({card['data-venue'] for card in venue.cards}, {'sunshine-theater'})
        self.assertEqual(venue.current, [])
        saved = Elements(self.app.page(ROOT/'src/pages/saved.html'))
        self.assertEqual(len(saved.cards), 1)
        self.assertEqual(saved.current, ['ink-after-dark'])
        self.assertNotIn('data-venue', saved.cards[0])  # Existing shortlist semantics.

    def test_sample_text_is_escaped_in_text_and_attribute_contexts(self):
        event = deepcopy(self.app.events[0])
        event['title'] = '<img src=x onerror="alert(1)"> & "Example"'
        event['search'] = '" autofocus onfocus="alert(1)'
        card = self.app.card(event, '')
        self.assertNotIn('<img', card)
        self.assertIn('&lt;img', card)
        parsed = Elements(card)
        self.assertEqual(parsed.cards[0]['data-search'], event['search'])
        self.assertNotIn('autofocus', parsed.cards[0])
        self.assertNotIn('onfocus', parsed.cards[0])

    def test_text_that_looks_like_a_template_is_not_executed(self):
        self.assertEqual(expand('{{TITLE}}', {'TITLE':'{{> unknown}}'}, {}), '{{&gt; unknown}}')

    def test_missing_values_and_partials_fail(self):
        with self.assertRaisesRegex(ValueError, 'Unknown app template value'):
            expand('{{MISSING}}', {}, {})
        with self.assertRaisesRegex(ValueError, 'Unknown app partial'):
            expand('{{> unknown}}', {}, {})
        with self.assertRaisesRegex(ValueError, 'Unknown app route'):
            self.app.context('missing-route')

    def test_cyclic_includes_fail_with_context(self):
        with self.assertRaisesRegex(ValueError, 'first -> second -> first'):
            expand('{{> first}}', {}, {'first':'{{> second}}', 'second':'{{> first}}'})

    def test_malformed_tokens_and_include_paths_fail(self):
        for text in ('{{TITLE', '{{title}}', '{{> ../header}}'):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'Malformed app template token'):
                expand(text, {}, {})

    def test_existing_navigation_variants_keep_active_links(self):
        for route, href in [('index', 'index.html'), ('sunshine-theater', 'index.html'), ('saved', 'saved.html'), ('submit', 'submit.html')]:
            with self.subTest(route=route):
                header = self.app.partial('header', self.app.context(route))
                self.assertIn('href="'+href+'" aria-current="page"', header)
        self.assertNotIn('aria-current', self.app.partial('header', self.app.context('help')))


if __name__=='__main__':
    unittest.main()
