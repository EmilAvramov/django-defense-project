from .models import UserModel, UserProfileModel
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.ModelForm):
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, max_length=64
    )

    class Meta:
        model = UserModel
        fields = ["email", "password"]


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, max_length=64
    )
    password2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput, max_length=64
    )

    class Meta:
        model = UserModel
        fields = ["email", "password", "first_name", "last_name"]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["email", "first_name", "last_name"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ["age", "gender", "image"]


class PasswordEditForm(forms.ModelForm):
    oldPassword = forms.CharField(
        label="Old Password", widget=forms.PasswordInput, max_length=64
    )
    newPassword = forms.CharField(
        label="New Password", widget=forms.PasswordInput, max_length=64
    )
    newPassword2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput, max_length=64
    )

    class Meta:
        model = UserModel
        fields = ["oldPassword", "newPassword", "newPassword2"]


class UserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ["email"]


class UserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ["email"]
