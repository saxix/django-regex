# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

import pytest

from django_regex import perl

PATTERNS = [('/.*/', re.compile('.*')),
            ('/.*/i', re.compile('.*', re.IGNORECASE)),
            ('/.*/m', re.compile('.*', re.MULTILINE)),
            ('/.*/im', re.compile('.*', re.IGNORECASE | re.MULTILINE)),
            ('/\//im', re.compile('/', re.IGNORECASE | re.MULTILINE)),
            ('|.*|i', re.compile('.*', re.IGNORECASE)),
            ('|path/to/file/|i', re.compile('path/to/file/', re.IGNORECASE)),
            ('|[ab]|i', re.compile('[ab]', re.IGNORECASE)),
            ('/(aa|bb)/i', re.compile('(aa|bb)', re.IGNORECASE)),
            ]


@pytest.mark.parametrize("pattern,expected", PATTERNS, ids=[i[0] for i in PATTERNS])
def test_parser(pattern, expected):
    assert perl.compile(pattern) == expected
