from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.ModelForm):
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, max_length=64
    )

    class Meta:
        model = User
        fields = ["email", "password"]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, max_length=64
    )
    password2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput, max_length=64
    )

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email"]


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email"]
