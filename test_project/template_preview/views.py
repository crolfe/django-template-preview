import os

from functools import reduce

from django.conf import settings
from django.shortcuts import render
from django.template import loader
from django.template.base import VariableNode
from django.utils import dateparse
from django.views.generic import TemplateView

from .constants import DATE, DATETIME, STRING
from .forms import TemplateForm

template_path = os.path.join(os.path.abspath('.'), settings.TEMPLATE_PREVIEW_DIR)
templates = [f for f in os.listdir(template_path)
             if os.path.isdir(os.path.join(template_path, f))]

print(templates)
print(template_path)


class TemplateListView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['templates'] = templates
        return context


def _template_vars(template):
    """
    `contents` could be a dotted path, which means the variable
    is a nested object
    """
    nodes = template.template.nodelist

    variables = []
    for node in nodes:
        if isinstance(node, VariableNode):
            # need to remove any filters attached to the variable name
            var = node.token.contents.split('|')
            variables.append(var[0])
    return variables
    # return [n.token.contents for n in nodes if isinstance(n, VariableNode)]


_format_funcs = {
    DATE: lambda x: dateparse.parse_date(x),
    DATETIME: lambda x: dateparse.parse_datetime(x),
    STRING: lambda x: x
}


def _traverse(tokens, value):
    context = {}
    head, tail = tokens[0], tokens[1:]

    if not tail:

        context[head] = value
    else:
        context[head] = _traverse(tail, value)

    return context


def _build_context(form_data):
    """
    transforms a dict with dotted paths for keys into a nested dictionary
    e.g. {'user.firstName': 'Bob', 'user.lastName': 'Loblaw'}
    becomes {'user': {'firstname': Bob', 'lastName': 'Loblaw'}}
    """
    nested_values = []
    types = {}
    for key, value in form_data.items():
        if key.endswith('_typehint'):
            # this is metadata that shouldn't be part of the template context
            key = key[:-9]
            types[key] = value

    for key, value in form_data.items():
        if key not in types:
            continue  # skip any of the typehints

        tokens = key.split('.')
        func = _format_funcs[types[key]]
        value = func(value)

        nested_value = _traverse(tokens, value)
        nested_values.append(nested_value)

    if nested_values:
        return reduce(_merge_dicts, nested_values)

    return {}


def _merge_dicts(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge_dicts(a[key], b[key], path + [key])
            elif a[key] == b[key]:
                pass
            else:
                joined = '.'.join(path, key)
                raise Exception("Conflicting values at {}".format(joined))
        else:
            a[key] = b[key]

    return a


def email_template_render_view(request, template_name, template_dir=None):
    path = os.path.join(template_path, '{}/body.html'.format(template_name))
    template = loader.get_template(path)
    template_vars = _template_vars(template)
    rendered = None

    if request.method == 'GET':
        form = TemplateForm(variables=template_vars)
    elif request.method == 'POST':
        form = TemplateForm(request.POST, variables=template_vars)
        if form.is_valid():
            data = _build_context(form.cleaned_data)
            rendered = template.render(data)

    context = {'form': form, 'rendered': rendered, 'email_template_name': template_name}

    return render(request, 'edit_detail.html', context)
