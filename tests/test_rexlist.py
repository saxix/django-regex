# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys

import pytest

from django_regex.exceptions import InvalidPattern
from django_regex.utils import RegexList

pytestmark = pytest.mark.django_db


def test_init():
    rules = RegexList(['^abc$'])
    assert 'abc' in rules
    assert 'a' not in rules


def test_number():
    rules = RegexList()
    rules.append('\d*')
    assert 1 in rules
    assert 'a' not in rules


def test_append():
    rules = RegexList()
    rules.append('^abc$')
    assert 'abc' in rules
    assert 'a' not in rules


def test_setitem():
    rules = RegexList([''])
    rules[0] = '^abc$'
    assert 'abc' in rules
    assert 'a' not in rules


def test_error():
    with pytest.raises(InvalidPattern):
        RegexList(['*'])

    with pytest.raises(InvalidPattern):
        rules = RegexList()
        rules.append('**')


def test_repr():
    rules = RegexList(['.*', '[0-9]*'])
    if sys.version_info[0] < 3:
        assert str(rules) == "[u'.*', u'[0-9]*']"
    elif sys.version_info[0] == 3:
        assert str(rules) == "['.*', '[0-9]*']"
