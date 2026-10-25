"""Validated fixture data and calendar grouping, independent of presentation."""
from datetime import datetime
from itertools import groupby
import json


def load_events(path):
    events=json.loads(path.read_text(encoding='utf-8'))
    slugs=set()
    for event in events:
        if event['slug'] in slugs:raise ValueError('Duplicate event slug: '+event['slug'])
        slugs.add(event['slug'])
        stamp=datetime.fromisoformat(event['datetime'])
        if stamp.tzinfo is None or stamp.date().isoformat()!=event['date'] or stamp.strftime('%H:%M')!=event['start']:
            raise ValueError('Inconsistent local event time: '+event['slug'])
        if not event['title'].strip() or not event['lead'].strip():raise ValueError('Event copy is incomplete')
    return sorted(events,key=lambda x:(x['date'],x['start'],x['slug']))


def month_groups(events):
    return [(key,list(group)) for key,group in groupby(events,key=lambda x:x['date'][:7])]
