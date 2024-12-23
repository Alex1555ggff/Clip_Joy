from typing import Any
from django import forms 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='',
            widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    
    password = forms.CharField(label='', 
            widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Логин (используется при авторизации)'}))
    
    password = forms.CharField(label='Пароль', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    password2 = forms.CharField(label='', 
        widget=forms.PasswordInput(attrs={'placeholder': "Повтор пароля"}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', "email", "password", "password2"]
        labels = {
            'email': 'Ваша почта',
        }
        widgets = {
            "email": forms.TextInput(attrs={'placeholder': 'clipjoy@gmail.com'}),
        }
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd['password']
    
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Данный E-mail уже используется")
        return email
    