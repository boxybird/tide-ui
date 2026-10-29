"""Compact generated application CSS without rewriting values or source modules."""
import re


def compact_gap(source):
    return re.sub(r':\s+', ':', re.sub(r'\s*([;{}])\s*', r'\1', source))


def compact_css(source):
    # Same conservative strategy as Tide's existing distribution compiler:
    # protect strings/URLs, omit ordinary comments and separator indentation.
    tokens = re.compile(r'''\burl\((?:'(?:\\[\s\S]|[^'\\])*'|"(?:\\[\s\S]|[^"\\])*"|\\[\s\S]|[^'"\\)])*\)|'(?:\\[\s\S]|[^'\\])*'|"(?:\\[\s\S]|[^"\\])*"|/\*[\s\S]*?\*/''', re.I)
    pieces = []
    cursor = 0
    for match in tokens.finditer(source):
        gap = source[cursor:match.start()]
        pieces.append(compact_gap(gap))
        value = match.group()
        pieces.append(' ' if value.startswith('/*') and not re.search(r'^/\*!|@license|@preserve', value, re.I) else value)
        cursor = match.end()
    pieces.append(compact_gap(source[cursor:]))
    return ''.join(pieces)
