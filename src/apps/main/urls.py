from django.urls import path
from . import views

app_name = "main_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("search", views.Search.as_view(), name="search"),
    path(
        "search/<int:id>", views.Search.as_view(), name="search/digimon_by_id"
    ),
    path("about", views.about, name="about"),
]
