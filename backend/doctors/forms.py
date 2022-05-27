from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput, NumberInput, DateInput, FileInput, Select, Textarea
from pets.models import Medicine, Producer
from .models import DoctorShift, Shift


class MedicineCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=TextInput(attrs={'class': 'input','placeholder': 'type medicine name','type':"text"}))
    producer = forms.ModelChoiceField(queryset= Producer.objects.all(),  widget=Select(attrs={'class': 'g__form-input input','type':"text"}))
    description = forms.CharField(max_length=30, required=False, widget=Textarea(attrs={'class': 'textarea','placeholder': 'type medicine description','type':"text"}))
    class Meta:
        model=Medicine
        fields = ['name','producer','description']

class DoctorShiftCreationForm(forms.ModelForm):
    shift = forms.ModelChoiceField(queryset= Shift.objects.all(),  widget=Select(attrs={'class': 'g__form-input input','type':"text"}))#widget=forms.TimeInput(format='%H:%M')
    class Meta:
        model= DoctorShift
        fields = ['shift']
        