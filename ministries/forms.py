from django import forms
from .models import MinistryMembership

class MinistryMembershipForm(forms.ModelForm):
    class Meta:
        model = MinistryMembership
        fields = ['name', 'email', 'phone']
