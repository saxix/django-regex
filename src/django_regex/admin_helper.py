import logging
import re

from admin_extra_urls.extras import ExtraUrlMixin, action
from django import forms
from django.contrib import messages
from django.template.response import TemplateResponse

from django_regex.forms import RegexFlagsFormField
from django_regex.validators import decompress

logger = logging.getLogger(__name__)


class TestRegexForm(forms.Form):
    regex = RegexFlagsFormField(
        # widget=forms.TextInput,
        required=False)
    text = forms.CharField(widget=forms.Textarea,
                           required=False)


class AdminRegexHelperMixin(ExtraUrlMixin):

    @action(label='Test Regex')
    def test_regex(self, request, id):
        target = self.get_object(request, id)
        text = request.GET.get('text', '')
        context = {'target': target,
                   'opts': self.model._meta,
                   'object': target,
                   }
        if request.method == 'POST':
            form = TestRegexForm(request.POST)
            if form.is_valid():
                value = form.cleaned_data['regex']
                pattern, options = decompress(value)
                try:
                    regex = re.compile(pattern, options)
                    m = regex.match(form.cleaned_data['text'])
                    if m:
                        context['match'] = m
                        context['groups'] = m.groups()
                        context['span'] = m.span()
                        context['groupdict'] = m.groupdict()
                    else:
                        self.message_user(request, "Does not match", messages.WARNING)

                    if 'save' in request.POST:
                        target.regex = regex
                        target.save()
                        self.message_user(request, "Regex updated")
                        return None

                except Exception as e:  # pragma: no cover
                    self.message_user(request, str(e), messages.ERROR)
        else:
            form = TestRegexForm(initial={'regex': target.regex.pattern,
                                          'text': text})
        context['form'] = form
        return TemplateResponse(request, 'admin/django_regex/regex.html', context)
