"""Build-time authored kit examples. No app data, routing or browser behavior."""
from datetime import date,time
from html import escape
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
WEEKDAYS=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']


def template(name,values):
    source=(ROOT/'templates'/name).read_text(encoding='utf-8')
    for key,value in values.items():source=source.replace('{{'+key+'}}',str(value))
    missing=set(re.findall(r'\{\{([A-Z_]+)\}\}',source))-{'FRAMES'}
    if missing:raise ValueError('Unresolved listing template fields: '+', '.join(sorted(missing)))
    return source


def date_block(key,iso):
    d=date.fromisoformat(iso)
    return template('listing-date.html',{'DATE_CASE':escape(key,quote=True),'DATE_ISO':d.isoformat(),
        'DATE_LABEL':f'{WEEKDAYS[d.weekday()]}, {MONTHS[d.month-1]} {d.day}, {d.year}',
        'DATE_DAY':d.day,'DATE_WEEKDAY':WEEKDAYS[d.weekday()][:3],'DATE_MONTH':MONTHS[d.month-1][:3]})


def card(key,level,*,selected=False,status='Sample',tone='',action=False,hidden=False,
         available=True,iso='2026-10-24',title='Printmaking evening',venue='Sample print studio',
         price='$32',start='18:00',clock='6:00 PM'):
    if not re.fullmatch(r'[a-z][a-z0-9-]*',key) or not 1<=level<=6 or tone not in {'','success','warning','danger'}:
        raise ValueError('Invalid authored card key, heading or badge tone')
    iso=date.fromisoformat(iso).isoformat() if iso else None
    start=time.fromisoformat(start).isoformat() if start else None
    card_id='listing-'+key
    link=(f'<a class="tide-event-card__link" id="{card_id}-link" href="#listing-detail-target" aria-label="'
          +escape('Open '+title+' detail example',quote=True)+'"></a>') if available else ''
    badge=('<span class="tide-badge'+(' tide-badge--'+tone if tone else '')+' tide-event-card__status">'
           +escape('In view' if selected else status)+'</span>') if status or selected else ''
    icon=(ROOT/'assets/icons/BookmarkIcon.svg').read_text(encoding='utf-8')
    icon=re.sub(r'<svg\b','<svg class="tide-icon"',icon,count=1)
    separate=(f'<a class="tide-icon-button tide-event-card__save" id="{card_id}-action" href="#listing-saved-target" aria-label="Open saved-page example for '
              +escape(title,quote=True)+'">'+icon+'</a>') if action else ''
    return template('listing-card.html',{'CARD_ID':card_id,'CARD_CASE':key,'CARD_LEVEL':level,
        'CARD_MODIFIER':' tide-event-card--in-view' if selected else '', 'CARD_HIDDEN':' hidden' if hidden else '',
        'CARD_LINK':link,'CARD_STATUS':badge,'CARD_ACTION':separate,'CARD_CATEGORY':'Workshop',
        'CARD_TITLE':escape(title),'CARD_VENUE':escape(venue),'CARD_PRICE':escape(price),
        'CARD_DATE':date_block('date-'+key,iso) if iso else '<span>Date to be confirmed</span>',
        'CARD_TIME':f'<time datetime="{iso}T{escape(start,quote=True)}">{escape(clock)}</time>' if start and iso else '<span>'+escape(clock if start else 'Time to be confirmed')+'</span>'})


def listings(level):
    cards=[card('base',level+2),card('selected',level+2,selected=True),
        card('cancelled',level+2,status='Cancelled',tone='danger'),
        card('sold-out',level+2,status='Sold out',price='Free'),
        card('changed',level+2,status='Time changed',tone='warning',start='19:00',clock='7:00 PM'),
        card('long',level+2,title='A long evening of small editions, conversation and printmaking',
             venue='Sample studio and community workshop · venue-reference-abcdefghijklmnopqrstuvwxyz-0123456789',price='Suggested donation · pay what you can'),
        card('unknown',level+2,iso=None,start=None,status='Schedule pending',price='Admission to be confirmed'),
        card('unavailable',level+2,available=False,status='Details unavailable'),
        card('action',level+2,action=True,status='')]
    return template('listings.html',{'LISTING_LEVEL':level,'LISTING_SUBLEVEL':level+1,'LISTING_ITEM_LEVEL':level+2,
        'LISTING_CARDS':'\n'.join('<div>'+c+'</div>' for c in cards),'LISTING_DATES':'\n'.join(date_block(k,d) for k,d in
            [('single','2026-11-07'),('double','2026-10-24'),('year-end','2026-12-31'),('new-year','2027-01-01')]),
        'LISTING_OCTOBER_CARDS':card('calendar-first',level+3)+card('calendar-hidden',level+3,hidden=True)+card('calendar-second',level+3,selected=True),
        'LISTING_NOVEMBER_CARD':card('calendar-november',level+3,iso='2026-11-01'),
        'LISTING_STATIC_CARD':card('calendar-static',level+3,iso='2026-11-07'),
        'LISTING_CONTEXT_CARD':card('context-card',level+2),'LISTING_CONTEXT_DATE':date_block('context-date','2026-10-24'),
        'LISTING_CONTEXT_GROUP_CARD':card('context-group-card',level+3)})
