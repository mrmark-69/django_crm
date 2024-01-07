from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.forms import ModelForm
from .models import Advertising, Service


class AdvertisingForm(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = '__all__'


class ConfirmForm(forms.Form):
    confirm_action = forms.BooleanField(required=False)

    def clean(self):
        if self.cleaned_data['confirm_action'] is False:
            raise ValidationError('You must confirm this form')
        return super(ConfirmForm, self).clean()


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", ]
