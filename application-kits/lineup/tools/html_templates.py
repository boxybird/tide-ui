"""Build-time app composition. No browser templating, framework or kit writes.

Only {{UPPERCASE_VALUE}} and {{> registered-partial}} are supported. Plain
values are HTML-escaped; Html is reserved for markup composed by this module.
"""
from collections import defaultdict
from datetime import date, datetime
import json
from pathlib import Path
import re
from template_engine import Html, expand, attribute
from event_details import EventDetails
from form_fields import FormFields

ROOT = Path(__file__).resolve().parents[1]
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


class AppTemplates:
    def __init__(self):
        manifest = json.loads((ROOT/'consumer-manifest.json').read_text(encoding='utf-8'))
        sources = [ROOT/name for name in manifest['templateHome']]
        if set(sources) != set((ROOT/'src/templates').glob('*.html')):
            raise ValueError('Register every app partial in consumer-manifest.json')
        self.templates = {p.stem:p.read_text(encoding='utf-8').removesuffix('\n') for p in sources}
        if len(self.templates) != len(sources):
            raise ValueError('App partial names must be unique')
        self.events = json.loads((ROOT/manifest['dataHome']['events']).read_text(encoding='utf-8'))
        self.detail_presentations = json.loads((ROOT/manifest['dataHome']['detailPresentations']).read_text(encoding='utf-8'))
        self.details = EventDetails(self.partial, self.detail_presentations)
        self.routes = json.loads((ROOT/manifest['dataHome']['routes']).read_text(encoding='utf-8'))
        self.submission_fields = json.loads((ROOT/manifest['dataHome']['submissionFields']).read_text(encoding='utf-8'))
        self.fields = FormFields(self.partial)
        self.by_id = {event['id']:event for event in self.events}
        if len(self.by_id) != len(self.events):
            raise ValueError('Sample event IDs must be unique')
        for event in self.events:
            for key in ('id', 'venue'):
                if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', event[key]):
                    raise ValueError('Invalid sample ' + key)
            if event['category'] not in ('music', 'comedy', 'workshop'):
                raise ValueError('Unknown sample category')
            date.fromisoformat(event['date'])
            if event.get('start'):
                datetime.fromisoformat(event['start'])
            if event.get('endDate'):
                date.fromisoformat(event['endDate'])
        for page in self.routes.values():
            if page['layout'] not in ('workspace', 'content'):
                raise ValueError('Unsupported app page layout')
            if page.get('source') and not re.fullmatch(r'[a-z]+(?:-[a-z]+)*\.html', page['source']):
                raise ValueError('Invalid app content source')
            if page['layout']=='content' and not page.get('source'):
                raise ValueError('Content pages need an explicit source')
            if page.get('collection')=='venue':
                owner = self.routes.get(page.get('venue'), {})
                if owner.get('collection')!='venue' or page.get('source')!=owner.get('source'):
                    raise ValueError('Venue results must retain their venue owner and information source')
                links = owner.get('resultRoutes', {})
                if set(links)!={'all','music','comedy','workshop','empty'}:
                    raise ValueError('Register every venue result-state destination')
                for target in links.values():
                    destination = self.routes.get(target, {})
                    if destination.get('collection')!='venue' or destination.get('venue')!=page['venue']:
                        raise ValueError('Venue result-state links must remain in the same venue')
                # This authored venue has only music samples, so All and Music
                # intentionally share one truthful document, not a duplicate.
                if links['music']==links['all'] and any(event['category']!='music' for event in self.events if event['venue']==page['venue']):
                    raise ValueError('A shared All/Music venue page requires only music samples')
        actual = {p.name for p in (ROOT/'src/pages').glob('*.html')}
        if actual != {page['source'] for page in self.routes.values() if page.get('source')}:
            raise ValueError('Only registered unique content fragments belong in src/pages')
        field_tokens = re.findall(r'{{(FIELD_[A-Z_]+)}}', (ROOT/'src/pages/submit.html').read_text(encoding='utf-8'))
        expected_tokens = ['FIELD_'+key.replace('-', '_').upper() for key in self.submission_fields]
        if sorted(field_tokens)!=sorted(expected_tokens) or any(key!=field['id'] for key, field in self.submission_fields.items()):
            raise ValueError('Every submission field needs one unique content slot and matching ID')

    def partial(self, name, values):
        return Html(expand('{{> ' + name + '}}', values, self.templates))

    def card(self, event, selected, saved=False):
        day = date.fromisoformat(event['date'])
        values = {
            'ID':event['id'], 'TITLE':event['title'], 'CATEGORY':event['category'],
            'CATEGORY_LABEL':event['categoryLabel'], 'VENUE_LABEL':event['venueLabel'],
            'VENUE_ATTRIBUTE':Html('') if saved else attribute('data-venue', event['venue']),
            'DATE':event['date'], 'END_DATE_ATTRIBUTE':attribute('data-end-date', event['endDate']) if event.get('endDate') else Html(''),
            'SEARCH':event['search'], 'DAY':day.day, 'WEEKDAY':WEEKDAYS[day.weekday()][:3], 'MONTH':MONTHS[day.month-1][:3],
            'DATE_LABEL':f'{WEEKDAYS[day.weekday()]}, {MONTHS[day.month-1]} {day.day}, {day.year}',
            'TIME_TAG':'time' if event.get('start') else 'span',
            'TIME_ATTRIBUTE':attribute('datetime', event['start']) if event.get('start') else Html(''),
            'TIME':event['time'], 'PRICE':event['price'],
            'IN_VIEW_CLASS':Html(' tide-event-card--in-view' if event['id']==selected else ''),
            'STATUS_HIDDEN':Html('' if event['id']==selected else ' hidden'),
        }
        return self.partial('event-card', values)

    def context(self, route):
        if route in self.by_id:
            page = {'collection':'all', 'selected':route, 'headingLevel':2}
        elif route in self.routes:
            page = self.routes[route]
        else:
            raise ValueError('Unknown app route: ' + route)
        current = page.get('currentNav')
        secondary = page.get('secondaryNav', 'venue')
        values = {
            'FIND_CURRENT':attribute('aria-current', 'page') if current=='find' else Html(''),
            'SECONDARY_CURRENT':attribute('aria-current', 'page') if current=='secondary' else Html(''),
            'SAVED_CURRENT':attribute('aria-current', 'page') if current=='saved' else Html(''),
            'SECONDARY_HREF':'sunshine-theater.html' if secondary=='venue' else 'submit.html',
            'SECONDARY_LABEL':'Sunshine Theater' if secondary=='venue' else 'Add an event',
            **{name:Html('{{'+name+'}}') for name in ('KIT_CSS','APP_CSS','KIT_ASSETS')},
        }
        collection = page.get('collection')
        values['FILTER_TRIGGER'] = self.partial('filter-trigger', {}) if collection and collection!='saved' else Html('')
        if collection is None:
            return values
        saved = collection=='saved'
        venue = collection=='venue'
        venue_id = page.get('venue') if venue else None
        venue_owner = self.routes[venue_id] if venue else {}
        result_routes = venue_owner['resultRoutes'] if venue else {'all':'search','music':'search-music','comedy':'search-comedy','workshop':'search-workshop','empty':'search-empty'}
        collection_href = venue_id+'.html' if venue else 'index.html'
        events = [event for event in self.events if (not venue or event['venue']==venue_id) and (not saved or event['id']=='ink-after-dark')]
        venue_total = len(events) if venue else 0
        sample = page.get('sampleFilter', {})
        if set(sample)-{'category','empty'} or sample.get('category') not in (None,'music','comedy','workshop'):
            raise ValueError('Unsupported authored result state')
        if sample.get('category'):
            events = [event for event in events if event['category']==sample['category']]
        if sample.get('empty'):
            events = []
        selected = page.get('selected', '')
        if selected and selected not in {event['id'] for event in events}:
            selected = ''
        groups = defaultdict(list)
        for event in events:
            groups[event['date'][:7]].append(event)
        group_html = []
        for month, entries in groups.items():
            day = date.fromisoformat(month+'-01')
            jumps = Html(''.join(self.partial('month-jump', {'MONTH_ID':key, 'MONTH_LABEL':MONTHS[int(key[5:])-1]+' '+key[:4], 'MONTH_SHORT':MONTHS[int(key[5:])-1][:3]}) for key in groups))
            group_html.append(self.partial('month-group', {
                'MONTH_ID':month, 'MONTH_NAME':MONTHS[day.month-1], 'MONTH_YEAR':day.year, 'MONTH_LABEL':MONTHS[day.month-1]+' '+str(day.year),
                'MONTH_COUNT':str(len(entries))+' '+('event' if len(entries)==1 else 'events'),
                'MONTH_NAV':self.partial('month-nav', {'MONTH_JUMPS':jumps}) if len(groups)>1 else Html(''),
                'EVENT_CARDS':Html(''.join(self.card(event, selected, saved) for event in entries)),
            }))
        values.update({
            'INTRO_LABEL':'Saved' if saved else 'Albuquerque',
            'INTRO_TITLE':'For another evening.' if saved else 'Sunshine Theater' if venue else 'Coming up.',
            'INTRO_COPY':'Your shortlist, all in one place.' if saved else '120 Central Ave SW · Downtown Albuquerque' if venue else 'Good things happening close to home.',
            'INTRO_LINKS':self.partial('scope-link', {'LINK_HREF':'#venue-information', 'LINK_LABEL':'About this venue'}) if venue else Html(''),
            'HEADING_LEVEL':page.get('headingLevel', 1), 'EVENT_COUNT':len(events),
            'COUNT_LABEL':str(len(events))+' '+('event' if len(events)==1 else 'events'),
            'SEARCH_ACTION':collection_href if venue else 'search.html',
            'VENUE_SCOPE':venue_id if venue else '',
            'RESULT_NOTE':f'Venue control examples. All {venue_total} venue samples are music.' if venue else 'Control examples. Browse sample result pages:',
            'RESULT_NAV_LABEL':'Sunshine Theater sample result states' if venue else 'Authored result states',
            **{'RESULT_'+kind.upper()+'_HREF':target+'.html' for kind,target in result_routes.items()},
            'COLLECTION_HREF':collection_href,
            'COLLECTION_LABEL':'All venue events' if venue else 'All events',
            'RESULTS_ACTION_LABEL':'View all venue samples' if venue else 'View all sample results',
            'RESET_TAG':'a' if venue else 'button',
            'RESET_ATTRIBUTES':attribute('href', collection_href) if venue else Html(attribute('type','reset')+attribute('form','event-search-form')),
            'SCOPE_EXIT':self.partial('scope-link', {'LINK_HREF':'index.html', 'LINK_LABEL':'All events across Albuquerque'}) if venue else Html(''),
            'SUMMARY_KICKER':Html('') if saved else self.partial('summary-kicker', {'KICKER':'Sunshine Theater' if venue else 'The lineup'}),
            'SUMMARY_BADGE':Html('') if saved else self.partial('summary-badge', {}),
            'SUMMARY_TOGGLE':Html(''),
            'EMPTY_HIDDEN':Html(' hidden' if events else ''),
            'EMPTY_TITLE':f"No {sample.get('category', 'matching')} sample events at Sunshine Theater." if venue else 'No events found.',
            'EMPTY_COPY':f'Browse all {venue_total} venue samples or read the venue information below.' if venue else 'This authored specimen shows an empty result state. Browse another sample result page.',
            'EMPTY_RECOVERY_HREF':collection_href+'#results' if venue else 'index.html',
            'EMPTY_RECOVERY_LABEL':'Show all venue events' if venue else 'Clear search and filters',
            'PREVIEW_HIDDEN':Html(' hidden' if events or venue else ''),
            'MUSIC_CHECKED':Html(' checked' if sample.get('category')=='music' else ''),
            'COMEDY_CHECKED':Html(' checked' if sample.get('category')=='comedy' else ''),
            'WORKSHOP_CHECKED':Html(' checked' if sample.get('category')=='workshop' else ''),
            'EVENT_DETAIL':Html(''),
            'ORDER_LABEL':'Sample schedule · Soonest first' if venue else 'Soonest first',
            'FEED_CLASS':'tide-event-list' if saved else 'tide-event-list tide-lineup__feed',
            'FEED_ID':Html('') if saved else attribute('id', 'venue-feed'),
            'MONTH_GROUPS':Html(''.join(group_html)),
            'FOOTER_HREF':'submit.html' if saved else '#venue-information' if venue else 'sunshine-theater.html',
            'FOOTER_LINK':'Have something happening? Add an event.' if saved else 'About Sunshine Theater' if venue else 'Explore Sunshine Theater and its upcoming sample events.',
            'FOOTER_BACK_HIDDEN':Html('') if saved or venue else Html(' hidden'),
            'FOOTER_BACK_LABEL':'All events across Albuquerque' if venue else 'Back to all events',
            'FOOTER_NOTE':'Saved items are an example shortlist.' if saved else 'End of the sample feed. Fictional events for UX testing. Venue information is sourced separately.',
        })
        if selected and not venue:
            event = self.by_id[selected]
            values['EVENT_DETAIL'] = self.details.render(event, 1 if route in self.by_id else 2)
            values['DOCUMENT_TITLE'] = event['detail']['documentTitle']
        return values

    def document_context(self, route, page, event):
        collection = page.get('collection')
        venue = collection=='venue'
        saved = collection=='saved'
        if event:
            skips = [('event-detail', 'Skip to event', '')]
        elif collection:
            detail_target = 'venue-information' if venue else 'preview-state' if page.get('sampleFilter',{}).get('empty') else 'event-detail'
            detail_label = 'Skip to venue details' if venue else 'Skip to event preview'
            skips = [('results', 'Skip to results', ''), (detail_target, detail_label, ' tide-app__skip--detail')]
        else:
            skips = [('main-content', 'Skip to content', '')]
        state_key = 'margin-aligned' if saved or not collection else 'app-release-1.1.0'
        body_class = 'tide-app--venue tide tide-app' if venue else 'tide tide-app tide-app--event' if event else 'tide tide-app'
        if collection and not saved:
            body_class += ' tide-app--columns'
        body_attributes = str(attribute('data-venue-scope', 'sunshine-theater')) if venue else ''
        body_attributes += attribute('data-state-key', state_key)+attribute('class', body_class)
        return {
            'BODY_ATTRIBUTES':Html(body_attributes),
            'VENUE_SCRIPT':Html(''),
            'SKIP_LINKS':Html(''.join(self.partial('skip-link', {'SKIP_TARGET':target, 'SKIP_LABEL':label, 'SKIP_MODIFIER':Html(modifier)}) for target, label, modifier in skips)),
            'SITE_FOOTER':Html('') if route=='help' else self.partial('site-footer', {}),
            'FILTER_DIALOG':Html(''),
        }

    def page(self, source):
        route = Path(source).stem
        values = self.context(route)
        event = route in self.by_id
        page = {'layout':'workspace', 'collection':'all'} if event else self.routes[route]
        collection = page.get('collection')
        saved = collection=='saved'
        if not event:
            values['DOCUMENT_TITLE'] = page['documentTitle']
        if route=='submit':
            values.update({'FIELD_'+key.replace('-', '_').upper():self.fields.render(field) for key, field in self.submission_fields.items()})
            values['SUBMISSION_BACK_ICON'] = self.partial('detail-icon-back', {'ICON_EXTRA':Html(' fill="none" xmlns="http://www.w3.org/2000/svg"')})
        content = Html(expand((ROOT/'src/pages'/page['source']).read_text(encoding='utf-8'), values, self.templates)) if page.get('source') else values['EVENT_DETAIL']
        if page['layout']=='workspace':
            results = self.partial('workspace-results', {
                **values, 'RESULTS_INTRO':self.partial('results-intro', values) if saved else Html(''),
            })
            content = self.partial('workspace', {
                **values, 'WORKSPACE_DETAIL':content,
                'WORKSPACE_BROWSE':results if saved else self.partial('workspace-browse', {**values, 'WORKSPACE_RESULTS':results}),
            })
        return self.partial('document', {**values, **self.document_context(route, page, event), 'PAGE_CONTENT':content})

    def pages(self):
        return {route+'.html':self.page(route) for route in sorted(set(self.by_id) | set(self.routes))}
