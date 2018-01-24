import os
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
