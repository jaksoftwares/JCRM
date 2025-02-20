from django import forms
from .models import PrayerRequest, PrayerResponse

class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'title', 'request', 'visibility']
        widgets = {
            'visibility': forms.Select(attrs={'class': 'form-control'}),
        }

class PrayerResponseForm(forms.ModelForm):
    class Meta:
        model = PrayerResponse
        fields = ['response']
