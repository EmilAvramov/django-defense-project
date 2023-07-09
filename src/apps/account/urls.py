from . import views
from django.urls import path, include
from .views import (
    Login,
    Register,
    Logout,
    ProfileEdit,
    ProfilePassword,
    ProfileDelete,
)

app_name = "acc_app"

urlpatterns = [
    path("register", Register.as_view(), name="register"),
    path("login", Login.as_view(), name="login"),
    path(
        "profile/",
        include(
            [
                path("", views.profile_details, name="profile"),
                path(
                    "edit_profile", ProfileEdit.as_view(), name="edit_profile"
                ),
                path(
                    "change_password",
                    ProfilePassword.as_view(),
                    name="change_password",
                ),
                path(
                    "delete_profile",
                    ProfileDelete.as_view(),
                    name="delete_profile",
                ),
            ]
        ),
    ),
    path("logout", Logout.as_view(), name="logout"),
]
