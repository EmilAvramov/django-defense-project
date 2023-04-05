from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=64)
    password = forms.CharField(label="Password", max_length=64)
