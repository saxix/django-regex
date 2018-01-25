# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

from django.core import serializers

from demo.models import DemoModel1

logger = logging.getLogger(__name__)


def test_serializer(demomodel):
    actual = serializers.serialize('json', DemoModel1.objects.all())
    data = json.loads(actual)
    assert data[0]["fields"]['regex'] == demomodel.regex.pattern
