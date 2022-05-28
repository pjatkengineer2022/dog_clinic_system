from dataclasses import fields
from django import forms
from django.forms.widgets import TextInput, Textarea
from .models import Diagnosis


class DiagnosisCreationForm(forms.ModelForm):
    description = forms.CharField(max_length=30, required=True, widget=Textarea(attrs={'class': 'textarea','placeholder': 'wpisz swoją diagnozę (w tym objawy choroby)','type':"text"}))
    class Meta:
        model=Diagnosis
        fields=['description']
