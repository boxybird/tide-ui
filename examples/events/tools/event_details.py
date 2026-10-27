"""Compose existing detail markup from structured sample content."""
from datetime import date
from html import escape
import re
from urllib.parse import urlsplit

from template_engine import Html, attribute

MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


def link_target(value):
    if not value or any(ord(char)<32 for char in value) or urlsplit(value).scheme.lower() not in ('', 'http', 'https', 'tel', 'mailto'):
        raise ValueError('Unsupported detail link target')
    return value


class EventDetails:
    def __init__(self, partial, presentations):
        self.partial = partial
        self.presentations = presentations

    def block(self, block, icon):
        kind = block['type']
        if kind=='paragraph':
            return self.partial('detail-paragraph', {'TEXT':block['text']})
        if kind=='place':
            lines = []
            for line in block['lines']:
                lines.append(self.partial('detail-place-line', {'TEXT':line['text']}) if line.get('wrapped') else Html(escape(line['text'])))
            return self.partial('detail-place', {'LINES':Html('<br>'.join(lines))})
        if kind=='inclusions':
            items = Html(''.join(self.partial('detail-inclusion', {'TEXT':text, 'CHECK_ICON':icon('check')}) for text in block['items']))
            return self.partial('detail-inclusions', {'ITEMS':items})
        if kind=='schedule':
            items = Html(''.join(self.partial('detail-schedule-item', {'LABEL':label, 'TEXT':text}) for label, text in block['items']))
            return self.partial('detail-schedule', {'ITEMS':items})
        if kind=='attendance':
            paragraphs = Html(''.join(self.partial('detail-paragraph', {'TEXT':text}) for text in block['paragraphs']))
            return self.partial('detail-attendance', {'PARAGRAPHS':paragraphs})
        if kind=='link':
            return self.partial('detail-venue-action', {'HREF':link_target(block['href']), 'LABEL':block['label']})
        raise ValueError('Unsupported detail block: ' + kind)

    def render(self, event, level):
        if level not in (1, 2):
            raise ValueError('Detail heading level must be 1 or 2')
        content = event['detail']
        presentation = self.presentations[content['presentation']]
        image = content['image']
        if not re.fullmatch(r'(?:assets|\{\{KIT_ASSETS\}\})/images/[a-z0-9-]+\.(?:png|jpg|webp)', image['src']):
            raise ValueError('Unsupported sample detail image')
        if int(image['width'])<=0 or int(image['height'])<=0:
            raise ValueError('Detail image dimensions must be positive')
        extra = Html(' fill="none" xmlns="http://www.w3.org/2000/svg"' if presentation['fullIconAttributes'] else '')
        def icon(name):
            return self.partial('detail-icon-'+name, {'ICON_EXTRA':extra})
        day = date.fromisoformat(event['date'])
        date_prefix = f'{WEEKDAYS[day.weekday()]}, {MONTHS[day.month-1]} {day.day}'
        date_label = Html(escape(date_prefix) + (self.partial('detail-note', {'TEXT':', '+str(day.year)}) if presentation['yearNote'] else ', '+str(day.year)))
        times = Html(escape(content.get('timeSeparator', '')).join(self.partial('detail-time', {'DATETIME':item['datetime'], 'TEXT':item['text']}) for item in content['times']))
        duration = self.partial('detail-note', {'TEXT':content['durationNote']}) if content.get('durationNote') else Html('')
        venue = self.partial('detail-venue-link', {'HREF':link_target(content['venueHref']), 'TEXT':event['venueLabel']}) if content.get('venueHref') else Html(escape(event['venueLabel']))
        sections = []
        for section in content['sections']:
            section_id = section.get('id')
            if section_id and not re.fullmatch(r'[a-z][a-z0-9-]*', section_id):
                raise ValueError('Invalid detail section ID')
            sections.append(self.partial('detail-section', {
                'SECTION_LEVEL':level+2, 'TITLE':section['title'],
                'SECTION_ATTRIBUTES':Html(str(attribute('id', section_id))+' tabindex="-1"') if section_id else Html(''),
                'BLOCKS':Html(''.join(self.block(block, icon) for block in section['blocks'])),
            }))
        values = {
            'PHOTO_SRC':image['src'], 'PHOTO_ALT':image['alt'], 'PHOTO_WIDTH':image['width'], 'PHOTO_HEIGHT':image['height'],
            'PHOTO_LOADING':'eager' if level==1 else 'lazy', 'PHOTO_PRIORITY':'high' if level==1 else 'auto',
            'BACK_ICON':icon('back'),
            'SAVED_CONTROL':self.partial('detail-saved-control', {'SAVED_ICON':icon('saved')}) if presentation['savedControl'] else Html(''),
            'CATEGORY':event['categoryLabel'], 'AGE':self.partial('detail-age', {'AGE':content['age']}) if content.get('age') else Html(''),
            'DETAIL_LEVEL':level, 'STORY_LEVEL':level+1, 'TITLE':event['title'],
            'TITLE_ATTRIBUTES':Html(' tabindex="-1"') if presentation['focusTitle'] else Html(''),
            'SUBTITLE':content['subtitle'], 'DATE':event['date'], 'DATE_LABEL':date_label,
            'DATE_ICON':icon('calendar'), 'TIME_ICON':icon('clock'), 'VENUE_ICON':icon('pin'),
            'TIMES':times, 'DURATION_NOTE':duration, 'VENUE':venue, 'PRICE':event['price'],
            'PRICE_UNIT':self.partial('detail-price-unit', {'TEXT':presentation['priceUnit']}) if presentation.get('priceUnit') else Html(''),
            'ADMISSION_NOTE':content['admissionNote'], 'PLAN_LABEL':presentation['planLabel'], 'PLAN_ICON':icon('arrow-right'),
            'CUE_LABEL':self.partial('detail-cue-label', {'TEXT':content['cueText']}) if presentation['wrappedCue'] else Html(escape(content['cueText'])+' '),
            'CUE_ICON':icon(presentation['cueIcon']),
            'STORY_LABEL':content['storyLabel'], 'STORY_TITLE':content['storyTitle'], 'LEAD':content['lead'],
            'SECTIONS':Html(''.join(sections)), 'DISCLOSURE':presentation['disclosure'],
            'STORY_BACK_ICON':icon('back') if presentation['backIcon'] else Html(''), 'BACK_LABEL':presentation['backLabel'],
        }
        return self.partial('event-detail', values)
