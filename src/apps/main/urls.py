from django.urls import path, include
from .views import Library, Search, home, about, history

app_name = "main_app"

urlpatterns = [
    path("", home, name="home"),
    path("about", about, name="about"),
    path("history", history, name="history"),
    path(
        "search/",
        include(
            [
                path("", Search.as_view(), name="search"),
                path("<int:id>/", Search.as_view(), name="search",),
            ]
        ),
    ),
    path(
        "library/",
        include(
            [
                path("", Library.as_view(), name="library"),
                path("<int:id>/", Library.as_view(), name="library"),
            ]
        ),
    ),
]
