from .models import Pet
from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput

# class PetCreateUpdateForm(forms.ModelForm):
#     name = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog name','type':"text"}))
#     race = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog race','type':"text"}))
#     year_birth = 
#     avatar = 
#     class Meta:
#         model=Pet
#         fields = ['name','race','year_birth', 'avatar']
