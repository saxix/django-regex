import re

from django import forms
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from django_regex.forms import RegexFormField

from .exceptions import InvalidPatternValidationError

rex = re.compile('')


# @deconstructible
# class RegexValidator(object):
#     message = _('Enter a valid regular expression pattern')
#     code = 'regex'
#
#     def __call__(self, value):
#         try:
#             re.compile(value)
#         except Exception:
#             raise InvalidPatternValidationError(self.message, code=self.code)
#

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
    widget = forms.Textarea

    # def __init__(self, *args, **kwargs):
    #     super(RegexField, self).__init__(*args, **kwargs)
    #     self.validators.append(RegexValidator)

    def contribute_to_class(self, cls, name, private_only=False, virtual_only=NOT_PROVIDED):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)
        setattr(cls, self.name, self.descriptor(self))

    def get_internal_type(self):
        return 'TextField'

    def deconstruct(self):
        name, path, args, kwargs = super(RegexField, self).deconstruct()
        return name, path, args, kwargs

    def to_python(self, value):
        if value is None:
            return None
        try:
            return re.compile(value)
        except Exception:
            raise InvalidPatternValidationError("%s is not a valid regular expression" % value)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value is None:
            return None
        # if isinstance(value, str):
        #     return value
        # else:
        return value.pattern

    def value_to_string(self, obj):
        """
        Return a string value of this field from the passed obj.
        This is used by the serialization framework.
        """
        return self.value_from_object(obj).pattern

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        kwargs['widget'] = self.widget
        return super(RegexField, self).formfield(RegexFormField, choices_form_class, **kwargs)
