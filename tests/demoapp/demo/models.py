# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from django.db import models

from django_regex.fields import RegexField

logger = logging.getLogger(__name__)


class DemoModel1(models.Model):
    name = models.CharField(max_length=100)
    regex = RegexField()

    class Meta:
        ordering = ("id",)


class DemoModel2(models.Model):
    name = models.CharField(max_length=100)
    regex = RegexField(null=True, blank=True)

    class Meta:
        ordering = ("id",)
