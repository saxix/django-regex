# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.admin import ModelAdmin, register

from .models import DemoModel1, DemoModel2


@register(DemoModel1)
class DemoAdmin1(ModelAdmin):
    list_display = ('name', 'regex')


@register(DemoModel2)
class DemoAdmin2(ModelAdmin):
    list_display = ('name', 'regex', 'pattern', 'flags')

    def pattern(self, obj):
        return obj.regex.pattern

    def flags(self, obj):
        return obj.regex.flags
