from . import views
from django.urls import path
from .views import Login, Register, Logout

app_name = "acc_app"

urlpatterns = [
    path("register", Register.as_view(), name="register"),
    path("login", Login.as_view(), name="login"),
    path("profile", views.profile, name="profile"),
    path("library", views.library, name="library"),
    path("logout", Logout.as_view(), name="logout")
]
