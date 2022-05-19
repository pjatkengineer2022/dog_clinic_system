from .models import Pet
from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput, NumberInput, DateInput, FileInput

class PetCreateUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog name','type':"text"}))
    race = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'dog race','type':"text"}))
    year_birth = forms.IntegerField(widget=NumberInput(attrs={'class': 'g__form-input input','placeholder': 'year of birth','type':"number"}))
    class Meta:
        model=Pet
        fields = ['name','race','year_birth']
        
class PetAvatarCreateUpdateForm(forms.ModelForm):
    #avatar = forms.ImageField(widget=NumberInput(attrs={'class': 'g__form-input input','placeholder': 'dog race','type':"number"}))
    class Meta:
        model=Pet
        fields = ['avatar']