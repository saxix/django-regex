# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

import pytest

from demo.models import DemoModel2
from django_regex.fields import RegexField, RegexFlagsField
from django_regex.forms import RegexFlagsFormField
from django_regex.validators import flags_to_value, value_to_flags, compress

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("value", [(re.I, re.M, re.DOTALL, re.U, re.VERBOSE),
                                   [2, 8, 16, 32, 64],
                                   'imsuv'
                                   ]
                         )
def test_value_to_flags1(value):
    assert value_to_flags(value) == 122


@pytest.mark.parametrize("value", [None, '', 0, '0'])
def test_value_to_flags2(value):
    assert value_to_flags(value) == 0


@pytest.mark.parametrize("value", [122, '122'])
def test_flags_to_value(value):
    assert flags_to_value(value) == [2, 8, 16, 32, 64]


def test_flags():
    f = RegexField(flags_separator='/')
    regex = f.clean('abc/2', None)
    assert regex.match('abc')
    assert regex.match('ABC')


def test_flags_humanized():
    f = RegexField(flags_separator='/')
    regex = f.clean('abc/i', None)
    assert regex.match('abc')
    assert regex.match('ABC')

    o = DemoModel2.objects.create(regex=compress(['aa', 2]))
    o.regex.match('AA')

    o = DemoModel2.objects.create(regex=compress(['aa', 'i']))
    o.regex.match('AA')


def test_flagsfield():
    f = RegexFlagsField()
    assert isinstance(f.formfield(), RegexFlagsFormField)
