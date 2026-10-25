"""Build-time app composition. No browser templating, framework or kit writes.

Only {{UPPERCASE_VALUE}} and {{> registered-partial}} are supported. Plain
values are HTML-escaped; Html is reserved for markup composed by this module.
"""
from collections import defaultdict
from datetime import date, datetime
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'{{\s*(?:>\s*([a-z][a-z0-9-]*)|([A-Z][A-Z0-9_]*))\s*}}')
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


class Html(str):
    """Explicit, trusted composition output; never use for sample text values."""


def expand(text, values, templates, stack=()):
    literal = TOKEN.sub('', text)
    if '{{' in literal or '}}' in literal:
        raise ValueError('Malformed app template token')
    def replace(match):
        partial, key = match.groups()
        if partial:
            if partial not in templates:
                raise ValueError('Unknown app partial: ' + partial)
            if partial in stack:
                raise ValueError('Cyclic app partial: ' + ' -> '.join((*stack, partial)))
            return expand(templates[partial], values, templates, (*stack, partial))
        if key not in values:
            raise ValueError('Unknown app template value: ' + key)
        value = values[key]
        return str(value) if isinstance(value, Html) else escape(str(value), quote=True)
    # Substitute once: sample text that resembles a token remains ordinary text.
    return TOKEN.sub(replace, text)


def attribute(name, value):
    return Html(' ' + name + '="' + escape(str(value), quote=True) + '"')


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
        self.routes = json.loads((ROOT/manifest['dataHome']['routes']).read_text(encoding='utf-8'))
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
        actual = {p.stem for p in (ROOT/'src/pages').glob('*.html')}
        if actual != set(self.by_id) | set(self.routes):
            raise ValueError('Every source page needs an event or explicit route context')

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
        if collection is None:
            return values
        saved = collection=='saved'
        venue = collection=='venue'
        events = [event for event in self.events if (not venue or event['venue']=='sunshine-theater') and (not saved or event['id']=='ink-after-dark')]
        selected = page.get('selected', '')
        groups = defaultdict(list)
        for event in events:
            groups[event['date'][:7]].append(event)
        group_html = []
        for month, entries in groups.items():
            day = date.fromisoformat(month+'-01')
            jumps = Html(''.join(self.partial('month-jump', {'MONTH_ID':key, 'MONTH_LABEL':MONTHS[int(key[5:])-1]+' '+key[:4], 'MONTH_SHORT':MONTHS[int(key[5:])-1][:3]}) for key in groups))
            group_html.append(self.partial('month-group', {
                'MONTH_ID':month, 'MONTH_LABEL':MONTHS[day.month-1]+' '+str(day.year),
                'MONTH_COUNT':str(len(entries))+' '+('event' if len(entries)==1 else 'events'),
                'MONTH_NAV':self.partial('month-nav', {'MONTH_JUMPS':jumps}) if len(groups)>1 else Html(''),
                'EVENT_CARDS':Html(''.join(self.card(event, selected, saved) for event in entries)),
            }))
        values.update({
            'INTRO_LABEL':'Saved' if saved else 'Albuquerque',
            'INTRO_TITLE':'For another evening.' if saved else 'Sunshine Theater' if venue else 'Coming up.',
            'INTRO_COPY':'Your shortlist, all in one place.' if saved else '120 Central Ave SW · Downtown Albuquerque' if venue else 'Good things happening close to home.',
            'HEADING_LEVEL':page.get('headingLevel', 1), 'EVENT_COUNT':len(events),
            'COUNT_LABEL':str(len(events))+' '+('event' if len(events)==1 else 'events'),
            'SEARCH_ACTION':'sunshine-theater.html' if venue else 'search.html',
            'VENUE_SCOPE':'sunshine-theater' if venue else '',
            'SUMMARY_KICKER':Html('') if saved else self.partial('summary-kicker', {'KICKER':'Sunshine Theater' if venue else 'The lineup'}),
            'SUMMARY_BADGE':Html('') if saved else self.partial('summary-badge', {}),
            'SUMMARY_TOGGLE':Html('') if saved else self.partial('summary-toggle', {}),
            'ORDER_LABEL':'Sample schedule · Soonest first' if venue else 'Soonest first',
            'FEED_CLASS':'tide-event-list' if saved else 'tide-event-list tide-lineup__feed',
            'FEED_ID':Html('') if saved else attribute('id', 'venue-feed'),
            'MONTH_GROUPS':Html(''.join(group_html)),
            'FOOTER_HREF':'submit.html' if saved else 'sunshine-theater.html',
            'FOOTER_LINK':'Have something happening? Add an event.' if saved else 'Explore Sunshine Theater and its upcoming sample events.',
            'FOOTER_BACK_HIDDEN':Html('') if saved else Html(' hidden'),
            'FOOTER_NOTE':'Saved items are an example shortlist.' if saved else 'End of the sample feed. Fictional events for UX testing. Venue information is sourced separately.',
        })
        return values

    def page(self, source):
        text = source.read_text(encoding='utf-8')
        return expand(text, self.context(source.stem), self.templates)
