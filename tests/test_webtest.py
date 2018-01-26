# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import re

import pytest
import six
from django.urls import reverse

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_admin_change(django_app, admin_user, demomodel):
    change_url = reverse('admin:demo_demomodel1_change', args=[demomodel.pk])
    res = django_app.get(change_url, user=admin_user)
    assert res.status_code == 200
    res.form['regex'] = 'xxx\d+'
    res = res.form.submit()
    assert res.status_code == 302
    demomodel.refresh_from_db()
    assert demomodel.regex.match('xxx22')


@pytest.mark.django_db
def test_admin_change_flags(django_app, admin_user, demomodel2):
    change_url = reverse('admin:demo_demomodel2_change', args=[demomodel2.pk])
    res = django_app.get(change_url, user=admin_user)
    res.form['regex_0'] = 'xxx[0-9]+'
    res.form['regex_1'] = [False, False, False, False, False]
    res = res.form.submit()
    assert res.status_code == 302
    demomodel2.refresh_from_db()
    assert demomodel2.regex.match('xxx22')
    assert not demomodel2.regex.match('xxx')
    if six.PY3:
        assert demomodel2.regex.flags == re.UNICODE
    else:
        assert demomodel2.regex.flags == 0


@pytest.mark.django_db
def test_admin_change_flags_none(django_app, admin_user, demomodel2):
    change_url = reverse('admin:demo_demomodel2_change', args=[demomodel2.pk])
    res = django_app.get(change_url, user=admin_user)
    res.form['regex_0'] = None
    res.form['regex_1'] = [True, True, True, True]
    res = res.form.submit()
    assert res.status_code == 302
    demomodel2.refresh_from_db()
    assert demomodel2.regex is None


@pytest.mark.django_db
def test_admin_change_flags_empty(django_app, admin_user, demomodel2):
    change_url = reverse('admin:demo_demomodel2_change', args=[demomodel2.pk])
    res = django_app.get(change_url, user=admin_user)
    res.form['regex_0'] = ''
    res.form['regex_1'] = [True, True, True, True]
    res = res.form.submit()
    assert res.status_code == 302
    demomodel2.refresh_from_db()
    assert demomodel2.regex is None
