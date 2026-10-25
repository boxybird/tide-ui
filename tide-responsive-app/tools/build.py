"""Build the responsive HTML study. Standard library, no runtime framework.

Composition is shared across viewport sizes and themes. Run after kit/tools/build.py.
"""
from pathlib import Path
from html import escape as e
import argparse
import json
import re
import calendar
import sys
from events import load_events,month_groups

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'kit/tools'))
from content import help_content
EVENTS = load_events(ROOT/'data/events.json')
THEMES = [(name,mode) for name in json.loads((ROOT/'kit/tokens/themes.json').read_text(encoding='utf-8'))['themes'] for mode in ('dark','light')]
INK = next(x for x in EVENTS if x['slug']=='ink-after-dark')
PAGES = ['index.html'] + [x['slug']+'.html' for x in EVENTS] + ['search.html','saved.html','submit.html','help.html']
REVIEWS = {'review.html': ('Browse','index.html'), 'event-review.html': ('Event','ink-after-dark.html'), 'search-review.html': ('Search','search.html'), 'submit-review.html': ('Submit','submit.html'), 'help-review.html': ('Help','help.html')}


def icon(name):
    svg=(ROOT/'assets/icons'/f'{name}Icon.svg').read_text(encoding='utf-8')
    svg=re.sub(r'<svg[^>]*>', '<svg class="tide-icon" viewBox="0 0 15 15" fill="none" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">', svg)
    return re.sub(r'fill="#[0-9a-fA-F]+"', 'fill="currentColor"', svg)


def doc(title,body,theme,mode,prefix,review=False,event=False,navigation=False):
    sheet='review' if review else 'app'
    cls='tide tide-review' if review else 'tide tide-app'+(' tide-app--event' if event else '')
    script=''.join(f'<script src="{prefix}js/{name}.js" defer></script>' for name in ('search-core','event-search','event-navigation')) if navigation else ''
    return f'''<!doctype html>
<html lang="en" data-theme="{theme}" data-mode="{mode}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="A static, responsive Burque events design study using the Tide HTML and CSS kit.">
  <title>{e(title)} · Burque</title>
  <link rel="stylesheet" href="{prefix}kit/css/tide.css">
  <link rel="stylesheet" href="{prefix}css/{sheet}.css">
  {script}
</head>
<body class="{cls}">
{body}
</body>
</html>
'''


def header(current=''):
    def link(href,text,wide=False,svg=''):
        return f'<a class="tide-app__nav-link'+(' tide-app__nav-link--wide' if wide else '')+f'" href="{href}"'+(' aria-current="page"' if current==href else '')+f'>{svg}{text}</a>'
    return f'''<header class="tide-app__header">
      <a class="tide-brand" href="index.html" aria-label="Burque home">BURQUE<span aria-hidden="true">.</span></a>
      <nav class="tide-app__nav" aria-label="Main">{link('index.html','Find events',True)}{link('submit.html','Add an event',True)}{link('saved.html','Saved',False,icon('Bookmark'))}</nav>
    </header>'''


def footer():
    return '<footer class="tide-app__site-footer">Design preview · Sample events and illustrative photography. No reservations or submissions are made.</footer>'


def skips(event=False,split=True):
    target='event-detail' if event else 'results' if split else 'main-content'
    text='Skip to event' if event else 'Skip to results' if split else 'Skip to content'
    return f'<a class="tide-app__skip" href="#{target}">{text}</a>'+('' if event or not split else '<a class="tide-app__skip tide-app__skip--detail" href="#event-detail">Skip to event preview</a>')


def card(x,selected=False,current=False):
    slug=x['slug']; stamp=x['datetime']
    searchable=' '.join(str(x[k]) for k in ('title','category','venue','subtitle','lead'))
    if x['category']=='Workshop':searchable+=' workshops'
    return f'''<article class="tide-event-card{(' tide-event-card--in-view' if selected else '')}" aria-labelledby="card-{slug}" data-date="{x['date']}" data-category="{x['category'].lower()}" data-search="{e(searchable)}">
      <a class="tide-event-card__link" href="{slug}.html" aria-label="View {e(x['title'])}"{(' aria-current="page"' if current else '')}></a>
      <div class="tide-event-card__content"><div class="tide-event-card__copy">
        <div class="tide-event-card__heading"><span class="tide-eyebrow">{x['category']}</span><span class="tide-badge tide-event-card__status"{('' if selected else ' hidden')}>In view</span></div>
        <h4 class="tide-event-card__title" id="card-{slug}">{e(x['title'])}</h4>
        <p class="tide-event-card__venue">{e(x['venue'])}</p>
      </div>
      <div class="tide-event-card__meta"><time class="tide-date" datetime="{x['date']}" aria-label="{x['longDate']}, {x['date'][:4]}"><span class="tide-date__day" aria-hidden="true">{x['day']}</span><span class="tide-date__parts" aria-hidden="true"><span>{x['weekday']}</span><span>{x['month']}</span></span></time><span class="tide-event-card__separator" aria-hidden="true"></span><time datetime="{stamp}">{x['time']}</time><span class="tide-event-card__separator" aria-hidden="true"></span><span class="tide-event-card__price">{x['price']}</span></div></div>
    </article>'''


def filters():
    # All controls belong to one GET form, including the search field above.
    return f'''<details class="tide-expandable tide-app__filters"><summary class="tide-expandable__summary">Filters {icon('ChevronDown').replace('class="tide-icon"','class="tide-icon tide-expandable__icon"')}</summary>
      <div class="tide-expandable__body tide-app__filter-form">
        <fieldset class="tide-fieldset"><legend class="tide-fieldset__legend">When</legend>
          <p class="tide-field__hint" id="date-hint">Include either date, or both. Dates are local to Albuquerque.</p>
          <div class="tide-app__date-fields">
            <div class="tide-field"><label class="tide-field__label" for="event-from">From</label><input class="tide-field__control" id="event-from" type="date" name="from" form="event-search-form" aria-describedby="date-hint"></div>
            <div class="tide-field"><label class="tide-field__label" for="event-to">Through</label><input class="tide-field__control" id="event-to" type="date" name="to" form="event-search-form" aria-describedby="date-hint date-error"></div>
          </div>
          <p class="tide-field__error" id="date-error" hidden>Choose an end date on or after the start date.</p>
        </fieldset>
        <fieldset class="tide-fieldset"><legend class="tide-fieldset__legend">Category</legend>
          <label class="tide-choice"><input type="checkbox" name="category" value="music" form="event-search-form"> Music</label>
          <label class="tide-choice"><input type="checkbox" name="category" value="comedy" form="event-search-form"> Comedy</label>
          <label class="tide-choice"><input type="checkbox" name="category" value="workshop" form="event-search-form"> Workshops</label>
          <p class="tide-field__hint">No category selected includes all categories.</p>
        </fieldset>
        <div class="tide-app__filter-actions"><button class="tide-button tide-button--secondary" type="submit" form="event-search-form">Apply filters</button><a class="tide-link" href="index.html">Clear all</a></div>
      </div>
    </details>'''


def month_label(key):
    year,month=map(int,key.split('-'))
    return f'{calendar.month_name[month]} {year}'


def month_navigation(items):
    groups=month_groups(items)
    if len(groups)<2:return ''
    return '<nav class="tide-event-group__nav" aria-label="Jump to month">'+''.join(f'<a class="tide-event-group__jump" href="#month-{key}" aria-label="Jump to {month_label(key)}">{calendar.month_abbr[int(key[-2:])]}</a>' for key,_ in groups)+'</nav>'


def feed(items,selected,current):
    groups=[]
    for key,events in month_groups(items):
        count=f'{len(events)} '+('event' if len(events)==1 else 'events')
        groups.append(f'<section class="tide-event-group tide-event-group--sticky" id="month-{key}" aria-labelledby="month-title-{key}" tabindex="-1"><header class="tide-event-group__header"><h3 class="tide-event-group__title" id="month-title-{key}" tabindex="-1">{month_label(key)} <span class="tide-event-group__count">{count}</span></h3>{month_navigation(items)}</header>'+''.join(card(x,x==selected,current and x==selected) for x in events)+'</section>')
    return '<div class="tide-event-list">'+''.join(groups)+'</div>'


def results(selected=INK,current=False,state='browse'):
    level=2 if current else 1
    title,eyebrow,desc=('Coming up.','Albuquerque','Good things happening close to home.')
    items=EVENTS
    if state=='search': title,eyebrow,desc='Find your evening.','Search','One idea can lead to a good night out.'
    if state=='saved': title,eyebrow,desc='For another evening.','Saved','Your shortlist, all in one place.';items=[INK]
    count=f'{len(items)} '+('event' if len(items)==1 else 'events')
    search=''
    if state!='saved':
        search=f'''<form class="tide-app__search tide-stack" id="event-search-form" action="search.html" method="get" aria-label="Find events">
          <label class="tide-app__search-label" for="event-query">Search events</label>
          <div class="tide-search-line"><input class="tide-field__control" id="event-query" name="q" type="search" placeholder="Music, workshops, a place…" maxlength="160"><button class="tide-button tide-button--icon" aria-label="Search events" type="submit">{icon('ArrowRight')}</button></div>
        </form>
        <div class="tide-app__filter-row"><p id="date-summary">Oct 23–Nov 29, 2026</p><span class="tide-badge" id="filter-badge">Upcoming</span><a class="tide-link tide-app__clear" href="index.html" hidden>Clear all</a></div>{filters()}
        <noscript><p class="tide-app__search-note tide-caption">Search and filters need JavaScript in this local preview. All 48 events are available below.</p></noscript>'''
    return f'''<section class="tide-app__results" id="results" aria-labelledby="results-title" tabindex="0">
      <div class="tide-page-intro tide-app__intro"><p class="tide-eyebrow">{eyebrow}</p><h{level} class="tide-page-intro__title" id="results-title">{title}</h{level}><p>{desc}</p></div>
      {search}
      <div class="tide-results"><h2 class="tide-results__count" id="result-count" role="status" aria-live="polite" aria-atomic="true">{count}</h2><span class="tide-results__order">Soonest first</span></div>
      {feed(items,selected,current)}
      <div class="tide-empty" id="empty-results" hidden>{icon('Calendar')}<h2>No events found.</h2><p>Try another search, a wider date range or fewer categories.</p><a class="tide-button tide-button--secondary" href="index.html">Clear search and filters</a></div>
      <footer class="tide-app__result-footer"><a class="tide-link" href="submit.html">Have something happening? Add an event.</a><a class="tide-link tide-app__all-events" href="index.html"{(' hidden' if state=='browse' else '')}>Back to all events</a><p class="tide-caption">{('Saved items are an example shortlist.' if state=='saved' else 'End of the sample feed. Fictional events for UX testing.')}</p></footer>
    </section>'''


def detail(x,prefix,event=False):
    heading=1 if event else 2;story=heading+1;sub=story+1
    img=prefix+('kit/assets/images/' if x['image']=='ink-after-dark.png' else 'assets/images/')+x['image']
    def fact(label,svg,content):
        return f'<div><dt>{icon(svg)}<span class="tide-sr-only">{label}</span></dt><dd>{content}</dd></div>'
    def section(title,content,id=''):
        return f'<section class="tide-event-details__section"><h{sub} class="tide-event-details__section-title"'+(f' id="{id}" tabindex="-1"' if id else '')+f'>{title}</h{sub}>{content}</section>'
    inclusions='<ul class="tide-inclusions">'+''.join(f'<li>{icon("Check")}{e(s)}</li>' for s in x['inclusions'])+'</ul>'
    schedule='<dl class="tide-schedule">'+''.join(f'<div><dt>{e(t)}</dt><dd>{e(s)}</dd></div>' for t,s in x['schedule'])+'</dl>'
    know=''.join(f'<p>{e(p)}</p>' for p in x['know'])
    return f'''<section class="tide-app__detail" id="event-detail" aria-labelledby="event-title" tabindex="-1">
      <section class="tide-event-hero" aria-labelledby="event-title">
        <img class="tide-event-hero__photo" src="{img}" width="1024" height="1536" alt="{e(x['alt'])}" fetchpriority="high">
        <div class="tide-event-hero__scrim" aria-hidden="true"></div>
        <nav class="tide-event-hero__toolbar" aria-label="Event"><a class="tide-photo-control" href="index.html" aria-label="Back to all events">{icon('ArrowLeft')}</a><a class="tide-photo-control" href="saved.html" aria-label="View saved events">{icon('Bookmark')}</a></nav>
        <div class="tide-event-hero__content"><div class="tide-event-hero__intro"><p class="tide-eyebrow">{x['category']} <span aria-hidden="true">/</span> {x['age']}</p><h{heading} class="tide-event-hero__title" id="event-title">{e(x['title'])}</h{heading}><p class="tide-event-hero__subtitle">{e(x['subtitle'])}</p></div>
          <dl class="tide-event-hero__facts">
            {fact('Date','Calendar',f'<time datetime="{x["date"]}">{x["longDate"]}<span class="tide-event-hero__note">, {x["date"][:4]}</span></time>')}
            {fact('Time','Clock',f'<time datetime="{x["datetime"]}">{x["range"]}</time><span class="tide-event-hero__note">· {x["duration"]}</span>')}
            {fact('Venue','SewingPin',e(x['venue']))}
          </dl>
          <div class="tide-event-hero__admission"><p><strong>{x['price']}</strong><span>per person</span></p><span>{x['included']}</span></div>
          <a class="tide-button tide-button--plan" href="#attendance"><span>Plan this evening</span>{icon('ArrowRight')}</a>
          <a class="tide-event-hero__cue" href="#event-story"><span>More about the {x['category'].lower()}</span>{icon('ArrowDown')}</a>
        </div>
      </section>
      <article class="tide-event-details" id="event-story" aria-labelledby="story-title" tabindex="-1">
        <p class="tide-eyebrow">{x['eyebrow']}</p><h{story} class="tide-event-details__title" id="story-title">{e(x['heading'])}</h{story}><p class="tide-event-details__lead">{e(x['lead'])}</p>
        {section('Your evening includes',inclusions)}
        {section('The evening, loosely planned',schedule)}
        {section('Good to know',know)}
        {section('Finding your way',f'<p class="tide-place">{e(x["venue"])}<br><span>Albuquerque, New Mexico</span></p><p>Ask the organizer about step-free access, seating and other access needs before booking. Access details have not been confirmed for this sample event.</p>')}
        {section('Before you go',f'<div class="tide-app__attendance"><p>{e(x["attendance"])}</p><p>This is an illustrative event. Booking is unavailable in this design preview.</p></div>','attendance')}
        <p class="tide-disclosure">A fictional evening for a design study. Event details and photography are illustrative; this page does not make a reservation.</p>
        <a class="tide-back-link" href="index.html">{icon('ArrowLeft')}Back to all events</a>
      </article>
    </section>'''


def app_page(filename,theme,mode,prefix):
    if filename=='help.html':
        body=skips(split=False)+header()+help_content({'BROWSE':'index.html','SEARCH':'search.html','SUBMIT':'submit.html','EVENT':'ink-after-dark.html'})
        return doc('Help & guidance',body,theme,mode,prefix)
    event=next((x for x in EVENTS if filename==x['slug']+'.html'),None)
    if filename=='submit.html': return submission(theme,mode,prefix)
    state='search' if filename=='search.html' else 'saved' if filename=='saved.html' else 'browse'
    selected=event or INK
    preview_state='<section class="tide-app__preview-state tide-empty" id="preview-state" aria-labelledby="preview-state-title" tabindex="-1" hidden><p class="tide-eyebrow">Event preview</p><h2 id="preview-state-title">Choose an evening.</h2><p id="preview-state-description">Open a result to see the full event.</p></section>'
    body=skips(bool(event))+header(filename)+f'<main class="tide-app__workspace">{results(selected,bool(event),state)}{detail(selected,prefix,bool(event))}{preview_state}</main>'+footer()
    title=event['title'] if event else 'Search events' if state=='search' else 'Saved events' if state=='saved' else 'Upcoming events in Albuquerque'
    return doc(title,body,theme,mode,prefix,event=bool(event),navigation=True)


def field(label,id,type='text',hint='',value='',required=True,attrs=''):
    req=' required' if required else ''
    desc=f' aria-describedby="{id}-hint"' if hint else ''
    control=f'<textarea class="tide-field__control" id="{id}" name="{id}"{req}{desc}>{e(value)}</textarea>' if type=='textarea' else f'<input class="tide-field__control" id="{id}" name="{id}" type="{type}" value="{e(value)}"{req}{desc} {attrs}>'
    return f'<div class="tide-field"><label class="tide-field__label" for="{id}">{label}'+(' <span>(optional)</span>' if not required else '')+f'</label>{control}'+(f'<p class="tide-field__hint" id="{id}-hint">{hint}</p>' if hint else '')+'</div>'


def submission(theme,mode,prefix):
    body=skips(split=False)+header('submit.html')+f'''<main class="tide-app__form-wrap" id="main-content" tabindex="-1">
      <div class="tide-page-intro tide-app__intro"><p class="tide-eyebrow">For the neighborhood</p><h1 class="tide-page-intro__title">Make a little noise.</h1><p>Have something happening in Albuquerque? Start with the details.</p></div>
      <div class="tide-page-body"><form class="tide-app__form" aria-label="Event submission example">
        <p class="tide-caption">Form preview. Fields are required unless marked optional. Nothing is submitted or stored.</p>
        <section class="tide-form-section" aria-labelledby="basics"><h2 id="basics">The basics</h2>
          {field('Event name','event-name',hint='Keep it clear and specific. Up to 80 characters.',attrs='maxlength="80"')}
          <div class="tide-field"><label class="tide-field__label" for="event-category">Category</label><select class="tide-field__control" id="event-category" name="category" required><option value="">Choose a category</option><option>Music</option><option>Comedy</option><option>Workshop</option><option>Community</option></select></div>
          {field('Tell us about it','description','textarea','What will people do, and what should they know before coming?')}
        </section>
        <section class="tide-form-section" aria-labelledby="when-where"><h2 id="when-where">When &amp; where</h2>
          <div class="tide-app__field-row">{field('Date','date','date')}{field('Start time','time','time','Times are local to Albuquerque.')}</div>
          {field('Venue name','venue')}
          {field('Address','address',attrs='autocomplete="street-address"')}
          <div class="tide-app__field-row">{field('Admission price','price',hint='Use “Free” or the full price including fees.')}{field('Age requirement','age',hint='For example: All ages or 21+.')}</div>
          {field('Accessibility information','access','textarea','Describe confirmed access, seating and facilities. If unknown, say so.',required=False)}
        </section>
        <section class="tide-form-section" aria-labelledby="photo-contact"><h2 id="photo-contact">Photo &amp; contact</h2>
          <div class="tide-upload"><label class="tide-field__label" for="photo">Event photo (optional)</label><input id="photo" name="photo" type="file" accept="image/jpeg,image/png,image/webp" aria-describedby="photo-hint"><p class="tide-field__hint" id="photo-hint">A clear phone photo is enough. JPEG, PNG or WebP. Nothing is uploaded in this preview.</p></div>
          {field('Organizer email','email','email','For questions about your listing. Not displayed publicly.',attrs='autocomplete="email"')}
          <label class="tide-choice"><input type="checkbox" name="permission" required> I have permission to share these details and this photo.</label>
        </section>
        <div class="tide-form-actions"><button class="tide-button tide-button--secondary" type="reset">Reset form</button><a class="tide-back-link" href="index.html">{icon('ArrowLeft')}Back to all events</a></div>
      </form></div>
    </main>'''+footer()
    return doc('Add an event',body,theme,mode,prefix)


def review_page(filename,theme,mode,prefix):
    state,target=REVIEWS[filename]
    if state=='Help': return help_review(theme,mode,prefix)
    themes=''.join(f'<a class="tide-chip" href="{prefix}{t}-{m}/{filename}"'+(' aria-current="page"' if (t,m)==(theme,mode) else '')+f'>{t.title()} · {m}</a>' for t,m in THEMES)
    states=''.join(f'<a class="tide-chip" href="{f}"'+(' aria-current="page"' if f==filename else '')+f'>{name}</a>' for f,(name,_) in REVIEWS.items())
    def frame(name,size,description,variant):
        return f'''<figure class="tide-review__figure"><figcaption><div><h2>{name}</h2><p>{size} · {description}</p></div><a href="{target}" target="_blank" rel="noopener">Open app<span class="tide-sr-only"> · {name} example, new tab</span></a></figcaption><div class="tide-review__viewport tide-review__viewport--{variant}"><iframe src="{target}" title="{name}: {e(state)} screen" loading="lazy"></iframe></div></figure>'''
    body=f'''<div class="tide-review__wrap"><header class="tide-review__header"><div><p class="tide-eyebrow">Tide in use · Responsive HTML study</p><h1>One kit. More room.</h1><p>The same components, reflowing around the space available. Browse on a phone, open an event, then compare it with the paired desktop view.</p></div><a class="tide-button tide-button--secondary" href="{target}" target="_blank" rel="noopener">Open full-size app<span class="tide-sr-only"> in a new tab</span></a></header>
      <nav class="tide-review__nav" aria-label="Theme and mode">{themes}</nav>
      <nav class="tide-review__nav" aria-label="Screen example">{states}</nav>
      <main><div class="tide-review__pair">{frame('Phone','390 × 844','One column, full-width cards','phone')}{frame('Tablet portrait','834 × 1112','A contained reading width','tablet')}</div>
      {frame('Desktop / tablet landscape','1440 × 1000','Results beside the full event','desktop')}
      <aside class="tide-review__notes" aria-label="About this study"><p><strong>Preserved foundation.</strong> The original Tide kit remains untouched. This study consumes a reviewed copy with the same palette, type, card geometry and spacing primitives. <a href="{prefix}versions/1.0.3/index.html">Open the preserved three-event version.</a></p><p><strong>Long-feed UX test.</strong> Browse 48 distinct events: 16 in October and 32 in November. Month headings stay in view; Oct/Nov links jump within the desktop list. Search by title, venue or description, combine inclusive dates and categories, then clear to the complete feed. <a href="{prefix}docs/SEARCH-FILTERS.md">Search test cases</a>.</p><p><strong>HTML with small enhancements.</strong> Search and filters work locally in JavaScript, with choices retained in the URL and event links. Event links and disclosures retain native fallbacks. The desktop helper preserves list position and sequences smooth event navigation. Saved is a sample shortlist; submission does not send anything.</p><p><strong>Responsive, with room for a PWA.</strong> Safe-area spacing, a full-height event opening and in-app back navigation are included. Installation, offline behavior and account storage belong to a later implementation.</p><p><a href="{prefix}kit/index.html">Reviewed UI kit</a> · <a href="{prefix}docs/REVIEW.md">Code and accessibility review</a> · <a href="{prefix}docs/RESPONSIVE.md">Responsive decisions</a> · <a href="{prefix}README.md">Source and handoff</a></p></aside></main></div>'''
    return doc('Tide in use — '+state,body,theme,mode,prefix,review=True)


def help_review(theme,mode,prefix):
    themes=''.join(f'<a class="tide-chip" href="{prefix}{t}-{m}/help-review.html"'+(' aria-current="page"' if (t,m)==(theme,mode) else '')+f'>{t.title()} · {m}</a>' for t,m in THEMES)
    def frame(name,size,description,variant):
        return f'<figure class="tide-review__figure"><figcaption><div><h2>{name}</h2><p>{size} · {description}</p></div><a href="help.html" target="_blank" rel="noopener">Open help page<span class="tide-sr-only"> in a new tab</span></a></figcaption><div class="tide-review__viewport tide-review__viewport--{variant}"><iframe src="help.html" title="{name}: Help and guidance" loading="lazy"></iframe></div></figure>'
    body=f'''<div class="tide-review__wrap"><header class="tide-review__header"><div><p class="tide-eyebrow">Tide in use · Prose &amp; content pages</p><h1>Room for the words.</h1><p>A realistic help page, using the same kit. Compare reading rhythm, contents links and practical details across every theme and screen size.</p></div><a class="tide-button tide-button--secondary" href="help.html" target="_blank" rel="noopener">Open full-size help<span class="tide-sr-only"> in a new tab</span></a></header>
    <nav class="tide-review__nav" aria-label="Theme and mode">{themes}</nav><nav class="tide-review__nav" aria-label="Related previews"><a class="tide-chip" href="review.html">Event app</a><a class="tide-chip" href="{prefix}kit/{theme}-{mode}/index.html#content-pages">UI kit additions</a><a class="tide-chip" href="{prefix}kit/docs/CONTENT.md">HTML &amp; CSS contract</a></nav>
    <main><div class="tide-review__pair">{frame('Phone','390 × 844','Contents followed by the article','phone')}{frame('Tablet portrait','834 × 1112','The same reading rhythm, with room to breathe','tablet')}</div>{frame('Desktop','1440 × 1000','Contents beside a contained reading column','desktop')}
    <aside class="tide-review__notes" aria-label="About these additions"><p><strong>Preserved foundation.</strong> Manrope, the existing type/space/color tokens, square corners and neutral outlines. Existing event pages and app CSS are preserved.</p><p><strong>Shared implementation.</strong> <code>tide-prose</code> styles ordinary rich HTML. <code>tide-content-page</code> owns the title, updated date, optional contents and footer. The app consumes both from the kit; this gallery adds no product styling.</p><p><strong>Realistic content, clear scope.</strong> Guidance covers search, dates, admission, access questions and changed plans. It describes the current preview honestly; it is not an invented privacy policy.</p><p><a href="{prefix}kit/{theme}-{mode}/frames/prose.html">Full rich-HTML specimen</a> · <a href="{prefix}kit/docs/CONTENT.md">Component contracts</a> · <a href="{prefix}README.md">Source and handoff</a></p></aside></main></div>'''
    return doc('Help page — theme and viewport review',body,theme,mode,prefix,review=True)


def outputs():
    out={}
    for folder,theme,mode,prefix in [('', 'tide','dark','')]+[(f'{t}-{m}/',t,m,'../') for t,m in THEMES]:
        for filename in PAGES:out[folder+filename]=app_page(filename,theme,mode,prefix)
        for filename in REVIEWS:out[folder+filename]=review_page(filename,theme,mode,prefix)
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    stale=[]
    for filename,html in outputs().items():
        path=ROOT/filename
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=html:stale.append(filename)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(html,encoding='utf-8')
    if stale:raise SystemExit('Stale HTML: '+', '.join(stale))
    print(f'{len(outputs())} responsive HTML documents '+('current.' if args.check else 'built.'))
