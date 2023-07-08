from . import views
from django.urls import path, include
from .views import Login, Register, Logout

app_name = "acc_app"

urlpatterns = [
    path("register", Register.as_view(), name="register"),
    path("login", Login.as_view(), name="login"),
    path("profile/", include([
        path("", views.profile_details, name="profile"),
        path("edit_profile", views.profile_edit, name="edit_profile"),
        path("change_password", views.profile_password, name="change_password"),
        path("delete_profile", views.profile_delete, name="delete_profile")
    ])),
    path("library", views.library, name="library"),
    path("logout", Logout.as_view(), name="logout")
]
