from django import forms
from django.conf import settings

from .constants import DATE, DATETIME, STRING


TYPES = (
    (STRING, 'string'),
    (DATE, 'date'),
    (DATETIME, 'datetime')
)


class TemplateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        variables = kwargs.pop('variables', {})
        super(TemplateForm, self).__init__(*args, **kwargs)

        initial_values = getattr(settings, 'TEMPLATE_PREVIEW_DEFAULTS', {})
        ignore = getattr(settings, 'TEMPLATE_PREVIEW_IGNORE', set())

        # dynamically add fields for the variables defined in a template
        for var in variables:
            if var in ignore:
                continue

            initial = initial_values.get(var, '')

            self.fields[var] = forms.CharField(label=var, required=False, initial=initial)
            typehint = '{}_typehint'.format(var)
            self.fields[typehint] = forms.ChoiceField(choices=TYPES, initial=STRING, required=False)
