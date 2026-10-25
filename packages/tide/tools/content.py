"""Shared content-page HTML, consumed by kit fixtures and the app playground."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def help_content(routes):
    html = (ROOT/'templates/content/help.html').read_text(encoding='utf-8')
    for key in ('BROWSE', 'SEARCH', 'SUBMIT', 'EVENT'):
        html = html.replace('{{'+key+'}}', escape(routes[key], quote=True))
    if '{{' in html:
        raise ValueError('Unresolved help-page route')
    return html
