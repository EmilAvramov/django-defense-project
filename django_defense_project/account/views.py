from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from . import forms
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden


class Login(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.LoginForm()
        self.template = "account/public/login.html"

    def get(self, request):
        return render(request, self.template, {"form": self.form})

    @method_decorator(csrf_protect)
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("search/digimon")
        else:
            error = "not authenticated"
            return render(request, self.template, {"form": self.form, "error": error})


def register(request):
    return render(request, "account/public/register.html", {})


def profile(request):
    return render(request, "account/protected/profile.html", {})
