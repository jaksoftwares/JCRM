from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["amount", "currency", "message"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter Amount"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "placeholder": "Optional Message", "rows": 3}),
        }
