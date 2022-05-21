from email.policy import default
from random import choices
from .models import YEAR_CHOICES, Pet
from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput, NumberInput, DateInput, FileInput, Select
from .models import year_choices

YEAR_CHOICES = [(0,0)] + year_choices()
class PetCreateUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog name','type':"text"}))
    race = forms.CharField(max_length=30, required=False, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog race','type':"text"}))
    year_birth = forms.ChoiceField(choices = YEAR_CHOICES,  widget=Select(attrs={'class': 'g__form-input input','type':"number"}))
    avatar = forms.ImageField(required=False, widget=FileInput())#attrs={'class': "g__btn dog__btn-change-avatar"}))
    class Meta:
        model=Pet
        fields = ['name','race','year_birth','avatar']

# class PetCreateUpdateForm(forms.ModelForm):
#     name = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog name','type':"text"}))
#     race = forms.CharField(max_length=30, required=False, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog race','type':"text"}))
#     year_birth = forms.IntegerField(required=False, widget=NumberInput(attrs={'class': 'g__form-input input','placeholder': 'year of birth','type':"number"}))
#     class Meta:
#         model=Pet
#         fields = ['name','race','year_birth']
        
# class PetAvatarCreateUpdateForm(forms.ModelForm):
#     avatar = forms.ImageField(widget=FileInput())#attrs={'class': "g__btn dog__btn-change-avatar"}))
#     class Meta:
#         model=Pet
#         fields = ['avatar']

