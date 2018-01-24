# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

import six
from django import forms

from .exceptions import InvalidPatternValidationError

logger = logging.getLogger(__name__)


class RegexFormField(forms.CharField):
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
