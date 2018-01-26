import os
import re
import sys

import pytest


def pytest_configure(config):
    here = os.path.dirname(__file__)
    sys.path.insert(0, here)


@pytest.fixture(scope='session')
def client(request):
    import django_webtest

    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    app = django_webtest.DjangoTestApp()
    return app


@pytest.fixture
def demomodel(db):
    from demo.factories import DemoModelFactory
    return DemoModelFactory(regex='.*', name='name')


@pytest.fixture
def demomodel2(db):
    from demo.factories import DemoModel2Factory
    return DemoModel2Factory(regex=re.compile('^$', re.I + re.M), name='name')
