# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

import pytest
from django.core.exceptions import ValidationError
from django.db import connection

from django_regex.fields import RegexField
from django_regex.forms import RegexFormField, compress

pytestmark = pytest.mark.django_db


def test_type():
    f = RegexField()
    assert f.db_parameters(connection)['type'] == 'text'


def test_formfield():
    f = RegexField()
    assert isinstance(f.formfield(), RegexFormField)


def test_validation():
    f = RegexField()
    with pytest.raises(ValidationError):
        f.clean(None, None)

    with pytest.raises(ValidationError):
        f.clean('*', None)
    assert f.clean('.*', None)


def test_flags():
    f = RegexField()
    regex = f.clean('abc', None)
    assert regex.match('abc')
    assert not regex.match('ABC')

    f = RegexField(flags=re.I)
    regex = f.clean('abc', None)
    assert regex.match('abc')
    assert regex.match('ABC')

    f = RegexField(flags=re.I)
    regex = f.clean(compress(['abc', '32']), None)
    assert regex.match('abc')
    assert not regex.match('ABC')

    f = RegexField()
    regex = f.clean(compress(['abc', '2']), None)
    assert regex.match('abc')
    assert regex.match('ABC')
