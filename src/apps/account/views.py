from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from . import forms
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages


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
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("search/digimon")
        else:
            error = "Wrong credentials."
            return render(
                request, self.template, {"form": self.form, "error": error}
            )


class Register(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.RegisterForm()
        self.template = "pages/register.html"

    def get(self, request):
        return render(request, self.template, {"form": self.form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            password_1 = form.cleaned_data["password"]
            password_2 = form.cleaned_data["password2"]
            if password_1 == password_2:
                user = form.save()
                messages.success(request, 'Successfully registered!')
                login(request, user)
                return redirect("search/digimon")
            else:
                error = "Password do not match."
                return render(request, self.template, {"form": self.form, "error": error})
        else:
            error = "Something went wrong. Please try again."
            return render(request, self.template, {"form": self.form, "error": error})


def profile(request):
    return render(request, "pages/profile.html", {})
