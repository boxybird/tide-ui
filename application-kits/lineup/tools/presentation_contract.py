"""Lineup's strict component-adoption boundary, beyond Tide's consumer exceptions.

Private hosts may compose components. They cannot restyle public interiors,
including through aliases, generic descendants, inherited type or token changes.
This small scanner supports the grouping rules/selectors used by Lineup; it is
not a general CSS engine. Rendered browser comparisons verify the cascade too.
"""
from html.parser import HTMLParser
import re

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
TYPE = {'font', 'font-family', 'font-size', 'font-style', 'font-weight', 'line-height', 'letter-spacing', 'text-transform'}
HOST = {'position', 'inset', 'inset-block-start', 'inset-inline-start',
        'inline-size', 'min-inline-size', 'max-inline-size', 'block-size', 'min-block-size', 'max-block-size',
        'margin', 'margin-inline', 'margin-inline-start', 'margin-block', 'margin-block-start', 'margin-block-end',
        'grid-column', 'grid-row', 'align-self', 'justify-self', 'isolation',
        'scroll-margin-block-start', 'scroll-padding-block-start', 'overflow-y', 'scrollbar-width', 'scrollbar-gutter'}
# Responsive availability and native-popover placement are host responsibilities.
AVAILABILITY = {
    'tide-button': {'none', 'inline-flex'},
    'tide-filter-panel__header': {'none', 'grid'},
    'tide-filter-panel': {'none', 'grid'},
    'tide-empty': {'none', 'grid'},
    'tide-link': {'none'},
    'tide-skip-link': {'none', 'block'},
    'tide-event-card__status': {'none', 'inline-flex'},
    'tide-event-hero__toolbar': {'none'},
}


def private_class(name, private):
    return any(name == block or name.startswith((block+'__', block+'--')) for block in private)


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(); self.nodes = []; self.stack = []; self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = {'tag':tag, 'attrs':dict(attrs), 'parents':tuple(self.stack)}
        node['classes'] = set(node['attrs'].get('class', '').split())
        self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, -1, -1):
            if self.stack[index]['tag'] == tag:
                del self.stack[index:]; break


def split_selectors(text):
    depth = start = 0
    for index, char in enumerate(text):
        depth += (char == '(') - (char == ')')
        if char == ',' and depth == 0:
            yield text[start:index].strip(); start = index+1
    yield text[start:].strip()


def subject(selector):
    # Ignore ancestor classes and condition-only :has/:not arguments.
    selector = re.sub(r':(?:has|not)\([^()]*\)', '', selector)
    depth = start = 0
    for index, char in enumerate(selector):
        depth += (char == '(') - (char == ')')
        if depth == 0 and (char.isspace() or char in '>+~'):
            start = index+1
    return selector[start:]


def strict_style_issues(html, rules, private):
    aliases = {}
    for node in Tree(html).nodes:
        shared = {c for c in node['classes'] if c.startswith('tide-') and c != 'tide' and not private_class(c, private)}
        for name in node['classes']:
            if private_class(name, private):
                aliases.setdefault(name, set()).update(shared)
    issues = set()
    for selectors, declarations in rules:
        for selector in split_selectors(selectors):
            target = subject(selector)
            names = set(re.findall(r'\.(tide-[\w-]+)', target))
            shared = {c for c in names if not private_class(c, private)}
            for name in names:
                shared.update(aliases.get(name, ()))
            for declaration in declarations.split(';'):
                prop, value = map(str.strip, declaration.split(':', 1))
                if prop.startswith('--'):
                    if not prop.startswith(('--tide-app-', '--tide-lineup-')):
                        issues.add('Shared token override: '+prop)
                    continue
                # No private lookalike typography/decoration, even on ancestors.
                appearance = prop in TYPE or prop.startswith(('background', 'border', 'outline', 'text-', 'color', 'box-shadow', 'opacity', 'filter', 'fill', 'stroke'))
                shell = not shared and target == '.tide-app__header' and (
                    (prop == 'background' and value == 'var(--tide-color-canvas)') or
                    (prop == 'box-shadow' and value == '0 var(--tide-space-6) 0 var(--tide-color-canvas)'))
                if appearance and not shell:
                    issues.add('Private appearance: '+selector+' / '+prop)
                if shared and prop not in HOST:
                    visible = prop == 'display' and any(value in AVAILABILITY.get(c, ()) for c in shared)
                    popover = 'tide-filter-panel' in shared and prop in {'transform', 'transition', 'position-anchor'}
                    if not (visible or popover):
                        issues.add('Shared interior override: '+selector+' / '+prop)
    return sorted(issues)


def primitive_markup_issues(html):
    issues = []
    for node in Tree(html).nodes:
        tag, attrs, classes = node['tag'], node['attrs'], node['classes']
        parents = node['parents']
        if tag == 'button' and not classes & {'tide-button', 'tide-photo-control', 'tide-icon-button', 'tide-save'}:
            issues.append('Button without Tide recipe')
        if tag == 'label' and not classes & {'tide-field__label', 'tide-choice', 'tide-chip'}:
            issues.append('Label without Tide recipe: '+attrs.get('for', ''))
        if tag in ('input', 'select', 'textarea') and attrs.get('type') != 'hidden':
            if attrs.get('type') in ('checkbox', 'radio'):
                if not any(p['classes'] & {'tide-choice', 'tide-chip'} for p in parents):
                    issues.append('Choice without Tide recipe')
            elif attrs.get('type') == 'file':
                if not any('tide-upload' in p['classes'] for p in parents):
                    issues.append('Upload without Tide recipe')
            elif 'tide-field__control' not in classes:
                issues.append('Control without Tide recipe: '+attrs.get('id', ''))
        if 'tide-field__label' in classes:
            field = next((p for p in reversed(parents) if p['classes'] & {'tide-field', 'tide-upload'}), None)
            if field is None:
                issues.append('Field label outside canonical field: '+attrs.get('for', ''))
    return sorted(set(issues))
