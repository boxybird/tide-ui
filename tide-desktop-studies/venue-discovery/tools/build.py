"""Separate venue discovery copy. Frozen app, kit and earlier study are read-only."""
from pathlib import Path
from html import escape
import importlib.util
import json
import re
import shutil
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'shared-filter-release'
APP=ROOT/'app'
CHECK='--check' in sys.argv
spec=importlib.util.spec_from_file_location('venue_markup_helpers',ROOT.parent/'event-pressure-test/tools/build.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
EVENTS=json.loads((ROOT/'data/events.json').read_text(encoding='utf-8'))
for e in EVENTS:e.update(category='music',venue='Sunshine Theater',venueId='sunshine-theater',endDate=e['date'],photo='concert',action='Event information')
ORIGINAL=json.loads((ROOT.parent.parent/'tide-responsive-app/data/events.json').read_text(encoding='utf-8'))
STARTS={e['slug']:e['start'] for e in ORIGINAL}
STARTS.update({e['id']:e['start'][11:16] for e in EVENTS})
VENUES={e['slug']:re.sub(r'[^a-z0-9]+','-',e['venue'].lower()).strip('-') for e in ORIGINAL}

def write(path,text):
    if CHECK:assert path.exists() and path.read_text(encoding='utf-8')==text,'Stale output: '+str(path)
    else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8',newline='\n')

def card_id(card):return re.search(r'class="tide-event-card__link" href="([^"?]+)',card).group(1).removesuffix('.html')

template=(BASE/'app/index.html').read_text(encoding='utf-8')
OLD_CARDS=re.findall(r'<article class="tide-event-card\b.*?</article>',template,re.S)
assert len(OLD_CARDS)==48
CARDS=[c.replace('data-date=',f'data-venue="{VENUES[card_id(c)]}" data-date=',1) for c in OLD_CARDS]
CARDS += [helper.card(e,'').replace(' tide-pressure__card-heading','').replace('data-date=','data-venue="sunshine-theater" data-date=',1) for e in EVENTS]

def feed(selected='',venue=False):
    out='<div class="tide-event-list tide-venue-study__feed" id="venue-feed">'
    months=[('2026-10','October'),('2026-11','November')]
    for month,label in months:
        cards=[c for c in CARDS if f'data-date="{month}' in c and (not venue or 'data-venue="sunshine-theater"' in c)]
        cards.sort(key=lambda c:(re.search(r'data-date="([^"]+)',c).group(1),STARTS[card_id(c)]))
        nav=''.join(f'<a class="tide-event-group__jump" href="#month-{m}" aria-label="Jump to {name} 2026">{name[:3]}</a>' for m,name in months)
        out+=f'<section class="tide-event-group tide-event-group--sticky" id="month-{month}" aria-labelledby="month-title-{month}" tabindex="-1"><header class="tide-event-group__header tide-feed-study__month-header tide-slide-study__month-header"><h3 class="tide-event-group__title tide-feed-study__month-title" id="month-title-{month}" tabindex="-1">{label} 2026 <span class="tide-event-group__count tide-feed-study__month-count">{len(cards)} events</span></h3><nav class="tide-event-group__nav tide-feed-study__month-nav" aria-label="Jump to month">{nav}</nav></header>'
        for card in cards:
            chosen=card_id(card)==selected
            card=re.sub(r'class="tide-event-card(?: tide-event-card--in-view)?"','class="tide-event-card'+(' tide-event-card--in-view' if chosen else '')+'"',card,1)
            card=re.sub(r'(<span class="tide-badge tide-event-card__status")(?: hidden)?(>In view</span>)',r'\1'+('' if chosen else ' hidden')+r'\2',card)
            out+=card
        out+='</section>'
    return out+'</div>'

def event_detail(e,level):
    text=helper.detail(e,level)
    text=text.replace('<dd>Sunshine Theater</dd>','<dd><a class="tide-link" href="sunshine-theater.html">Sunshine Theater</a></dd>')
    venue=f'<section class="tide-event-details__section"><h{level+2} class="tide-event-details__section-title" id="venue-information">At Sunshine Theater</h{level+2}><p class="tide-place">120 Central Ave SW<br>Albuquerque, NM 87102</p><p>Downtown, near Central and Second. Explore the venue and its upcoming sample schedule.</p><a class="tide-button tide-button--secondary" href="sunshine-theater.html">More events at Sunshine Theater</a></section>'
    venue=venue.replace('id="venue-information"','id="venue-information" tabindex="-1"')
    text=text.replace('<p class="tide-disclosure">',venue+'<p class="tide-disclosure">',1)
    text=text.replace('An authored pressure-test event. Details, availability and photographs are illustrative.','Sample event, not an actual Sunshine Theater listing. Concert photograph is illustrative and does not depict this venue.')
    return text

def venue_profile():
    return '''<section class="tide-app__detail tide-study__detail tide-slide-study__detail tide-room-study__detail tide-venue-study__profile" id="event-detail" aria-labelledby="venue-info-title" tabindex="-1"><article class="tide-venue-study__information tide-venue-study__visit" id="venue-information"><header><p class="tide-eyebrow">The venue</p><h2 class="tide-page-intro__title" id="venue-info-title">Know the room.</h2><p>A downtown live-music venue in the historic Sunshine Building, near Central and Second.</p></header><dl class="tide-summary"><div><dt>Address</dt><dd>120 Central Ave SW<br>Albuquerque, NM 87102</dd></div><div><dt>Contact</dt><dd><a class="tide-link" href="tel:+15057640249">505-764-0249</a></dd></div><div><dt>Website</dt><dd><a class="tide-link" href="https://sunshinetheaterlive.com/">Official venue website</a></dd></div></dl><div class="tide-row"><a class="tide-button" href="https://www.google.com/maps/search/?api=1&amp;query=Sunshine+Theater+120+Central+Ave+SW+Albuquerque+NM">Get directions</a><a class="tide-button tide-button--secondary" href="https://sunshinetheaterlive.com/page/frequently-asked-questions">Venue FAQs</a></div><section><h3 class="tide-event-details__section-title">Seating &amp; entry</h3><p>Primarily standing-room general admission, with limited seating available first come, first served. The venue does not allow re-entry.</p></section><section><h3 class="tide-event-details__section-title">Access arrangements</h3><p>Contact the venue before your visit about step-free entry, seating and other access needs. Its FAQ directs patrons needing assistance to the manager on arrival; it does not confirm specific access facilities.</p></section><section><h3 class="tide-event-details__section-title">Check each event</h3><p>Age restrictions, admission and doors/show times belong to the individual event. They are not a single venue-wide rule.</p></section><div class="tide-notice"><strong>Sample schedule</strong><p>The six events in this study are authored examples, not Sunshine Theater’s live listings. For actual shows, visit the official venue website.</p></div><footer class="tide-caption"><p>Venue facts checked <time datetime="2026-10-24">October 24, 2026</time>.</p><p><a class="tide-link" href="https://sunshinetheaterlive.com/contact_page">Contact information</a> · <a class="tide-link" href="https://sunshinetheaterlive.com/page/about-sunshine-theater">About the venue</a> · <a class="tide-link" href="https://sunshinetheaterlive.com/page/frequently-asked-questions">Visitor information</a></p></footer></article></section>'''

def page(source,selected='',event=None,index=False,venue=False):
    text=source.replace('../kit/','../../shared-filter-release/kit/')
    if 'id="event-search-form"' not in text:return text
    text=text.replace('data-width="margin-aligned"','data-width="venue-discovery"')
    text=text.replace('data-room="margin-aligned"','data-room="venue-discovery"')
    text=text.replace('class="tide-gutter-study','class="tide-venue-study'+(' tide-venue-study--profile' if venue else '')+' tide-gutter-study',1)
    if venue:text=text.replace('<body ','<body data-venue-scope="sunshine-theater" ',1)
    text=text.replace('<div class="tide-event-list">','<div class="tide-event-list" id="venue-feed">',1)
    text=helper.replace_node(text,'venue-feed',feed(selected,venue))
    text=text.replace('48 events',('6' if venue else '54')+' events').replace('All 48 events','All events')
    text=text.replace('All 48','All 54')
    text=text.replace('action="search.html"','action="sunshine-theater.html"' if venue else 'action="search.html"',1)
    text=text.replace('<label class="tide-app__search-label"',f'<input type="hidden" name="venue" id="venue-scope" value="{"sunshine-theater" if venue else ""}"><label class="tide-app__search-label"',1)
    if event:text=helper.replace_node(text,'event-detail',event_detail(event,2 if index else 1))
    if venue:
        text=helper.replace_node(text,'event-detail',venue_profile().replace('id="venue-information"','id="venue-information" tabindex="-1"'))
        text=text.replace('>Coming up.</h1>','>Sunshine Theater</h1>')
        text=text.replace('Good things happening close to home.','120 Central Ave SW · Downtown Albuquerque')
        text=text.replace('The lineup</p>','Sunshine Theater</p>')
        text=text.replace('Soonest first','Sample schedule · Soonest first')
        text=text.replace('href="#event-detail">Skip to event preview','href="#venue-information">Skip to venue details')
    text=text.replace('href="submit.html">Add an event','href="sunshine-theater.html">Sunshine Theater')
    text=text.replace('Have something happening? Add an event.','Explore Sunshine Theater and its upcoming sample events.').replace('href="submit.html"','href="sunshine-theater.html"')
    text=text.replace('Fictional events for UX testing.','Fictional events for UX testing. Venue information is sourced separately.')
    if venue or event:
        title='Sunshine Theater · Venue & upcoming sample events' if venue else event['title']
        text=re.sub(r'<title>.*?</title>','<title>'+escape(title)+' · Burque</title>',text)
    text=text.replace('<script src="js/event-search.js"','<script src="js/venue-context.js" defer></script>\n<script src="js/event-search.js"',1)
    text=text.replace('</head>','<link rel="stylesheet" href="../css/venue.css">\n</head>')
    return text

def scripts():
    core=(BASE/'app/js/search-core.js').read_text(encoding='utf-8')
    core=core.replace('function read(params) {','function read(params, defaultVenue = \'\') {')
    core=core.replace('q: (params.get',"venue: (params.get('venue') || defaultVenue) === 'sunshine-theater' ? 'sunshine-theater' : '',\n      q: (params.get",1)
    core=core.replace("if (state.q) params.set('q', state.q);","if (state.venue) params.set('venue', state.venue);\n    if (state.q) params.set('q', state.q);")
    core=core.replace('if (!validRange(state)) return false;','if (!validRange(state)) return false;\n    if (state.venue && event.venue !== state.venue) return false;')
    write(APP/'js/search-core.js',core)
    search=(BASE/'app/js/event-search.js').read_text(encoding='utf-8').replace('48 existing','54 existing')
    search=search.replace('TideSearch.read(new URLSearchParams(location.search))',"TideSearch.read(new URLSearchParams(location.search), document.body.dataset.venueScope || '')")
    search=search.replace('if (!active) return;', 'if (!active && !state.venue) return;')
    search=search.replace(": 'Oct 23–Nov 29, 2026';",": state.venue ? 'Oct 30–Nov 27, 2026' : 'Oct 23–Nov 29, 2026';")
    search=search.replace("new URL('search.html', location.href)","new URL(state.venue ? 'sunshine-theater.html' : 'search.html', location.href)")
    search=search.replace("'Back to results'","state.venue ? 'Back to venue' : 'Back to results'")
    search=search.replace('// A real event URL always owns its detail.',"if (document.body.classList.contains('tide-venue-study--profile')) { markPreview(null); return; }\n\n  // A real event URL always owns its detail.")
    write(APP/'js/event-search.js',search)
    filters=(BASE/'app/js/filters.js').read_text(encoding='utf-8')
    filters=filters.replace("intro.classList.add('tide-sr-only');","if(!document.body.classList.contains('tide-venue-study--profile'))intro.classList.add('tide-sr-only');")
    filters=filters.replace("TideSearch.read(new URLSearchParams(location.search))","TideSearch.read(new URLSearchParams(location.search), document.body.dataset.venueScope || '')")
    filters=filters.replace('tide:unified-search:applied','tide:venue-study:applied')
    write(APP/'js/filters.js',filters)

def main():
    for p in (BASE/'app').rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(BASE/'app')
        if rel.as_posix() in ('index.html','search.html'):continue
        if p.suffix=='.html':write(APP/rel,page(p.read_text(encoding='utf-8'),selected=p.stem))
        elif p.suffix in ('.js','.css'):
            if rel.as_posix() not in ('js/event-search.js','js/search-core.js','js/filters.js'):write(APP/rel,p.read_text(encoding='utf-8'))
        elif not CHECK:(APP/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,APP/rel)
    scripts()
    index=(BASE/'app/index.html').read_text(encoding='utf-8')
    event=(BASE/'app/desert-frequencies.html').read_text(encoding='utf-8')
    for e in EVENTS:write(APP/(e['id']+'.html'),page(event,e['id'],event=e))
    for name in ('index.html','search.html'):write(APP/name,page(index,EVENTS[0]['id'],event=EVENTS[0],index=True))
    write(APP/'sunshine-theater.html',page(index,venue=True))
    write(ROOT/'index.html','''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Venue discovery · Burque</title><link rel="stylesheet" href="../shared-filter-release/kit/css/tide.css"><link rel="stylesheet" href="app/css/host.css"><link rel="stylesheet" href="css/venue.css"></head><body class="tide"><main class="tide-venue-study__review tide-stack"><p class="tide-eyebrow">Separate app study · Sunshine Theater</p><h1 class="tide-page-intro__title">A place worth coming back to.</h1><p>Explore an event, its venue, and another evening in the same room. The approved app, UI kit and earlier studies remain untouched.</p><div class="tide-row"><a class="tide-button" href="app/high-desert-signal.html?inspect=1&amp;preview-filters=open">Start with an event</a><a class="tide-button tide-button--secondary" href="app/sunshine-theater.html">Explore Sunshine Theater</a></div><div class="tide-notice"><strong>Real venue details. Authored sample events.</strong><p>Address, contact and visitor information come from the venue’s official pages. The six added shows are fictional examples for testing the interface.</p></div><ol><li>Open High Desert Signal and select the linked Sunshine Theater name or More events at Sunshine Theater.</li><li>Browse the venue’s six upcoming samples alongside practical venue information.</li><li>Choose another show; the list stays scoped to Sunshine Theater. Reset clears your refinements while retaining the venue.</li></ol><p><a class="tide-link" href="app/sunday-in-stereo.html?venue=sunshine-theater">Open a show in venue context</a> · <a class="tide-link" href="app/index.html">All 54 sample events</a></p><p class="tide-caption"><a class="tide-link" href="README.md">Scope and component ownership</a> · <a class="tide-link" href="qa/checks.json">Source and preservation checks</a></p></main></body></html>''')
    print('54 events (48 existing + 6 authored Sunshine samples), linked venue destination and independent app copy built.')

if __name__=='__main__':main()
