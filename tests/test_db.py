# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest

from demo.models import DemoModel1, DemoModel2

pytestmark = pytest.mark.django_db


def test_save():
    m = DemoModel1()
    m.regex = '^aaa$'
    m.save()
    assert m.pk
    assert m.regex.match('aaa')


def test_none():
    assert DemoModel2.regex is None


def test_save_none():
    m = DemoModel2()
    m.save()
    assert m.pk
    with pytest.raises(AttributeError):
        assert m.regex.match('aaa')


def test_lookup_equal():
    m = DemoModel1()
    m.regex = '^aaa$'
    m.save()
    assert DemoModel1.objects.filter(regex='^aaa$').exists()


def test_lookup_startswith():
    m = DemoModel1()
    m.regex = '^aaa$'
    m.save()
    assert DemoModel1.objects.filter(regex__startswith='^').exists()


def test_lookup_endswith():
    m = DemoModel1()
    m.regex = '^aaa$'
    m.save()
    assert DemoModel1.objects.filter(regex__endswith='$').exists()


def test_lookup_contains():
    m = DemoModel1()
    m.regex = '^aaa$'
    m.save()
    assert DemoModel1.objects.filter(regex__contains='aaa').exists()
