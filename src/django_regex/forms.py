import logging

from django import forms
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from django_regex.utils import flags_to_value

from .validators import OPTIONS, Regex, RegexValidator, compress, decompress

logger = logging.getLogger(__name__)


class RegexFormField(forms.CharField):
    # widget = forms.Textarea

    def __init__(self, *args, **kwargs):
        super(RegexFormField, self).__init__(*args, **kwargs)
        self.validators.append(RegexValidator())

    def prepare_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value

        return value.pattern

    def to_python(self, value):
        """Return a string."""
        return value


class RegexTextField(forms.Textarea):
    pass


class RegexFlagsWidget(forms.MultiWidget):
    template_name = 'django_regex/widgets/regex.html'
    widget = forms.Textarea

    def __init__(self, widgets, attrs=None):
        super(RegexFlagsWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        pattern, flags = decompress(value)
        return pattern, flags_to_value(flags)


class FlagsInput(CheckboxSelectMultiple):
    template_name = 'django_regex/widgets/flags.html'


class FlagsField(forms.MultipleChoiceField):
    pass


class RegexFlagsFormField(forms.MultiValueField):
    """
    Form field that validates credit card expiry dates.
    """
    default_error_messages = {
        'invalid': _('Enter a list of values.'),
        'incomplete': _('Enter a complete value.'),
        'invalid_regex': ''}

    def __init__(self, *args, **kwargs):
        error_messages = self.default_error_messages.copy()
        kwargs['require_all_fields'] = False
        self.flags_separator = kwargs.pop('flags_separator', None)
        # self.regex_widget = kwargs.pop('widget', forms.Textarea)
        # w = kwargs.get('widget', RegexFormField)
        if 'error_messages' in kwargs:  # pragma: no cover
            error_messages.update(kwargs['error_messages'])
        fields = (
            RegexFormField(widget=kwargs.get('widget', forms.Textarea),
                           error_messages={'invalid': error_messages['invalid_regex']}),
            FlagsField(required=False,
                       choices=OPTIONS,
                       widget=FlagsInput)
        )
        super(RegexFlagsFormField, self).__init__(fields, *args, **kwargs)
        self.widget = RegexFlagsWidget(widgets=[fields[0].widget,
                                                fields[1].widget,
                                                ])
        self.validators.append(RegexValidator())

    def compress(self, data_list):
        return compress(data_list, self.flags_separator)

    def prepare_value(self, value):
        out = value
        if isinstance(value, Regex):
            out = compress([value.pattern, value.flags], self.flags_separator)
        if isinstance(value, list):
            out = compress(value, self.flags_separator)
        return out
