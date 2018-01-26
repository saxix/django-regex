# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

import six
from django.forms import modelform_factory

from demo.models import DemoModel2
from django_regex.forms import RegexFlagsFormField


def test_validate_fail():
    Form = modelform_factory(DemoModel2, exclude=())
    data = {'name': 'name', 'regex_0': '*', 'regex_1': ''}
    form = Form(data=data)
    assert not form.is_valid(), form.errors


def test_valid():
    Form = modelform_factory(DemoModel2, exclude=())
    data = {'name': 'name', 'regex_0': '.*', 'regex_1': ''}
    form = Form(data=data)
    assert form.is_valid()


# def test_required():
#     Form = modelform_factory(DemoModel2, exclude=())
#     data = {'name': 'name', 'regex_0': '', 'regex_1': ''}
#     form = Form(data=data)
#     assert not form.is_valid()


def test_none():
    Form = modelform_factory(DemoModel2, exclude=())
    data = {'name': 'name'}
    form = Form(data=data)
    assert form.is_valid()


def test_save(db):
    Form = modelform_factory(DemoModel2, exclude=())
    data = {'name': 'name', 'regex_0': 'aaa', 'regex_1': [int(re.I)]}
    form = Form(data=data)
    form.is_valid()
    obj = form.save()
    assert obj.regex.match('AAA')


def test_render_field(db, demomodel2):
    Form = modelform_factory(DemoModel2, fields=['regex'])
    form = Form(instance=demomodel2)
    rendered = form.as_p()
    m = re.findall(' checked ', rendered)
    if six.PY3:
        assert len(m) == 4, rendered
    else:
        assert len(m) == 3, rendered
    assert 'name="regex_0" value="^$"' in rendered, rendered


def test_render(db, demomodel):
    Form = modelform_factory(DemoModel2, exclude=())
    data = {'name': 'name', 'regex_0': '', 'regex_1': ''}
    form = Form(data=data)
    assert form.as_p()

    form = Form(instance=demomodel)
    assert form.as_p()

    demomodel.regex = None
    form = Form(instance=demomodel)
    assert form.as_p()


def test_instance(db, demomodel):
    Form = modelform_factory(DemoModel2, exclude=())
    form = Form({'name': demomodel.name,
                 'regex_0': demomodel.regex.pattern,
                 'regex_1': [],
                 }, instance=demomodel)
    assert form.initial['regex'] == demomodel.regex
    assert isinstance(form.fields['regex'], RegexFlagsFormField)

    assert form.is_valid(), form.errors

    obj = form.save()
    assert obj.regex == demomodel.regex
