from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView
from django.shortcuts import redirect
from .forms import (
    LoginForm,
    RegisterForm,
    ProfileEditForm,
    UserEditForm,
    PasswordEditForm,
    ProfileDeleteForm,
)
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import UserModel, UserProfileModel
from django.http import HttpResponseForbidden
from django.db import transaction
from django.contrib.auth.decorators import login_required


class Login(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = LoginForm()
        self.template = "pages/login.html"

    def get(self, request):
        context = {"form": self.form}
        return render(request, self.template, context)

    @method_decorator(csrf_protect)
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            next = request.POST.get("next", None)
            if next:
                return redirect(next)
            return redirect("main_app:search")
        else:
            context = {"form": self.form, "error": "Wrong credentials."}
            return render(request, self.template, context)

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
        self.form = RegisterForm()
        self.template = "pages/register.html"

    def get(self, request):
        return render(request, self.template, {"form": self.form})

    @method_decorator(csrf_protect)
    def post(self, request):
        form = RegisterForm(request.POST)
        result = self.createUser(form)
        if result[0] == "Success":
            messages.success(request, "Successfully registered!")
            login(request, result[1])
            return redirect("main_app:search")
        else:
            errors = form.errors.as_data()
            error_messages = {}

            for field, error_list in errors.items():
                error_messages[self.get_verbose_name(field)] = []
                for error in error_list:
                    error_messages[self.get_verbose_name(field)].append(
                        error.message
                    )

            error_messages["Passwords"] = ["Do not match!"]

            context = {"form": self.form, "error": error_messages}
            return render(request, self.template, context)

    def get_verbose_name(self, field_name):
        return UserModel._meta.get_field(field_name).verbose_name

    @transaction.atomic
    def createUser(self, form):
        if form.is_valid():
            email = form.cleaned_data["email"]
            password_1 = form.cleaned_data["password"]
            password_2 = form.cleaned_data["password2"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            if password_1 == password_2:
                user = UserModel.objects.create_user(
                    email=email,
                    password=password_1,
                    first_name=first_name,
                    last_name=last_name,
                )
                UserProfileModel.objects.create(user=user)
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


@login_required()
def profile_details(request):
    profile = UserProfileModel.objects.get(user=request.user.id)
    return render(
        request, "components/profile_details.html", {"profile": profile},
    )


class ProfileEdit(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template = "components/profile_edit.html"

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        profile = UserProfileModel.objects.get(user=user.id)
        userInitial = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        profileInitial = {
            "age": profile.age,
            "gender": profile.gender,
            "image": profile.image,
        }
        context = {
            "profile": profile,
            "userForm": UserEditForm(initial=userInitial),
            "profileForm": ProfileEditForm(initial=profileInitial),
        }
        return render(request, self.template, context)

    @method_decorator(csrf_protect, login_required)
    def post(self, request):
        user = request.user
        profile = UserProfileModel.objects.get(user=user.id)
        userForm = UserEditForm(request.POST, instance=user)
        profileForm = ProfileEditForm(request.POST, instance=profile)
        if self.updateData(user.id, userForm, profileForm):
            messages.success(request, "Successfully edited profile!")
            return redirect("acc_app:profile")
        else:
            context = {
                "profile": profile,
                "userForm": userForm,
                "profileForm": profileForm,
            }
            return render(request, self.template, context)

    def updateData(self, user_id, userForm, profileForm):
        if userForm.is_valid() and profileForm.is_valid():
            UserModel.objects.filter(id=user_id).update(
                email=userForm.cleaned_data["email"],
                first_name=userForm.cleaned_data["first_name"],
                last_name=userForm.cleaned_data["last_name"],
            )
            UserProfileModel.objects.filter(user=user_id).update(
                age=profileForm.cleaned_data["age"],
                gender=profileForm.cleaned_data["gender"],
                image=profileForm.cleaned_data["image"],
            )
            return True
        return False

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()


class ProfilePassword(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template = "components/profile_password.html"

    @method_decorator(login_required)
    def get(self, request):
        form = PasswordEditForm()
        profile = UserProfileModel.objects.get(user=request.user.id)
        context = {"profile": profile, "form": form}
        return render(request, self.template, context)

    @method_decorator(csrf_protect, login_required)
    def post(self, request):
        user = request.user
        profile = UserProfileModel.objects.get(user=user.id)
        form = PasswordEditForm(request.POST)
        if form.is_valid():
            oldPassword = form.cleaned_data["oldPassword"]
            newPassword = form.cleaned_data["newPassword"]
            newPassword2 = form.cleaned_data["newPassword2"]
            password_correct = authenticate(
                email=user.email, password=oldPassword
            )
            if password_correct is not None and newPassword == newPassword2:
                user.set_password(newPassword)
                user.save()
                return redirect("acc_app:profile")
            else:
                context = {"profile": profile, "form": form}
                return render(request, self.template, context)

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()


class ProfileDelete(DeleteView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template = "components/profile_delete.html"

    @method_decorator(login_required)
    def get(self, request):
        form = ProfileDeleteForm()
        profile = UserProfileModel.objects.get(user=request.user.id)
        context = {"profile": profile, "form": form}
        return render(request, self.template, context)

    @method_decorator(csrf_protect, login_required)
    def post(self, request):
        user = UserModel.objects.get(id=request.user.id)
        logout(request)
        user.delete()
        messages.success(request, "The user is deleted")
        return redirect("/")

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()
