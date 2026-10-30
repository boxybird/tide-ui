"""Compact generated application CSS without rewriting values or source modules."""
import re


def compact_gap(source):
    compact = re.sub(r':\s+', ':', re.sub(r'\s*([;{}])\s*', r'\1', source))
    # The final declaration separator is optional. Strings/URLs are protected
    # by the caller; removing it changes neither selectors nor declarations.
    return re.sub(r';(?=})', '', compact)


def compact_css(source):
    # Same conservative strategy as Tide's existing distribution compiler:
    # protect strings/URLs, omit ordinary comments and separator indentation.
    tokens = re.compile(r'''\burl\((?:'(?:\\[\s\S]|[^'\\])*'|"(?:\\[\s\S]|[^"\\])*"|\\[\s\S]|[^'"\\)])*\)|'(?:\\[\s\S]|[^'\\])*'|"(?:\\[\s\S]|[^"\\])*"|/\*[\s\S]*?\*/''', re.I)
    pieces = []
    gap = ''
    cursor = 0
    for match in tokens.finditer(source):
        gap += source[cursor:match.start()]
        value = match.group()
        if value.startswith('/*') and not re.search(r'^/\*!|@license|@preserve', value, re.I):
            # Keep a token boundary, then compact the whole gap once. A removed
            # comment must not strand indentation beside a declaration brace.
            gap += ' '
        else:
            pieces.extend((compact_gap(gap), value))
            gap = ''
        cursor = match.end()
    pieces.append(compact_gap(gap + source[cursor:]))
    return ''.join(pieces)
