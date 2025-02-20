from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'category', 'message']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
