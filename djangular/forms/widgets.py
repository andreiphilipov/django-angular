# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join
from django.forms.util import flatatt


class CheckboxChoiceInput(widgets.CheckboxChoiceInput):
    def tag(self):
        name = '{0}.{1}'.format(self.name, self.choice_value)
        tag_attrs = dict(self.attrs, type=self.input_type, name=name, value=self.choice_value)
        if 'id' in self.attrs:
            tag_attrs['id'] = '{0}_{1}'.format(self.attrs['id'], self.index)
        if 'ng-model' in self.attrs:
            tag_attrs['ng-model'] = '{0}.{1}'.format(self.attrs['ng-model'], self.choice_value)
        if self.is_checked():
            tag_attrs['checked'] = 'checked'
        return format_html('<input{0} />', flatatt(tag_attrs))


class CheckboxFieldRenderer(widgets.ChoiceFieldRenderer):
    choice_input_class = CheckboxChoiceInput

    def __init__(self, name, value, attrs, choices):
        attrs.pop('djng-error', None)  # TODO: use for bound forms
        self.field_attrs = [format_html('ng-form="{0}"', name)]
        if attrs.pop('multiple_checkbox_required', False):
            self.field_attrs.append(format_html('validate-multiple-checkbox="{0}"',
                format_html_join(',', '{0}.{1}', ((name, choice) for choice, dummy in choices))))
        super(CheckboxFieldRenderer, self).__init__(name, value, attrs, choices)

    def render(self):
        """
        Outputs a <ul ng-form="name"> for this set of choice fields to nest an ngForm.
        """
        start_tag = format_html('<ul {0}>', mark_safe(' '.join(self.field_attrs)))
        output = [start_tag]
        for widget in self:
            output.append(format_html('<li>{0}</li>', force_text(widget)))
        output.append('</ul>')
        return mark_safe('\n'.join(output))


class CheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    """
    Form fields of type 'MultipleChoiceField' using the widget 'CheckboxSelectMultiple' must behave
    slightly different from the original. This widget overrides the default functionality.
    """
    renderer = CheckboxFieldRenderer

    def implode_multi_values(self, name, data):
        """
        Due to the way Angular organizes it model, when Form data is sent via a POST request,
        then for this kind of widget, the posted data must to be converted into a format suitable
        for Django's Form validation.
        """
        mkeys = [k for k in data.keys() if k.startswith(name + '.')]
        mvls = [data.pop(k)[0] for k in mkeys]
        if mvls:
            data.setlist(name, mvls)

    def convert_ajax_data(self, field_data):
        """
        Due to the way Angular organizes it model, when this Form data is sent using Ajax,
        then for this kind of widget, the sent data has to be converted into a format suitable
        for Django's Form validation.
        """
        return [key for key, val in field_data.items() if val]

    def get_field_attrs(self, field):
        return {'multiple_checkbox_required': field.required}


class RadioFieldRenderer(widgets.RadioFieldRenderer):
    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        output = ['<div>']
        for widget in self:
            output.append(force_text(widget))
        output.append('</div>')
        return mark_safe('\n'.join(output))


class RadioSelect(widgets.RadioSelect):
    """
    Form fields of type 'ChoiceField' using the widget 'RadioSelect' must behave
    slightly different from the original. This widget overrides the default functionality.
    """
    renderer = RadioFieldRenderer

    def get_field_attrs(self, field):
        return {'multiple_checkbox_required': field.required}
