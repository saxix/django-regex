# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import six
from django import forms
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from .exceptions import InvalidPatternValidationError
from .validators import (
    OPTIONS, Regex, RegexValidator, compress, decompress, flags_to_value
)

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
        # if value is None:
        #     return None
        # if isinstance(value, six.string_types):
        return value
        # return value.pattern


class RegexFlagsWidget(forms.MultiWidget):
    template_name = 'django_regex/widgets/regex.html'

    def __init__(self, widgets, attrs=None):
        super(RegexFlagsWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        pattern, flags = decompress(value)
        return pattern, flags_to_value(flags)


class FlagsInput(CheckboxSelectMultiple):
    template_name = 'django_regex/widgets/flag.html'


class FlagsField(forms.MultipleChoiceField):
    pass


# class OptionFormField(forms.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs['max_length'] = len(FLAGS)
#         super(OptionFormField, self).__init__(*args, **kwargs)
#         self.validators.append(OptionValidator())
#


class RegexFlagsFormField(forms.MultiValueField):
    """
    Form field that validates credit card expiry dates.
    """

    default_error_messages = {
        'invalid_regex': _(u'Please enter a valid regular expression.'),
    }

    def __init__(self, *args, **kwargs):
        error_messages = self.default_error_messages.copy()
        kwargs['require_all_fields'] = False
        self.flags_separator = kwargs.pop('flags_separator', None)

        if 'error_messages' in kwargs:  # pragma: no cover
            error_messages.update(kwargs['error_messages'])
        fields = (
            RegexFormField(error_messages={'invalid': error_messages['invalid_regex']}),
            FlagsField(required=False,
                       choices=OPTIONS,
                       widget=FlagsInput)
        )
        super(RegexFlagsFormField, self).__init__(fields, *args, **kwargs)
        self.widget = RegexFlagsWidget(widgets=[fields[0].widget,
                                                fields[1].widget,
                                                ])
        # self.validators.append(RegexValidatorEnh())

    def compress(self, data_list):
        return compress(data_list, self.flags_separator)

    def prepare_value(self, value):
        out = value
        if isinstance(value, Regex):
            out = compress([value.pattern, value.flags], self.flags_separator)
        #     if value == [None,None]:
        #         value = ['', '']
        if isinstance(value, list):
            out = compress(value, self.flags_separator)
        return out

    # def to_python(self, value):
    #     return value
    #     """Return a string."""
    #     if value is None:
    #         return None
    #     if isinstance(value, six.string_types):
    #         return value
    #     return value.pattern
