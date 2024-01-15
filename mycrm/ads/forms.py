from django import forms

from ads.models import Advertisement


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'
