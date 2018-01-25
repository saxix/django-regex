# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from django_regex.exceptions import InvalidPatternValidationError

logger = logging.getLogger(__name__)

# flags
FLAGS = {
    'I': re.IGNORECASE,
    # 'L': re.LOCALE,
    # 'U': re.UNICODE,
    'M': re.MULTILINE,
    'D': re.DOTALL,
    'V': re.VERBOSE,
}
OPTIONS = {
    re.IGNORECASE: 'ignore case',
    re.LOCALE: 'assume current 8-bit locale',
    re.UNICODE: 'assume unicode locale',
    re.MULTILINE: 'make anchors look for newline',
    re.DOTALL: 'make dot match newline',
    re.VERBOSE: 'ignore whitespace and comments',
}


@deconstructible
class RegexValidator(object):
    message = _('Enter a valid regular expression pattern')
    code = 'regex'

    def __call__(self, value):
        try:
            re.compile(value)
        except Exception:
            raise InvalidPatternValidationError(self.message, code=self.code)


@deconstructible
class OptionValidator(object):
    message = _('Enter a valid regular expression pattern')
    code = 'regex'

    def __call__(self, value):
        opts = set(value)
        if not opts.issubset(FLAGS.keys()):
            raise ValidationError('Invalid Options %s. '
                                  'Valid choices are %s' % (value,
                                                            ",".join(FLAGS.keys())))


@deconstructible
class RegexValidatorEnh(object):
    message = _('Enter a valid regular expression pattern')
    code = 'regex'

    def __call__(self, value):
        if value is None:
            return
        pattern, options = value.split(chr(0))
        opts = set(options)
        # options = "".join(opts)
        if not opts.issubset(FLAGS.keys()):
            raise ValidationError('Invalid Options %s. Valid choices are %s' % (options, FLAGS.keys()))
        try:
            re.compile(pattern)
        except Exception:
            raise InvalidPatternValidationError(self.message, code=self.code)
