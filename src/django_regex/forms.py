# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import re

import six
from django import forms
from django.db.models import TextField
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from .validators import RegexValidator, RegexValidatorEnh, OptionValidator, FLAGS
from .exceptions import InvalidPatternValidationError

logger = logging.getLogger(__name__)


class RegexFormField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(RegexFormField, self).__init__(*args, **kwargs)
        self.validators.append(RegexValidator())

    def validate(self, value):
        if value in self.empty_values and self.required:
            raise InvalidPatternValidationError(self.error_messages['required'], code='required')

    def prepare_value(self, value):
        if value is None:
            return None
        if isinstance(value, six.string_types):
            return value

        return value.pattern

    def to_python(self, value):
        """Return a string."""
        if value is None:
            return None
        if isinstance(value, six.string_types):
            return value
        return value.pattern


SEP = chr(0)


def compress(data_list):
    if data_list:
        return SEP.join(data_list)


def decompress(value):
    if value:
        return value.split(chr(0))
    return [None, None]

def get_options(value):
    ret = 0
    if 'I' in value:
        ret += re.IGNORECASE
    if 'M' in value:
        ret += re.MULTILINE
    if 'D' in value:
        ret += re.DOTALL
    if 'V' in value:
        ret += re.VERBOSE
    return ret


class RegexWidgetEnh(forms.MultiWidget):
    """
    Widget containing two select boxes for selecting the month and year.
    """
    template_name = 'django/forms/widgets/multiwidget.html'

    def decompress(self, value):
        return decompress(value)


class OptionFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = len(FLAGS)
        super(OptionFormField, self).__init__(*args, **kwargs)
        self.validators.append(OptionValidator())

class RegexFormFieldEnh(forms.MultiValueField):
    """
    Form field that validates credit card expiry dates.
    """

    default_error_messages = {
        'invalid_regex': _(u'Please enter a valid regular expression.'),
        'invalid_year': _(u'Please enter a valid year.'),
        'date_passed': _(u'This expiry date has passed.'),
    }

    def __init__(self, *args, **kwargs):
        error_messages = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            error_messages.update(kwargs['error_messages'])
        if 'initial' not in kwargs:
            pass
        fields = (
            forms.CharField(widget=Textarea,
                            error_messages={'invalid': error_messages['invalid_regex']}),
            OptionFormField(),
            # forms.BooleanField(label='ignore_case'),
            # forms.BooleanField(label='make anchors look for newline'),
        )
        super(RegexFormFieldEnh, self).__init__(fields, *args, **kwargs)
        self.widget = RegexWidgetEnh(widgets=[fields[0].widget,
                                              fields[1].widget,
                                              # fields[2].widget
                                              ])
        self.validators.append(RegexValidatorEnh())

    # def clean(self, value):
    #     expiry_date = super(RegexFormFieldEnh, self).clean(value)
    #     if date.today() > expiry_date:
    #         raise forms.ValidationError(self.error_messages['date_passed'])
    #     return expiry_date

    def compress(self, data_list):
        return compress(data_list)
