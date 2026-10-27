"""Contracts for escaped values, complete routes and selected/scoped lists."""
from copy import deepcopy
from html.parser import HTMLParser
import unittest

from html_templates import AppTemplates, ROOT, expand


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.cards = []; self.current = []; self.inputs = []; self.stack = []; self.ancestors = {}; self.navigation = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ancestors[attrs['id']] = [parent.get('id') for _, parent in self.stack]
        classes = attrs.get('class', '').split()
        if tag=='a' and 'tide-site-header__link' in classes:
            self.navigation.append(attrs)
        if 'tide-event-card' in classes:
            self.cards.append(attrs)
        if 'tide-event-card--in-view' in classes:
            self.current.append(attrs['aria-labelledby'].removeprefix('card-'))
        if tag=='input':
            self.inputs.append(attrs.get('id'))
        if tag not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):
            self.stack.append((tag, attrs))

    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


class TemplateContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = AppTemplates()

    def test_every_event_route_selects_its_own_card_once(self):
        for slug in self.app.by_id:
            with self.subTest(slug=slug):
                parsed = Elements(self.app.page(slug))
                self.assertEqual(len(parsed.cards), 54)
                self.assertEqual(parsed.current, [slug])
                for control in ('event-query', 'event-from', 'event-to', 'venue-scope'):
                    self.assertEqual(parsed.inputs.count(control), 1)

    def test_every_document_preloads_the_shared_local_font(self):
        for name, page in self.app.pages().items():
            with self.subTest(name=name):
                preload='<link rel="preload" href="{{KIT_ASSETS}}/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>'
                self.assertIn(preload, page)
                self.assertLess(page.index(preload), page.index('<link rel="stylesheet"'))

    def test_venue_and_saved_collections_reuse_canonical_cards(self):
        venue = Elements(self.app.page(ROOT/'src/pages/sunshine-theater.html'))
        self.assertEqual(len(venue.cards), 6)
        self.assertEqual({card['data-venue'] for card in venue.cards}, {'sunshine-theater'})
        self.assertEqual(venue.current, [])
        saved = Elements(self.app.page(ROOT/'src/pages/saved.html'))
        self.assertEqual(len(saved.cards), 1)
        self.assertEqual(saved.current, ['ink-after-dark'])
        self.assertNotIn('data-venue', saved.cards[0])  # Existing shortlist semantics.

    def test_one_heading_stays_outside_the_popover_while_controls_remain_inside(self):
        for route in set(self.app.by_id) | {name for name,page in self.app.routes.items() if page.get('collection') in ('all','venue')}:
            with self.subTest(route=route):
                parsed=Elements(self.app.page(route))
                for identifier in ('event-search-form','event-from','event-to'):
                    self.assertIn('lineup-filters', parsed.ancestors[identifier])
                    self.assertNotIn('results', parsed.ancestors[identifier])
                self.assertNotIn('lineup-filters', parsed.ancestors['results-title'])
                self.assertNotIn('results', parsed.ancestors['results-title'])
                self.assertIn('results', parsed.ancestors['result-count'])
                self.assertNotIn('lineup-filters', parsed.ancestors['result-count'])
                self.assertEqual(parsed.inputs.count('event-query'), 1)

    def test_authored_result_pages_match_their_declared_category(self):
        for category in ('music','comedy','workshop'):
            parsed=Elements(self.app.page('search-'+category))
            expected=[e for e in self.app.events if e['category']==category]
            self.assertEqual(len(parsed.cards), len(expected))
            self.assertEqual({card['data-category'] for card in parsed.cards}, {category})
        self.assertEqual(Elements(self.app.page('search-empty')).cards, [])

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

    def test_native_navigation_marks_only_its_actual_current_destination(self):
        for route in set(self.app.routes) | set(self.app.by_id):
            with self.subTest(route=route):
                header = self.app.partial('header', self.app.context(route))
                links = Elements(header).navigation
                secondary = 'submit.html' if route in ('saved','help','submit') else 'sunshine-theater.html'
                self.assertEqual([link['href'] for link in links], ['index.html',secondary,'saved.html'])
                self.assertIn('<ul class="tide-site-header__links">', header)
                self.assertEqual([link['href'] for link in links if link.get('aria-current')=='page'],
                                 [link['href'] for link in links if link['href']==route+'.html'])
                self.assertFalse(any('hidden' in link or 'role' in link or 'target' in link for link in links))


if __name__=='__main__':
    unittest.main()
