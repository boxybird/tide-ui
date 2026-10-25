"""Dependency-free escaped values and registered includes for app templates."""
from html import escape
import re

TOKEN = re.compile(r'{{\s*(?:>\s*([a-z][a-z0-9-]*)|([A-Z][A-Z0-9_]*))\s*}}')


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
