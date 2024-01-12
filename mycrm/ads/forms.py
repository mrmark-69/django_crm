from django import forms
from django.core.exceptions import ValidationError

from ads.models import Advertisement


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'
