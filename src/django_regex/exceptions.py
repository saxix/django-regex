# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ValidationError


class InvalidPattern(Exception):
    pass


class InvalidPatternValidationError(ValidationError):
    pass
