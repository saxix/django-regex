import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_checker_success(django_app, admin_user, demomodel2):
    change_url = reverse('admin:demo_demomodel2_test_regex', args=[demomodel2.pk])
    res = django_app.get(change_url, user=admin_user)
    res.form['regex_0'] = '[0-9]*'
    res.form['regex_1'] = [False, ]
    res.form['text'] = '123'
    res = res.form.submit()
    assert res.status_code == 200
    assert "SRE_Match" in str(res.content)


@pytest.mark.django_db
def test_checker_error(django_app, admin_user, demomodel2):
    change_url = reverse('admin:demo_demomodel2_test_regex', args=[demomodel2.pk])
    res = django_app.get(change_url, user=admin_user)
    res.form['regex_0'] = '*'
    res.form['regex_1'] = [False, ]
    res.form['text'] = '123'
    res = res.form.submit()
    assert res.status_code == 200
    assert not "SRE_Match" in str(res.content)


@pytest.mark.django_db
def test_checker_fail(django_app, admin_user, demomodel2):
    change_url = reverse('admin:demo_demomodel2_test_regex', args=[demomodel2.pk])
    res = django_app.get(change_url, user=admin_user)
    res.form['regex_0'] = '[a-z]$'
    res.form['regex_1'] = [False, False, False, False, False, False, ]
    res.form['text'] = '1'
    res = res.form.submit()
    assert res.status_code == 200
    assert not "SRE_Match" in str(res.content)


@pytest.mark.django_db
def test_checker_save(django_app, admin_user, demomodel2):
    change_url = reverse('admin:demo_demomodel2_test_regex', args=[demomodel2.pk])
    res = django_app.get(change_url, user=admin_user)
    res.form['regex_0'] = '[a-z]*'
    res.form['regex_1'] = [False, ]
    res.form['text'] = '123'
    res = res.form.submit('save')
    assert res.status_code == 302
