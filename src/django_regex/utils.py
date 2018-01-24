# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import re

from django_regex.exceptions import InvalidPattern

logger = logging.getLogger(__name__)


class RegexList(list):
    """
        list class where each entry is a valid regular expression

    >>> r = RegexList(["a.*"])
    >>> r.append("[0-9]*")
    >>> "1" in r
    True

    >>> "cc" in r
    False

    >>> "abc" in r
    True

    >>> print(r)
    [u'a.*', u'[0-9]*']

    >>> r[0] = '.*'

    >>> r[0] = '[0-'
    Traceback (most recent call last):
        ...
    InvalidPattern: [0- is not a valid regular expression
    """

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
