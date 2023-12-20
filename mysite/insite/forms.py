from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'mail', 'password1', 'password2', 'avatar']

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'avatar': 'Аватарка',
            'mail': 'Ваша почта'
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'mail', 'password', 'avatar']