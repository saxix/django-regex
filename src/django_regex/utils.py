import logging
import re

from django_regex.exceptions import InvalidPattern

logger = logging.getLogger(__name__)

Regex = type(re.compile(''))


class RegexList(list):
    def __init__(self, seq=None):
        regexx = []
        if seq:
            for el in seq:
                regexx.append(self._compile(el))
        super(RegexList, self).__init__(regexx)

    def __repr__(self):
        return str([r.pattern for r in self])

    def _compile(self, pattern, index=None):
        try:
            if isinstance(pattern, Regex):
                return pattern
            return re.compile(pattern)
        except (TypeError, re.error):
            raise InvalidPattern(pattern)

    def __setitem__(self, i, pattern):
        rex = self._compile(pattern)
        super(RegexList, self).__setitem__(i, rex)

    def append(self, pattern):
        rex = self._compile(pattern)
        super(RegexList, self).append(rex)

    def __contains__(self, target):
        t = str(target)
        for rex in self:
            m = rex.match(t)
            if m and m.group():
                return True
        return False


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


FLAGS = {
    'I': re.IGNORECASE,
    'M': re.MULTILINE,
    'L': re.LOCALE,
    'S': re.DOTALL,
    'U': re.UNICODE,
    'V': re.VERBOSE,
}


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

    if isinstance(value, str):
        value = [FLAGS[x.upper()] for x in value if x.upper() in FLAGS]

    return sum(map(int, value))
