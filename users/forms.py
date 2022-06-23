from .models import Profile
from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm #, PasswordChangeForm
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import CaptchaField

#REGISTER USER (creating profile)
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'wpisz swój username','type':"text"}))
    password1 = forms.CharField(max_length=30, widget=PasswordInput(attrs={'class': 'g__form-input input','placeholder':'wpisz hasło','type':"password"}))
    password2 = forms.CharField(max_length=30,widget=PasswordInput(attrs={'class': 'g__form-input input','placeholder':'potwierdź hasło','type':"password"}))
    captcha = CaptchaField()
    error_messages = {
        'unique_username': 'login już istnieje',
        'duplicate_username': 'login już istnieje',
        'password_mismatch': "hasła muszą być takie same",
    }
    class Meta:
        model=User
        fields = ['username','password1','password2']
    # def __init__(self, *args, **kwargs):
    #     super(UserRegisterForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'class': 'g__form-input input', 'type':"text"})
    #     self.fields['password1'].widget.attrs.update({'class': 'g__form-input input', 'type':"password"})
    #     self.fields['password2'].widget.attrs.update({'class': 'g__form-input input', 'type':"password"})
class ProfileRegisterForm(forms.ModelForm):
    mobileNumber = PhoneNumberField(widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'wpisz swój numer telefonu','type':"text"}))#(max_length=15, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'username','type':"text"}))
    class Meta:
        model = Profile
        fields = ['mobileNumber']

#LOGIN USER
class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'wpisz swój username','type':"text"}))
    password = forms.CharField(max_length=30, widget=PasswordInput(attrs={'class': 'g__form-input input','placeholder':'wpisz swoje hasło','type':"password"}))
    class Meta:
        model = User
        fields = ['username','password']

# UPDATE PROFILE (&user)
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'wpisz swój username','type':"text"}))
    email = forms.EmailField(max_length=60, required=False, widget=EmailInput(attrs={'class': 'g__form-input input','placeholder': 'wpisz swój email','type':"email"}))
    class Meta:
        model=User
        fields = ['username', 'email']
class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=60,required=False, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'wpisz swoje imię i nazwisko','type':"text"}))
    mobileNumber = PhoneNumberField(widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'wpisz swój numer telefonu','type':"text"}))#(max_length=15, widget=TextInput(attrs={'class': 'g__form-input input','placeholder': 'username','type':"text"}))
    class Meta:
        model = Profile
        fields = ['name','mobileNumber']

#CHANGE PASSWORD
class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=EmailInput(attrs={
        'class': "g__form-input input",
        'placeholder': 'wpisz swój email',
        'type': 'email',
        'name': 'email'
        }))
    class Meta:
        model=User
        fields = ["email"]

# class UserPasswordChangeForm(PasswordChangeForm):
#     old_password = forms.CharField(max_length=30, label='Stare hasło', widget=PasswordInput(attrs={'class': 'g__form-input input','placeholder':'type old password','type':"password"}))
#     password1 = forms.CharField(max_length=30, label='Wprowadź nowe hasło', widget=PasswordInput(attrs={'class': 'g__form-input input','placeholder':'type new password','type':"password"}))
#     password2 = forms.CharField(max_length=30, label='Potwierdź nowe hasło', widget=PasswordInput(attrs={'class': 'g__form-input input','placeholder':'confirm new password','type':"password"}))
#     class Meta:
#         model=User
#         fields = ["password1","password2"]