"""One-time migration from the approved study to independent BEM source templates.

Normal kit builds never read or mutate previous design collections.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'tide-ui-kit-studies'
MAPPING = dict(pair.split(':') for pair in '''
library:tide-library skip-link:tide-skip-link kit-nav:tide-doc-nav brand:tide-brand edition:tide-doc-nav__edition nav-foot:tide-doc-nav__foot kit-content:tide-doc-content kit-hero:tide-doc-hero kicker:tide-eyebrow row:tide-row btn:tide-button icon:tide-icon hero-card:tide-doc-anchor event-card:tide-event-card card-hit-area:tide-event-card__link sr-only:tide-sr-only card-content:tide-event-card__content card-copy:tide-event-card__copy card-heading-row:tide-event-card__heading category:tide-eyebrow save-mark:tide-event-card__save card-title:tide-event-card__title venue:tide-event-card__venue card-meta:tide-event-card__meta event-date:tide-date date-day:tide-date__day date-small:tide-date__parts meta-separator:tide-event-card__separator price:tide-event-card__price hero-card-label:tide-doc-anchor__caption kit-section:tide-doc-section section-heading:tide-doc-heading doc-grid:tide-doc-grid doc-panel:tide-doc-panel fine:tide-caption swatches:tide-doc-swatches swatch:tide-doc-swatch swatch-label:tide-doc-swatch-label type-row:tide-doc-type space-row:tide-doc-space space-bar:tide-doc-space__bar rule-list:tide-doc-rules stack:tide-stack component-label:tide-doc-label icon-btn:tide-icon-button chips:tide-chip-list chip:tide-chip field:tide-field native-choice:tide-choice badge:tide-badge notice:tide-notice toast-sample:tide-toast organizer:tide-organizer muted:tide-u-muted text-link:tide-link partner:tide-partner partner-label:tide-partner__label screen-grid:tide-doc-screens screen-study:tide-doc-screen coverage:tide-doc-table kit-footer:tide-doc-footer screen:tide-screen event-screen:tide-screen--event event-hero:tide-event-hero hero-photo:tide-event-hero__photo photo-shade:tide-event-hero__scrim event-toolbar:tide-event-hero__toolbar round-control:tide-photo-control save-preview:tide-photo-control--save-preview hero-content:tide-event-hero__content event-intro:tide-event-hero__intro subtitle:tide-event-hero__subtitle event-facts:tide-event-hero__facts fact-note:tide-event-hero__note place-note:tide-event-hero__place-note admission:tide-event-hero__admission primary-action:tide-button detail-cue:tide-event-hero__cue full-details:tide-event-details detail-section:tide-event-details__section inclusions:tide-inclusions schedule:tide-schedule place:tide-place demo-disclosure:tide-disclosure back-link:tide-back-link list-screen:tide-screen--list list-content:tide-list list-header:tide-list__header brand-row:tide-list__brand-row saved-label:tide-saved-link context-row:tide-list__context location:tide-list__location date-context:tide-list__date-context event-list:tide-event-list list-footer:tide-list__footer kit-screen:tide-screen--kit appbar:tide-appbar page-intro:tide-page-intro page-body:tide-page-body form-section:tide-form-section form-actions:tide-form-actions screen-footer:tide-screen-footer empty:tide-empty fallback-panel:tide-fallback missing-label:tide-fallback__label summary-list:tide-summary result-label:tide-results search-line:tide-search-line state-block:tide-state split:tide-split upload-field:tide-upload error-text:tide-field__error
'''.split())
MODS = {'secondary', 'quiet', 'full', 'selected', 'demo-focus', 'success', 'warning', 'danger', 'error', 'spaced', 'wide'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Migrator(HTMLParser):
    def __init__(self, is_doc):
        super().__init__(convert_charrefs=False)
        self.out, self.stack, self.is_doc = [], [], is_doc
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        originals = attrs.get('class', '').split()
        classes = []
        for item in originals:
            if item == 'date-inline':
                continue
            if item == 'lead':
                classes.append('tide-doc-hero__lead' if self.is_doc else 'tide-event-details__lead')
            elif item in MODS:
                block = next((MAPPING[key] for key in originals if key in ['btn', 'icon-btn', 'chip', 'badge', 'notice', 'page-body', 'doc-panel']), None)
                if not block:
                    raise ValueError((tag, originals, item))
                classes.append(block + '--' + ('focus-sample' if item == 'demo-focus' else item))
            else:
                classes.append(MAPPING[item])
        if tag == 'body':
            classes.insert(0, 'tide')
        if 'primary-action' in originals:
            classes.append('tide-button--plan')
        if 'coverage' in originals:
            classes.append('tide-doc-table--coverage')
        ancestors = [c for _, cs in self.stack for c in cs]
        if 'tide-field' in ancestors:
            if tag in {'input', 'select', 'textarea'} and attrs.get('type') not in {'checkbox', 'radio', 'file'}:
                classes.append('tide-field__control')
            elif tag == 'label':
                classes.append('tide-field__label')
            elif tag == 'small':
                classes.append('tide-field__hint')
        if tag == 'legend' and 'tide-sr-only' not in classes:
            classes.append('tide-fieldset__legend')
        style = attrs.pop('style', None)
        if style:
            if style == 'margin-top:28px': classes.append('tide-u-mt-7')
            elif style == 'margin-top:32px': classes.append('tide-u-mt-8')
            elif style == 'margin-bottom:32px': classes.append('tide-u-mb-8')
            elif style == 'justify-self:start': classes.append('tide-u-start')
            elif style == 'justify-content:space-between': classes.append('tide-row--between')
            elif style.startswith('background:'):
                key = {'#0f1720':'canvas','#17232e':'surface','#22323d':'raised','#edf2ef':'text-primary','#b2c5c7':'text-secondary','#91d2c8':'accent'}[style[11:]]
                classes.append('tide-doc-swatch--' + key)
            elif style.startswith('font-size:'):
                kind = {'36':'event', '28':'page', '24':'card'}[style.split(':')[1].split('px')[0]]
                classes.append('tide-doc-type--' + kind)
            elif style.startswith('width:'):
                width = int(style.split(':')[1].split('px')[0]) // 16
                classes.append('tide-doc-space__bar--' + str(width))
            else: raise ValueError(style)
        attrs.pop('data-study', None)
        attrs.pop('data-layout', None)
        if classes: attrs['class'] = ' '.join(dict.fromkeys(classes))
        if tag == 'img' and '/icons/' in attrs.get('src', ''):
            svg = (SOURCE / 'assets/icons' / Path(attrs['src']).name).read_text(encoding='utf-8')
            svg = re.sub(r'fill="#[^"]+"', 'fill="currentColor"', svg)
            svg = svg.replace('<svg ', '<svg class="tide-icon" focusable="false" ')
            self.out.append(svg)
            return
        for key in ['src', 'href']:
            if key in attrs and re.search(r'(?:\.\./)*assets/', attrs[key]):
                attrs[key] = re.sub(r'(?:\.\./)*assets/', '{{ASSETS}}', attrs[key])
        if self.is_doc:
            for key in ['src', 'href']:
                if attrs.get(key, '').startswith('frames/'):
                    attrs[key] = '{{FRAMES}}' + attrs[key][7:]
        self.out.append('<' + tag + ''.join(' ' + k + ('' if v is None else '="' + escape(v, quote=True) + '"') for k, v in attrs.items()) + '>')
        if tag not in VOID: self.stack.append((tag, classes))
    def handle_endtag(self, tag):
        self.out.append('</' + tag + '>')
        if self.stack and self.stack[-1][0] == tag: self.stack.pop()
    def handle_data(self, data): self.out.append(data)
    def handle_entityref(self, name): self.out.append('&' + name + ';')
    def handle_charref(self, name): self.out.append('&#' + name + ';')
    def handle_comment(self, data): self.out.append('<!--' + data + '-->')


def migrate(path, is_doc):
    text = path.read_text(encoding='utf-8-sig')
    body = re.search(r'<body\b.*</body>', text, re.S).group()
    if is_doc:
        body = re.sub(r'<section class="kit-switcher".*?</section>', '{{THEME_PICKER}}', body, flags=re.S)
        body = body.replace('href="01-date-line.html"', 'href="{{FRAMES}}01-list.html"')
        body = body.replace('href="README.md"', 'href="{{BASE}}README.md"').replace('href="tokens.json"', 'href="{{BASE}}tokens/resolved.json"').replace('href="screen-map.json"', 'href="{{BASE}}screen-map.json"')
        body = re.sub(r'<code>#[0-9A-F]+</code>', '<code>{{SWATCH}}</code>', body)
    migrator = Migrator(is_doc)
    migrator.feed(body)
    out = ''.join(migrator.out)
    if is_doc:
        roles = iter(['canvas','surface','raised','text-primary','text-secondary','accent'])
        out = re.sub(r'\{\{SWATCH\}\}', lambda m: '--tide-color-' + next(roles), out)
        out = out.replace('TIDE · PALETTE STUDIES', 'TIDE · HTML / CSS KIT · 1.0')
        out = out.replace('Tide / Interface library', '{{THEME_NAME}} / {{MODE_NAME}} · Interface library')
        out = out.replace('A considered foundation for everything around the event. Built from the Date Line you chose, with the original list and full-screen event preserved.', 'One structure. Three themes. Light and dark, thoughtfully paired. The Tide you chose, now a reusable HTML and CSS system.')
        out = out.replace('THE ANCHOR / Original card anatomy, unchanged', 'THE ANCHOR / Tide geometry · semantic color roles')
        out = out.replace('Static HTML · 22 Oct 2026', '{{THEME_NAME}} · {{MODE_NAME}}<br>Pure HTML / CSS · 1.0')
        out = out.replace('New</p>', 'Pattern</p>')
        out = out.replace('Tide / Palette studies · Static HTML.', 'Tide / HTML + CSS kit 1.0 · Static HTML.')
        out = out.replace('Source of truth: the approved Date Line frames.', 'BEM components · OKLCH themes · validated foreground/surface pairs.')
        out = out.replace('<a href="#coverage"><span>04</span>Coverage</a>', '<a href="#coverage"><span>04</span>Coverage</a><a href="#tokens"><span>05</span>Tokens</a><a href="#themes"><span>06</span>Themes</a><a href="#extend"><span>07</span>Extend</a>')
        out = out.replace('<footer class="tide-doc-footer">', '{{CONTRACT_SECTIONS}}<footer class="tide-doc-footer">')
        out = out.replace('View Tide reference', 'Open event list')
        out = out.replace('class="tide-field__hint" id="specimen-venue-note"', 'class="tide-field__hint tide-field__error" id="specimen-venue-note"')
    return out


if __name__ == '__main__':
    destination = ROOT / 'templates'
    (destination / 'frames').mkdir(parents=True, exist_ok=True)
    (destination / 'library.html').write_text(migrate(SOURCE / 'index.html', True), encoding='utf-8')
    for path in (SOURCE / 'frames').glob('*.html'):
        (destination / 'frames' / path.name).write_text(migrate(path, False), encoding='utf-8')
    print('Imported BEM templates; future builds are independent of earlier studies.')
