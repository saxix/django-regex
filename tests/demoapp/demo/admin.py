# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.admin import ModelAdmin, register

from .models import DemoModel1


@register(DemoModel1)
class DemoAdmin(ModelAdmin):
    pass
