"""Canonical shared shell; consumed by static kit fixtures and the app copy.

Body/actions are trusted authored HTML, never unsanitized user content.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def panel(*, opening, closing, body='', actions='', header='', count='', reset_attributes='', body_attributes=''):
    source = (ROOT/'templates/filter-panel.html').read_text(encoding='utf-8')
    for key, value in {'OPEN':opening, 'CLOSE':closing, 'HEADER':header, 'BODY':body,
                       'ACTIONS':actions, 'COUNT':escape(count), 'RESET_ATTRIBUTES':reset_attributes,
                       'BODY_ATTRIBUTES':body_attributes}.items():
        source = source.replace('{{'+key+'}}', value)
    return source


def header(title_id='responsive-filter-title', level=2):
    return f'''<header class="tide-filter-panel__header">
<h{level} class="tide-filter-panel__title" id="{title_id}" tabindex="-1">Search &amp; filters</h{level}>
<button class="tide-button tide-button--quiet tide-button--icon" type="button" aria-label="Cancel search and filter changes" data-filter-close><svg class="tide-icon" viewBox="0 0 15 15" fill="none" aria-hidden="true" focusable="false"><path d="m4 4 7 7M11 4l-7 7" stroke="currentColor" stroke-linecap="round" stroke-width="1.25"/></svg></button>
<p class="tide-filter-panel__description">Find an event or narrow the lineup. Changes apply together.</p></header>'''


def specimen(level=2):
    body = '''<form class="tide-field" id="filter-example" action="{{FRAMES}}filter-panel.html" method="get">
<label class="tide-field__label" for="example-query">Search events</label>
<input class="tide-field__control" id="example-query" name="q" type="search" placeholder="Music, workshops, a place…" maxlength="160"></form>
<fieldset class="tide-fieldset tide-stack"><legend class="tide-fieldset__legend">When</legend>
<p class="tide-field__hint" id="example-date-hint">Dates are inclusive and local to Albuquerque.</p>
<div class="tide-field"><label class="tide-field__label" for="example-from">From</label><input class="tide-field__control" id="example-from" name="from" type="date" form="filter-example" aria-describedby="example-date-hint"></div>
<div class="tide-field"><label class="tide-field__label" for="example-to">Through</label><input class="tide-field__control" id="example-to" name="to" type="date" form="filter-example" aria-describedby="example-date-hint"></div></fieldset>
<fieldset class="tide-fieldset tide-stack"><legend class="tide-fieldset__legend">Category</legend>
<label class="tide-choice"><input type="checkbox" name="category" value="music" form="filter-example">Music</label>
<label class="tide-choice"><input type="checkbox" name="category" value="comedy" form="filter-example">Comedy</label>
<label class="tide-choice"><input type="checkbox" name="category" value="workshop" form="filter-example">Workshops</label></fieldset>'''
    return panel(opening='<section class="tide-filter-panel" aria-label="Filter panel specimen">', closing='</section>',
                 body=body, header=header('example-panel-title',level), count='48 matching events', reset_attributes=' disabled',
                 actions='<button class="tide-button tide-button--full" type="submit" form="filter-example">Show 48 events</button>')
