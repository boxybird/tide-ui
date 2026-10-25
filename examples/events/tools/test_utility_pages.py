"""Native document, utility-page and submission-field regression contracts."""
from copy import deepcopy
from html.parser import HTMLParser
import unittest

from html_templates import AppTemplates, ROOT


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.nodes=[]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


class UtilityContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=AppTemplates()

    def test_script_order_and_session_profiles_remain_route_specific(self):
        common=['search-core', 'app-runtime', 'event-search', 'event-navigation', 'headings', 'filters', 'rail', 'preview']
        for route in ['index', 'search', 'sunshine-theater', 'saved', 'help', 'submit', 'ink-after-dark']:
            with self.subTest(route=route):
                doc=Document(self.app.page(route))
                scoped=route in ('index', 'search', 'sunshine-theater', 'ink-after-dark')
                scripts=common[:2]+(['venue-context'] if scoped else [])+common[2:]
                self.assertEqual([attrs['src'] for tag,attrs in doc.nodes if tag=='script'], ['js/'+name+'.js' for name in scripts])
                self.assertTrue(all('defer' in attrs for tag,attrs in doc.nodes if tag=='script'))
                body=next(attrs for tag,attrs in doc.nodes if tag=='body')
                self.assertEqual(body['data-state-key'], 'app-release-1.1.0' if scoped else 'margin-aligned')
                self.assertEqual(body.get('data-venue-scope'), 'sunshine-theater' if route=='sunshine-theater' else None)

    def test_saved_and_content_pages_do_not_gain_filter_controls(self):
        for route in ('saved', 'help', 'submit'):
            with self.subTest(route=route):
                nodes=Document(self.app.page(route)).nodes
                self.assertFalse(any(tag=='dialog' or attrs.get('id')=='event-search-form' for tag,attrs in nodes))
                footer_count=sum(attrs.get('class')=='tide-app__site-footer' for tag,attrs in nodes)
                self.assertEqual(footer_count, 0 if route=='help' else 1)
        self.assertEqual({p.name for p in (ROOT/'src/pages').glob('*.html')}, {'sunshine-theater.html', 'help.html', 'submit.html'})

    def test_skip_link_targets_keep_native_ids_and_route_labels(self):
        cases={
            'help':['#main-content'], 'submit':['#main-content'],
            'sunshine-theater':['#results', '#venue-information'],
            'index':['#results', '#event-detail'], 'saved':['#results', '#event-detail'],
            'ink-after-dark':['#event-detail'],
        }
        for route,targets in cases.items():
            with self.subTest(route=route):
                doc=Document(self.app.page(route))
                skips=[attrs['href'] for tag,attrs in doc.nodes if 'tide-app__skip' in attrs.get('class','').split()]
                ids={attrs['id'] for tag,attrs in doc.nodes if attrs.get('id')}
                self.assertEqual(skips, targets)
                self.assertTrue(all(target[1:] in ids for target in targets))

    def test_submission_fields_keep_native_validation_and_hint_associations(self):
        doc=Document(self.app.page('submit'))
        nodes={attrs['id']:(tag,attrs) for tag,attrs in doc.nodes if attrs.get('id')}
        labels=[attrs.get('for') for tag,attrs in doc.nodes if tag=='label']
        self.assertEqual(len(self.app.submission_fields), 11)
        for field in self.app.submission_fields.values():
            with self.subTest(field=field['id']):
                tag,attrs=nodes[field['id']]
                self.assertEqual(labels.count(field['id']), 1)
                self.assertEqual(tag, field['control'])
                self.assertEqual('required' in attrs, field.get('required',False))
                if field.get('hint'):
                    self.assertEqual(attrs['aria-describedby'], field['id']+'-hint')
                    self.assertIn(attrs['aria-describedby'], nodes)
        self.assertEqual(nodes['event-name'][1]['maxlength'], '80')
        self.assertEqual(nodes['email'][1]['type'], 'email')
        self.assertEqual(nodes['email'][1]['autocomplete'], 'email')
        self.assertEqual(nodes['address'][1]['autocomplete'], 'street-address')
        self.assertEqual(nodes['photo'][1]['accept'], 'image/jpeg,image/png,image/webp')
        self.assertFalse(any(tag=='button' and attrs.get('type')=='submit' for tag,attrs in doc.nodes))

    def test_field_and_option_copy_is_escaped_without_executing_tokens(self):
        field=deepcopy(self.app.submission_fields['event-category'])
        field['label']='<script>example</script>'
        field['hint']='{{> missing}} & "example"'
        field['options'][0]={'label':'<img src=x>', 'value':'" onfocus="example'}
        source=self.app.fields.render(field)
        self.assertNotIn('<script>', source)
        self.assertNotIn('<img', source)
        self.assertIn('{{&gt; missing}}',source)
        option=next(attrs for tag,attrs in Document(source).nodes if tag=='option')
        self.assertEqual(option, {'value':field['options'][0]['value']})

    def test_arbitrary_field_markup_and_invalid_controls_are_rejected(self):
        for mutation in ({'onclick':'example'}, {'control':'script'}, {'type':'file'}, {'id':'../other'}, {'optional':True}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                field={**self.app.submission_fields['event-name'], **mutation}
                self.app.fields.render(field)

    def test_venue_and_help_content_retain_their_semantic_landmarks(self):
        venue=Document(self.app.page('sunshine-theater'))
        self.assertEqual(sum(attrs.get('id')=='venue-information' for tag,attrs in venue.nodes),1)
        self.assertTrue(any(attrs.get('href')=='tel:+15057640249' for tag,attrs in venue.nodes))
        self.assertTrue(any(attrs.get('href')=='https://sunshinetheaterlive.com/' for tag,attrs in venue.nodes))
        help_doc=Document(self.app.page('help'))
        self.assertTrue(any(tag=='article' and attrs.get('class')=='tide-prose' for tag,attrs in help_doc.nodes))
        self.assertTrue(any(attrs.get('id')=='admission-caption' for tag,attrs in help_doc.nodes))
        self.assertTrue(any(tag=='th' and attrs.get('scope')=='row' for tag,attrs in help_doc.nodes))

    def test_document_title_is_escaped(self):
        title=self.app.routes['help']['documentTitle']
        try:
            self.app.routes['help']['documentTitle']='</title><script>example</script>'
            source=self.app.page('help')
            self.assertIn('&lt;/title&gt;&lt;script&gt;',source)
            self.assertNotIn('<script>example',source)
        finally:
            self.app.routes['help']['documentTitle']=title


if __name__=='__main__':
    unittest.main()
