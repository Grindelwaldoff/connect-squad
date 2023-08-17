from django import forms
from django.conf import settings


class CountryChoice(forms.Form):
    date_range = forms.MultipleChoiceField(choices=settings.COUNTRY_CHOICES)
