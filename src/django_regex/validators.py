# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import re

import six
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

FLAGS = {
    'I': re.IGNORECASE,
    'M': re.MULTILINE,
    'L': re.LOCALE,
    'S': re.DOTALL,
    'U': re.UNICODE,
    'V': re.VERBOSE,
}

OPTIONS = (
    (int(re.I), _('ignore case (IGNORECASE)')),
    (int(re.M), _('make anchors look for newline (MULTILINE)')),
    (int(re.M), _('assume current 8-bit locale (LOCALE)')),
    (int(re.S), _('make dot match newline (DOTALL)')),
    (int(re.U), 'assume unicode locale (UNICODE)'),
    (int(re.X), _('ignore whitespace and comments (VERBOSE)')),
)

Regex = type(re.compile(''))

DEFAULT_SEPARATOR = getattr(settings, 'DJANGO_REGEX_SEPARATOR', chr(1))


def compress(data_list, separator=None):
    sep = separator or DEFAULT_SEPARATOR
    if data_list in [None, [], ()]:
        return sep.join(['', '0'])
    pattern, flags = data_list
    return sep.join([pattern, str(value_to_flags(flags))])


def decompress(value, separator=None):
    sep = separator or DEFAULT_SEPARATOR
    if value is None:
        return [None, 0]
    if isinstance(value, Regex):
        return value.pattern, value_to_flags(value.flags)

    try:
        pattern, flags = value.split(sep)
    except ValueError:
        return value, 0
    return pattern, value_to_flags(flags)


def flags_to_value(value):
    out = []
    int_value = int(value)
    if int_value & re.IGNORECASE:  # SRE_FLAG_IGNORECASE = 2
        out.append(int(re.IGNORECASE))
    if int_value & re.MULTILINE:  # SRE_FLAG_MULTILINE = 8
        out.append(int(re.MULTILINE))
    if int_value & re.DOTALL:  # SRE_FLAG_MULTILINE = 16
        out.append(int(re.DOTALL))
    if int_value & re.UNICODE:  # SRE_FLAG_UNICODE = 32
        out.append(int(re.UNICODE))
    if int_value & re.VERBOSE:  # SRE_FLAG_VERBOSE = 64
        out.append(int(re.VERBOSE))
    return out


def value_to_flags(value):
    """

    :param value: int, string, list ->
    :return:
    >>> value_to_flags(0) == 0
    >>> value_to_flags("0") == 0
    >>> value_to_flags("i") == 2
    >>> value_to_flags([2]) == 2
    >>> value_to_flags(['I']) == 2

    """
    if not value:
        return 0
    try:
        return int(value)
    except (ValueError, TypeError):
        pass

    if isinstance(value, six.string_types):
        value = [FLAGS[x.upper()] for x in value if x.upper() in FLAGS]

    return sum(map(int, value))


@deconstructible
class RegexValidator(object):
    message = _("`%(pattern)s` is not a valid regular expression")
    code = 'regex'

    def __call__(self, value):
        try:
            re.compile(value)
        except Exception:
            raise ValidationError(self.message,
                                  code=self.code,
                                  params={'pattern': value})
