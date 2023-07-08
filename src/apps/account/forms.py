from .models import User, UserProfile
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
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, max_length=64
    )
    password2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput, max_length=64
    )

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
