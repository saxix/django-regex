import re

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.utils.translation import ugettext_lazy as _

from .forms import RegexFlagsFormField, RegexFormField
from .validators import Regex, RegexValidator, compress, decompress

rex = re.compile('')


class RegexFieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return None
        return obj.__dict__.get(self.field.name)

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class RegexField(models.Field):
    descriptor = RegexFieldDescriptor
    form_class = RegexFormField
    widget = forms.TextInput

    def __init__(self, *args, **kwargs):
        self.flags_separator = kwargs.pop('flags_separator', None)
        self.flags = kwargs.pop('flags', 0)
        super(RegexField, self).__init__(*args, **kwargs)
        self.validators.append(RegexValidator)

    def contribute_to_class(self, cls, name, private_only=False, virtual_only=NOT_PROVIDED):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)
        setattr(cls, self.name, self.descriptor(self))

    def get_internal_type(self):
        return 'TextField'

    def to_python(self, value):
        if not value:
            return None
        pattern, flags = value, self.flags
        if isinstance(value, Regex):
            return value
        try:
            pattern, flags = decompress(value, self.flags_separator)
            flags = flags or self.flags
        except ValueError:
            pass
        if not pattern:
            return None
        try:
            return re.compile(pattern, flags)
        except Exception:
            raise ValidationError(_("`%(pattern)s` is not a valid regular expression"),
                                  params={'pattern': pattern})

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:  # pragma: no cover
            return None
        return value.pattern

    def value_to_string(self, obj):
        """
        Return a string value of this field from the passed obj.
        This is used by the serialization framework.
        """
        return self.value_from_object(obj).pattern

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        kwargs['widget'] = self.widget
        return super(RegexField, self).formfield(self.form_class,
                                                 choices_form_class, **kwargs)


class RegexFlagsField(RegexField):
    form_class = RegexFlagsFormField

    def to_python(self, value):
        if not value:
            return None
        pattern, flags = value, self.flags
        if isinstance(value, Regex):
            return value
        try:
            pattern, flags = decompress(value, self.flags_separator)
        except ValueError:
            pass
        if not pattern:
            return None
        try:
            return re.compile(pattern, flags)
        except Exception:
            raise ValidationError(_("`%(pattern)s` is not a valid regular expression"),
                                  params={'pattern': pattern})

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            return None
        return compress([value.pattern, value.flags])
