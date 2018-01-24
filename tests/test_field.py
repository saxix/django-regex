# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest
from django.core.exceptions import ValidationError
from django.db import connection

from demo.models import DemoModel1, DemoModel2
from django_regex.fields import RegexField
from django_regex.forms import RegexFormField

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
