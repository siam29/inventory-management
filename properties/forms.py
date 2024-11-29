from django import forms
from .models import LocalizeAccommodation
from django.core.exceptions import ValidationError


class LocalizeAccommodationForm(forms.ModelForm):
    class Meta:
        model = LocalizeAccommodation
        fields = ['accommodation', 'language', 'description', 'policy']

    def clean_policy(self):
        policy = self.cleaned_data.get('policy', {})
        if not isinstance(policy, dict):
            raise ValidationError("Policy must be a valid JSON dictionary.")
        return policy
