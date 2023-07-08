from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import User, UserProfile
from django.http import HttpResponseForbidden
from django.db import transaction


class Login(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.LoginForm()
        self.template = "pages/login.html"

    def get(self, request):
        return render(request, self.template, {"form": self.form})

    @method_decorator(csrf_protect)
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("main_app:search")
        else:
            error = "Wrong credentials."
            return render(
                request, self.template, {"form": self.form, "error": error}
            )

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()


class Logout(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get(self, request):
        logout(request)
        return redirect("/")

    def post(self, request):
        return HttpResponseForbidden()

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()


class Register(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.RegisterForm()
        self.template = "pages/register.html"

    def get(self, request):
        return render(request, self.template, {"form": self.form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        result = self.createUser(form)
        if result[0] == "Success":
            messages.success(request, "Successfully registered!")
            login(request, result[1])
            return redirect("main_app:search")
        else:
            return render(
                request, self.template, {"form": self.form, "error": result[1]}
            )

    @transaction.atomic
    def createUser(self, form):
        if form.is_valid():
            email = form.cleaned_data["email"]
            password_1 = form.cleaned_data["password"]
            password_2 = form.cleaned_data["password2"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            if password_1 == password_2:
                user = User.objects.create_user(
                    email=email,
                    password=password_1,
                    first_name=first_name,
                    last_name=last_name,
                )
                UserProfile.objects.create(user=user)
                return ["Success", user]
            else:
                return ["Error", "Password do not match."]
        return ["Error", "Something went wrong. Please try again."]

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()


def profile_details(request):
    user = request.user
    if user:
        profile = UserProfile.objects.get(user=user.id)
        return render(
            request,
            "components/profile_details.html",
            {"user": user, "profile": profile},
        )
    else:
        return redirect("account:login")


def profile_edit(request):
    user = request.user
    if user:
        profile = UserProfile.objects.get(user=user.id)
        return render(
            request,
            "components/profile_edit.html",
            {"user": user, "profile": profile},
        )
    else:
        return redirect("account:login")


def profile_password(request):
    user = request.user
    if user:
        profile = UserProfile.objects.get(user=user.id)
        return render(
            request,
            "components/profile_password.html",
            {"user": user, "profile": profile},
        )
    else:
        return redirect("account:login")


def profile_delete(request):
    user = request.user
    if user:
        profile = UserProfile.objects.get(user=user.id)
        return render(
            request,
            "components/profile_delete.html",
            {"user": user, "profile": profile},
        )
    else:
        return redirect("account:login")


def library(request):
    if request.user:
        return render(request, "pages/library.html", {})
    else:
        return redirect("account:login")
