"""Compose the existing submission fields without adding form behavior."""
import re

from template_engine import Html, attribute


class FormFields:
    def __init__(self, partial):
        self.partial = partial

    def render(self, field):
        if set(field) - {'id', 'name', 'label', 'control', 'type', 'required', 'optional', 'hint', 'maxlength', 'autocomplete', 'options'}:
            raise ValueError('Unsupported submission field property')
        for key in ('id', 'name'):
            if not re.fullmatch(r'[a-z][a-z0-9-]*', field[key]):
                raise ValueError('Invalid submission field '+key)
        kind = field['control']
        if kind not in ('input', 'textarea', 'select'):
            raise ValueError('Unsupported submission control')
        if kind=='input' and field.get('type') not in ('text', 'email', 'date', 'time'):
            raise ValueError('Unsupported submission input type')
        if field.get('optional') and field.get('required'):
            raise ValueError('Optional submission field cannot be required')
        attrs = ' required' if field.get('required') else ''
        if field.get('hint'):
            attrs += attribute('aria-describedby', field['id']+'-hint')
        for key in ('maxlength', 'autocomplete'):
            if key in field:
                attrs += attribute(key, field[key])
        values = {
            'FIELD_ID':field['id'], 'FIELD_NAME':field['name'], 'FIELD_LABEL':field['label'],
            'FIELD_TYPE':field.get('type', ''), 'FIELD_ATTRIBUTES':Html(attrs),
            'FIELD_OPTIONAL':self.partial('form-optional', {}) if field.get('optional') else Html(''),
            'FIELD_HINT':self.partial('form-hint', {'FIELD_ID':field['id'], 'FIELD_HINT_TEXT':field['hint']}) if field.get('hint') else Html(''),
        }
        if kind=='select':
            values['FIELD_OPTIONS'] = Html(''.join(self.partial('form-option', {
                'OPTION_LABEL':option['label'],
                'OPTION_VALUE':attribute('value', option['value']) if 'value' in option else Html(''),
            }) for option in field['options']))
        values['FIELD_CONTROL'] = self.partial('form-'+kind, values)
        return self.partial('form-field', values)
