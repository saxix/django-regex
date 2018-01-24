# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys

import pytest

from django_regex.exceptions import InvalidPattern
from django_regex.utils import RegexList

pytestmark = pytest.mark.django_db


def test_init():
    l = RegexList(['^abc$'])
    assert 'abc' in l
    assert 'a' not in l


def test_number():
    l = RegexList()
    l.append('\d*')
    assert 1 in l
    assert 'a' not in l


def test_append():
    l = RegexList()
    l.append('^abc$')
    assert 'abc' in l
    assert 'a' not in l


def test_setitem():
    l = RegexList([''])
    l[0] = '^abc$'
    assert 'abc' in l
    assert 'a' not in l


def test_error():
    with pytest.raises(InvalidPattern):
        l = RegexList(['*'])

    with pytest.raises(InvalidPattern):
        l = RegexList()
        l.append('**')


def test_repr():
    l = RegexList(['.*', '[0-9]*'])
    if sys.version_info[0] < 3:
        assert str(l) == "[u'.*', u'[0-9]*']"
    elif sys.version_info[0] == 3:
        assert str(l) == "['.*', '[0-9]*']"
