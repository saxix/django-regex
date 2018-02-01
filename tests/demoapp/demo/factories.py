# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from factory import DjangoModelFactory


class DemoModelFactory(DjangoModelFactory):
    class Meta:
        model = 'demo.DemoModel1'
        # django_get_or_create = ('id',)


class DemoModel2Factory(DjangoModelFactory):
    class Meta:
        model = 'demo.DemoModel2'
        # django_get_or_create = ('id',)
