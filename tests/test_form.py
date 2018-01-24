# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

from django.forms import modelform_factory

from demo.models import DemoModel1, DemoModel2
from django_regex.forms import RegexFormField


def test_validate_fail():
    Form = modelform_factory(DemoModel1, exclude=())
    data = {'name': 'name', 'regex': '*'}
    form = Form(data=data)
    assert not form.is_valid()


def test_valid():
    Form = modelform_factory(DemoModel1, exclude=())
    data = {'name': 'name', 'regex': '.*'}
    form = Form(data=data)
    assert form.is_valid()


def test_required():
    Form = modelform_factory(DemoModel1, exclude=())
    data = {'name': 'name', 'regex': ''}
    form = Form(data=data)
    assert not form.is_valid()


def test_none():
    Form = modelform_factory(DemoModel2, exclude=())
    data = {'name': 'name'}
    form = Form(data=data)
    assert form.is_valid()


def test_save(db):
    Form = modelform_factory(DemoModel1, exclude=())
    data = {'name': 'name', 'regex': 'aaa'}
    form = Form(data=data)
    form.is_valid()
    obj = form.save()
    assert obj.regex.match('aaa')


def test_render(db, demomodel):
    Form = modelform_factory(DemoModel1, exclude=())
    data = {'name': 'name', 'regex': 'aaa'}
    form = Form(data=data)
    assert form.as_p()

    form = Form(instance=demomodel)
    assert form.as_p()

    demomodel.regex = None
    form = Form(instance=demomodel)
    assert form.as_p()


def test_instance(db, demomodel):
    Form = modelform_factory(DemoModel1, exclude=())
    form = Form({'name': demomodel.name,
                 'regex': demomodel.regex.pattern}, instance=demomodel)
    assert form.initial['regex'] == demomodel.regex
    assert isinstance(form.fields['regex'], RegexFormField)
    assert form.is_valid(), form.errors
    obj = form.save()
    assert obj.regex == demomodel.regex


def test_unexpected():
    # FIXME: Not sure why this should be tested

    Form = modelform_factory(DemoModel1, exclude=())
    data = {'name': 'name', 'regex': re.compile('.*')}
    form = Form(data=data)
    assert form.is_valid()
