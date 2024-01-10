from django import forms
from django.core.exceptions import ValidationError
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


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", ]
        widgets = {
            'description': forms.Textarea(attrs={"cols": "40", "rows": "5"}),
        }
