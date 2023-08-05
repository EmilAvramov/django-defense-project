from .models import UserModel, UserProfileModel
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_attributes()

    password = forms.CharField(widget=forms.PasswordInput, max_length=64)

    def __set_attributes(self):
        for field in self.fields.values():
            field.label = False

        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["password"].widget.attrs["placeholder"] = "Password"

    class Meta:
        model = UserModel
        fields = ["email", "password"]


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_attributes()

    def __set_attributes(self):
        for field in self.fields.values():
            field.label = False

        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs[
            "placeholder"
        ] = "Repeat Password"

    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=64)

    class Meta:
        model = UserModel
        fields = ["email", "password", "password2", "first_name", "last_name"]


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


class ProfileDeleteForm(forms.Form):
    pass


class UserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ["email"]


class UserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = ["email"]
