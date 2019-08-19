import logging
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from django_regex.utils import Regex, value_to_flags

logger = logging.getLogger(__name__)


OPTIONS = (
    (int(re.I), _('ignore case (IGNORECASE)')),
    (int(re.M), _('make anchors look for newline (MULTILINE)')),
    (int(re.M), _('assume current 8-bit locale (LOCALE)')),
    (int(re.S), _('make dot match newline (DOTALL)')),
    (int(re.U), 'assume unicode locale (UNICODE)'),
    (int(re.X), _('ignore whitespace and comments (VERBOSE)')),
)

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
