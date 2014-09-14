# -*- coding: utf-8 -*-
from django.forms import fields
from django.forms import widgets
from django.utils.encoding import force_text
from djangular.forms import field_mixins
from . import widgets as bs3widgets


class BooleanFieldMixin(field_mixins.BooleanFieldMixin):
    def get_converted_widget(self):
        assert(isinstance(self, fields.BooleanField))
        if isinstance(self.widget, widgets.CheckboxInput):
            self.widget_css_classes = None
            if not isinstance(self.widget, bs3widgets.CheckboxInput):
                new_widget = bs3widgets.CheckboxInput()
                new_widget.__dict__ = self.widget.__dict__
                # the label shall be rendered by the Widget class rather than using BoundField.label_tag()
                new_widget.choice_label = force_text(self.label)
                self.label = ''
                return new_widget


class ChoiceFieldMixin(field_mixins.ChoiceFieldMixin):
    def get_converted_widget(self):
        assert(isinstance(self, fields.ChoiceField))
        if isinstance(self.widget, widgets.CheckboxInput):
            raise RuntimeError('Shouls never reach this')
            self.widget_css_classes = None
            if not isinstance(self.widget, bs3widgets.CheckboxInput):
                new_widget = bs3widgets.CheckboxInput()
                new_widget.__dict__ = self.widget.__dict__
                # the label shall be rendered by the Widget class rather than using BoundField.label_tag()
                new_widget.choice_label = force_text(self.label)
                self.label = ''
                return new_widget
        if isinstance(self.widget, widgets.RadioSelect):
            self.widget_css_classes = None
            if not isinstance(self.widget, bs3widgets.RadioSelect):
                new_widget = bs3widgets.RadioSelect()
                new_widget.__dict__ = self.widget.__dict__
                return new_widget


class MultipleChoiceFieldMixin(field_mixins.MultipleChoiceFieldMixin):
    def get_converted_widget(self):
        assert(isinstance(self, fields.MultipleChoiceField))
        if isinstance(self.widget, widgets.CheckboxSelectMultiple):
            self.widget_css_classes = None
            if not isinstance(self.widget, bs3widgets.CheckboxSelectMultiple):
                new_widget = bs3widgets.CheckboxSelectMultiple()
                new_widget.__dict__ = self.widget.__dict__
                return new_widget


#             if isinstance(field.widget, widgets.CheckboxSelectMultiple):
#                 if not isinstance(field.widget, bs3widgets.CheckboxSelectMultiple):
#                     field.widget = bs3widgets.CheckboxSelectMultiple()
#                     field.widget.__dict__ = fw_dict
#                 if isinstance(data, QueryDict):
#                     data = field.widget.implode_multi_values(name, data.copy())
#                 setattr(field, 'widget_css_classes', None)
#             elif isinstance(field.widget, widgets.CheckboxInput):
#                 if not isinstance(field.widget, bs3widgets.CheckboxInput):
#                     field.widget = bs3widgets.CheckboxInput()
#                     field.widget.__dict__ = fw_dict
#                     # the label shall be rendered by the Widget class rather than using BoundField.label_tag()
#                     field.widget.choice_label = force_text(field.label)
#                     field.label = ''
#                 setattr(field, 'widget_css_classes', None)
#             elif isinstance(field.widget, widgets.RadioSelect):
#                 if not isinstance(field.widget, bs3widgets.RadioSelect):
#                     field.widget = bs3widgets.RadioSelect()
#                     field.widget.__dict__ = fw_dict
#                 setattr(field, 'widget_css_classes', None)
