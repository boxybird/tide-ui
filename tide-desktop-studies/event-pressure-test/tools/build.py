"""Authored stress fixtures in an independent app copy; baseline is read-only."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from datetime import date
import json
import re
import shutil
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'shared-filter-release'
APP=ROOT/'app'
EVENTS=json.loads((ROOT/'data/events.json').read_text(encoding='utf-8'))
CHECK='--check' in sys.argv

def write(path,value):
    if CHECK:
        assert path.exists() and path.read_text(encoding='utf-8')==value,'Stale output: '+str(path)
    else:
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value,encoding='utf-8',newline='\n')

def replace_node(source,id,replacement):
    class Range(HTMLParser):
        def __init__(self):super().__init__();self.start=None;self.end=None;self.tag=None;self.depth=0
        def position_index(self):
            row,col=self.getpos();return sum(len(s) for s in source.splitlines(keepends=True)[:row-1])+col
        def handle_starttag(self,tag,attrs):
            if self.start is None and dict(attrs).get('id')==id:self.start=self.position_index();self.tag=tag;self.depth=1
            elif self.start is not None and self.end is None and tag==self.tag:self.depth+=1
        def handle_endtag(self,tag):
            if self.start is not None and self.end is None and tag==self.tag:
                self.depth-=1
                if not self.depth:self.end=source.index('>',self.position_index())+1
    p=Range();p.feed(source)
    assert p.start is not None and p.end is not None,'Missing node '+id
    return source[:p.start]+replacement+source[p.end:]

def plain(value):return escape(str(value or ''))

def date_text(value):
    d=date.fromisoformat(value)
    return f'{d:%A}, {d:%B} {d.day}, {d.year}'

def date_label(e):
    if not e.get('date'):return 'New date to be announced' if e.get('status')=='postponed' else 'Date unavailable'
    label=date_text(e['date'])
    if e.get('endDate') and e['endDate']!=e['date']:label+=' – '+date_text(e['endDate'])
    if e.get('status') in ('ended','cancelled'):label='Originally '+label
    return label

def badge(e):
    if not e.get('badge'):return ''
    variant=' tide-badge--danger' if e.get('status')=='cancelled' else ' tide-badge--warning' if e.get('status') in ('postponed','rescheduled','sold-out') else ''
    return f'<span class="tide-badge{variant}">{plain(e["badge"])}</span>'

def card(e,selected):
    chosen=e['id']==selected
    if e.get('date'):
        d=date.fromisoformat(e['date'])
        prominent=f'<time class="tide-date" datetime="{e["date"]}" aria-label="{plain(date_label(e))}"><span class="tide-date__day" aria-hidden="true">{d.day}</span><span class="tide-date__parts" aria-hidden="true"><span>{d:%a}</span><span>{d:%b}</span></span></time>'
        if e.get('endDate') and e['endDate']!=e['date']:
            end=date.fromisoformat(e['endDate']);prominent+=f'<span class="tide-caption">through {end:%b} {end.day}</span>'
    else:
        parts=('Not','available') if e.get('status')=='removed' else ('Date','TBA')
        prominent=f'<span class="tide-date" aria-label="{plain(date_label(e))}"><span class="tide-date__day" aria-hidden="true">—</span><span class="tide-date__parts" aria-hidden="true"><span>{parts[0]}</span><span>{parts[1]}</span></span></span>'
    price=e.get('price') or ('Price TBA' if not e.get('status') else '')
    meta=prominent+f'<span class="tide-event-card__separator" aria-hidden="true"></span><span>{plain(e["time"])}</span>'
    if price:meta+=f'<span class="tide-event-card__separator" aria-hidden="true"></span><span class="tide-event-card__price">{plain(price)}</span>'
    search=' '.join(str(e.get(k) or '') for k in ('title','venue','category','description','badge'))
    return f'''<article class="tide-event-card{' tide-event-card--in-view' if chosen else ''}" aria-labelledby="card-{e['id']}" data-date="{e.get('date') or ''}" data-end-date="{e.get('endDate') or e.get('date') or ''}" data-category="{e['category']}" data-search="{plain(search)}">
<a class="tide-event-card__link" href="{e['id']}.html" aria-label="View {plain(e['title'])}"></a>
<div class="tide-event-card__content"><div class="tide-event-card__copy"><div class="tide-event-card__heading tide-pressure__card-heading"><span class="tide-eyebrow">{e['category'].title()}</span>{badge(e)}<span class="tide-badge tide-event-card__status"{' hidden' if not chosen else ''}>In view</span></div><h4 class="tide-event-card__title" id="card-{e['id']}">{plain(e['title'])}</h4><p class="tide-event-card__venue">{plain(e['venue'])}</p></div><div class="tide-event-card__meta">{meta}</div></div></article>'''

def feed(selected):
    groups=[('month-2026-10','October 2026',lambda e:e.get('date','') and e['date'].startswith('2026-10') and e.get('status')!='ended'),
            ('month-2026-11','November 2026',lambda e:e.get('date','') and e['date'].startswith('2026-11')),
            ('date-updates','Awaiting details',lambda e:not e.get('date')),
            ('archive','Earlier events',lambda e:e.get('status')=='ended')]
    nav=''.join(f'<a class="tide-event-group__jump" href="#{id}" aria-label="Jump to {label}">{short}</a>' for (id,label,_),short in zip(groups,['Oct','Nov','TBA','Past']))
    out='<div class="tide-event-list tide-pressure__feed" id="pressure-feed">'
    for id,label,test in groups:
        items=sorted([e for e in EVENTS if test(e)],key=lambda e:(e.get('date') or '',e.get('start') or ''))
        out+=f'<section class="tide-event-group tide-event-group--sticky" id="{id}" aria-labelledby="{id}-title" tabindex="-1"><header class="tide-event-group__header tide-feed-study__month-header tide-slide-study__month-header"><h3 class="tide-event-group__title tide-feed-study__month-title" id="{id}-title" tabindex="-1">{label} <span class="tide-event-group__count tide-feed-study__month-count">{len(items)} events</span></h3><nav class="tide-event-group__nav tide-feed-study__month-nav" aria-label="Jump to event group">{nav}</nav></header>'
        out+=''.join(card(e,selected) for e in items)+'</section>'
    return out+'</div>'

def icon(name):
    value=(ROOT.parent.parent/'tide-responsive-app/assets/icons'/name).read_text(encoding='utf-8')
    value=re.sub(r'<svg[^>]*>','<svg class="tide-icon" viewBox="0 0 15 15" aria-hidden="true" focusable="false">',value)
    return re.sub(r'fill="#[A-Fa-f0-9]+"','fill="currentColor"',value)

def notice(e):
    if not e.get('notice'):return ''
    return f'<div class="tide-pressure__detail-message"><div class="tide-notice"><strong>{plain(e["notice"])}</strong><p>{plain(e["noticeBody"])}</p></div></div>'

def detail(e,level=2):
    classes='tide-app__detail tide-study__detail tide-slide-study__detail tide-room-study__detail'
    if e.get('status')=='removed':
        return f'<section class="{classes}" id="event-detail" aria-labelledby="event-title" tabindex="-1"><div class="tide-empty tide-pressure__state"><p class="tide-eyebrow">Listing unavailable</p><h{level} class="tide-pressure__state-title" id="event-title" tabindex="-1">This listing is no longer available.</h{level}><p>Previously listed as “{plain(e["title"])}”.</p><p>{plain(e["description"])}</p><a class="tide-button tide-button--secondary" href="index.html">Back to the lineup</a></div></section>'
    back=f'<a class="tide-photo-control" href="index.html" aria-label="Back to all events">{icon("ArrowLeftIcon.svg")}</a>'
    facts=[('CalendarIcon.svg','Date',date_label(e)),('ClockIcon.svg','Time',e['time']),('SewingPinIcon.svg','Venue',e['venue'])]
    fact_markup={label:plain(value) for _,label,value in facts}
    facts_html='<dl class="tide-event-hero__facts">'+''.join(f'<div><dt>{icon(symbol)}<span class="tide-sr-only">{label}</span></dt><dd>{plain(value)}</dd></div>' for symbol,label,value in facts)+'</dl>'
    # Machine-readable instants are emitted only when the organizer supplied them.
    if e.get('date'):
        dates=f'<time datetime="{e["date"]}">{plain(date_text(e["date"]))}</time>'
        if e.get('endDate') and e['endDate']!=e['date']:dates+=' – '+f'<time datetime="{e["endDate"]}">{plain(date_text(e["endDate"]))}</time>'
        if e.get('status') in ('cancelled','ended'):dates='Originally '+dates
        fact_markup['Date']=dates
        facts_html=facts_html.replace(plain(date_label(e)),dates)
    if e.get('start'):
        parts=e['time'].split('–',1)
        time_markup=f'<time datetime="{e["start"]}">{plain(parts[0])}</time>'
        if e.get('end') and len(parts)==2:time_markup+='–'+f'<time datetime="{e["end"]}">{plain(parts[1])}</time>'
        fact_markup['Time']=time_markup
        facts_html=facts_html.replace('<dd>'+plain(e['time'])+'</dd>','<dd>'+time_markup+'</dd>')
    price=e.get('price') or ('Price not announced' if not e.get('status') else 'No admission available')
    admission=f'<div class="tide-event-hero__admission"><p><strong>{plain(price)}</strong></p><span>{plain(e.get("priceNote", ""))}</span></div>'
    unavailable=e.get('status') in ('cancelled','postponed','sold-out','ended')
    action=f'<a class="tide-button tide-button--plan" href="{"index.html" if unavailable else "#attendance"}"><span>{plain(e["action"])}</span>{icon("ArrowRightIcon.svg")}</a>'
    intro=f'<div class="tide-event-hero__intro"><p class="tide-eyebrow">{e["category"].title()}</p><h{level} class="tide-event-hero__title" id="event-title" tabindex="-1">{plain(e["title"])}</h{level}><p class="tide-event-hero__subtitle">{plain(e["subtitle"])}</p></div>'
    if e.get('photo'):
        src={'rough':'js/assets/organizer-upload.png','print':'../../shared-filter-release/kit/assets/images/ink-after-dark.png','concert':'assets/images/concert.png'}[e['photo']]
        alt={'rough':'A softly focused organizer phone photo of a printmaking table below a large blank wall.','print':'Hands and inked tools on a shared printmaking worktable.','concert':'A small live music performance, photographed from the audience.'}[e['photo']]
        opening=f'<section class="tide-event-hero tide-study__opening" aria-labelledby="event-title"><img class="tide-event-hero__photo" src="{src}" alt="{alt}" width="1024" height="1536" fetchpriority="high"><div class="tide-event-hero__scrim" aria-hidden="true"></div><nav class="tide-event-hero__toolbar" aria-label="Event">{back}</nav><div class="tide-event-hero__content">{intro}{facts_html}{admission}{action}<a class="tide-event-hero__cue" href="#event-story">More about this event {icon("ChevronDownIcon.svg")}</a></div></section>'
    else:
        summary='<dl class="tide-summary">'+''.join(f'<div><dt>{label}</dt><dd>{fact_markup[label]}</dd></div>' for _,label,value in facts)+'</dl>'
        opening=f'<section class="tide-fallback tide-pressure__fallback" aria-labelledby="event-title"><nav class="tide-row tide-pressure__fallback-nav" aria-label="Event"><a class="tide-button tide-button--quiet" href="index.html">Back to the lineup</a></nav><p class="tide-fallback__label">No photo provided</p><p class="tide-eyebrow">{e["category"].title()}</p><h{level} class="tide-pressure__fallback-title" id="event-title" tabindex="-1">{plain(e["title"])}</h{level}><p class="tide-caption">{plain(e["subtitle"])}</p>{summary}<p><strong>{plain(price)}</strong></p><p class="tide-caption">{plain(e.get("priceNote", ""))}</p><a class="tide-button tide-button--full" href="{"index.html" if unavailable else "#attendance"}">{plain(e["action"])}</a></section>'
    article=f'''<article class="tide-event-details tide-study__story" id="event-story" aria-labelledby="story-title" tabindex="-1"><p class="tide-eyebrow">About this gathering</p><h{level+1} class="tide-event-details__title" id="story-title">{plain(e['subtitle'])}</h{level+1}><p class="tide-event-details__lead">{plain(e['description'])}</p><section class="tide-event-details__section"><h{level+2} class="tide-event-details__section-title">Before you go</h{level+2}><p>{plain(e['practical'])}</p></section><section class="tide-event-details__section"><h{level+2} class="tide-event-details__section-title" id="attendance" tabindex="-1">{plain(e['action'])}</h{level+2}><p>{'This event is not available for new attendance. Return to the lineup to explore another date.' if unavailable else 'A live listing would use the organizer’s verified contact or booking destination here. No external booking is made in this sample.'}</p></section><p class="tide-disclosure">An authored pressure-test event. Details, availability and photographs are illustrative.</p><a class="tide-back-link" href="index.html">Back to the lineup</a></article>'''
    return f'<section class="{classes}" id="event-detail" aria-labelledby="event-title" tabindex="-1">{notice(e)}{opening}{article}</section>'

def copy_sources():
    # Assets and legacy secondary sample pages stay local to this copy.
    for p in (BASE/'app').rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(BASE/'app');target=APP/rel
        if rel.as_posix() in ('index.html','search.html','js/filters.js'):continue
        if p.suffix=='.html':
            text=p.read_text(encoding='utf-8').replace('../kit/','../../shared-filter-release/kit/')
            write(target,text)
        elif p.suffix in ('.css','.js'):
            if rel.as_posix() in ('js/search-core.js','js/event-search.js'):continue
            write(target,p.read_text(encoding='utf-8'))
        elif not CHECK:
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    core=(BASE/'app/js/search-core.js').read_text(encoding='utf-8')
    core=core.replace("if (state.from && event.date < state.from) return false;\n    if (state.to && event.date > state.to) return false;", "const start=date(event.date), end=date(event.endDate)||start;\n    if ((state.from||state.to)&&!start) return false;\n    if (state.from && end < state.from) return false;\n    if (state.to && start > state.to) return false;")
    write(APP/'js/search-core.js',core)
    search=(BASE/'app/js/event-search.js').read_text(encoding='utf-8')
    search=search.replace("'Oct 23–Nov 29, 2026'","'Oct 23–Nov 6, 2026'")
    write(APP/'js/event-search.js',search)
    controller=(BASE/'app/js/filters.js').read_text(encoding='utf-8')
    controller=controller.replace("const next=state(),valid=TideSearch.validRange(next);", "const scene=document.body.dataset.pressureState;\n    if(scene==='feed-loading'||scene==='feed-failed'){\n      counter.textContent='Match count unavailable';apply.disabled=true;\n      apply.textContent=scene==='feed-loading'?'Loading events…':'Events unavailable';return;\n    }\n    apply.disabled=false;\n    const next=state(),valid=TideSearch.validRange(next);")
    controller=controller.replace("window.addEventListener('pageshow',()=>{", "window.addEventListener('pressure:state',update);\n  window.addEventListener('pageshow',()=>{")
    write(APP/'js/filters.js',controller)

SCENES=[
 ('feed-loading','Initial feed loading','The feed is unknown while a request is pending. Counts are not presented as zero.'),
 ('feed-failed','First load failed','A clear retry action recovers the same panel, preserving draft controls.'),
 ('no-upcoming','Nothing upcoming','An unfiltered empty feed has different wording from no filter matches.'),
 ('detail-loading','Opening one event','The list remains available while its selected event is loading.'),
 ('detail-failed','One event failed','Retry replaces only the failed detail; list position and draft filters remain.'),
 ('cached-copy','Stale / offline copy','Keep readable content, label its age, and provide a way to refresh the sample.')]

def page(e=None,scene=None,index=False):
    template=(BASE/'app'/('index.html' if index else 'desert-frequencies.html')).read_text(encoding='utf-8')
    template=template.replace('../kit/','../../shared-filter-release/kit/')
    template=template.replace('data-width="margin-aligned"','data-width="pressure-test"')
    template=template.replace('class="tide-gutter-study','class="tide-pressure tide-gutter-study',1)
    template=template.replace('<body ','<body data-pressure-state="'+(scene or 'ready')+'" ',1)
    template=template.replace('<div class="tide-event-list">','<div class="tide-event-list" id="pressure-feed">',1)
    selected=e or EVENTS[0]
    template=replace_node(template,'pressure-feed','<div class="tide-event-list" id="pressure-feed"></div>' if scene=='no-upcoming' else feed(selected['id']))
    template=replace_node(template,'event-detail',detail(selected,2 if index else 1))
    template=template.replace('48 events',f'{len(EVENTS)} events').replace('All 48 events','All sample events')
    template=template.replace('Soonest first','Date order')
    template=template.replace('Oct 23–Nov 29, 2026','Oct 23–Nov 6, 2026')
    template=template.replace('id="filter-badge">Upcoming','id="filter-badge">All dates')
    template=template.replace('href="submit.html">Add an event','href="../index.html">Test cases')
    template=template.replace('href="submit.html">Have something happening? Add an event.','href="../index.html">View the pressure-test cases')
    template=template.replace('End of the sample feed. Fictional events for UX testing.','End of the sample feed. Includes changed, undated and past events for this study.')
    template=re.sub(r'<title>.*?</title>','<title>'+plain((selected['title'] if e else 'Event pressure test')+' · Burque')+'</title>',template)
    if scene=='no-upcoming':template=template.replace('action="search.html"','action="no-upcoming.html"').replace('href="index.html"','href="no-upcoming.html"')
    template=template.replace('</head>','<link rel="stylesheet" href="../css/pressure.css">\n<script src="js/pressure.js" defer></script>\n</head>')
    return template

def review():
    sections=[]
    for priority,title,intro in [(1,'Messy event details','Long copy, incomplete information and schedules that do not fit one simple evening.'),(2,'Changed plans','Changes appear in the feed and detail, and attendance actions respect the event’s state.'),(3,'Waiting, failure and recovery','Held loading specimens and local retry demonstrations. No backend or user submissions are involved.')]:
        cards=''
        items=[(e['id'],e['case'],e['title']) for e in EVENTS if e['priority']==priority] if priority<3 else SCENES
        for id,name,description in items:
            extra=f'<a class="tide-link" href="app/{id}.html?play=1&amp;inspect=1">Play loading → ready</a>' if id in ('feed-loading','detail-loading') else ''
            cards+=f'<article class="tide-pressure-review__case"><p class="tide-eyebrow">{plain(name)}</p><h3>{plain(description)}</h3><div class="tide-row"><a class="tide-button tide-button--secondary" href="app/{id}.html?preview-filters=open&amp;inspect=1">Open case</a>{extra}</div></article>'
        sections.append(f'<section class="tide-stack" id="priority-{priority}"><header class="tide-stack"><p class="tide-eyebrow">Priority {priority}</p><h2>{title}</h2><p>{intro}</p></header><div class="tide-pressure-review__grid">{cards}</div></section>')
    return '''<!doctype html><html lang="en" data-theme="bumble" data-mode="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Burque · Event pressure test</title><link rel="stylesheet" href="../shared-filter-release/kit/css/tide.css"><link rel="stylesheet" href="css/review.css"></head><body class="tide tide-pressure-review"><a class="tide-skip-link" href="#cases">Skip to test cases</a><main class="tide-pressure-review__main tide-stack" id="cases"><header class="tide-stack"><p class="tide-eyebrow">Shared Filters / Separate pressure-test copy</p><h1>The same design. Less perfect events.</h1><p>Fourteen authored events and six recovery scenes test the accepted list and event layout. The approved baseline and UI kit remain untouched.</p><div class="tide-row"><a class="tide-button" href="app/index.html?preview-filters=open">Browse the pressure-test app</a><a class="tide-button tide-button--secondary" href="../shared-filter-release/app/index.html?preview-filters=open">Approved baseline</a></div><nav class="tide-row" aria-label="Case groups"><a class="tide-link" href="#priority-1">Messy details</a><a class="tide-link" href="#priority-2">Changed plans</a><a class="tide-link" href="#priority-3">Loading and recovery</a></nav></header><div class="tide-notice"><strong>Controlled sample data</strong><p>Reference time: October 24, 2026, noon in Albuquerque. Loading views are held for inspection; use Play loading → ready to see completion. Retry and refresh load local sample HTML. No network availability, bookings or PWA caching are claimed.</p></div>'''+''.join(sections)+'''<section class="tide-notice"><strong>What remains fixed</strong><p>Manrope, palette, spacing tokens, cards, square controls, desktop Margin Reveal, native scrollbar spacing and the mobile/tablet filter drawer come from the approved release.</p><p><a class="tide-link" href="README.md">Case and component contracts</a> · <a class="tide-link" href="qa/checks.json">Source and preservation checks</a></p></section></main></body></html>'''

def main():
    copy_sources()
    write(APP/'index.html',page(index=True))
    write(APP/'search.html',page(index=True))
    for e in EVENTS:write(APP/(e['id']+'.html'),page(e=e))
    for id,_,_ in SCENES:write(APP/(id+'.html'),page(e=EVENTS[0] if id.startswith('detail-') else None,scene=id,index=not id.startswith('detail-')))
    write(ROOT/'index.html',review())
    print('14 messy events, 6 loading/recovery scenes and independent consumer built.')

if __name__=='__main__':main()
