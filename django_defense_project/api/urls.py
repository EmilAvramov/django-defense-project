from django.urls import path
from .views import ApiSearch

app_name = "api_app"

urlpatterns = [
    path("search/digimon", ApiSearch.as_view(), name="search/digimon"),
    path("search/attribute", ApiSearch.as_view(), name="search/attribute"),
    path("search/field", ApiSearch.as_view(), name="search/field"),
    path("search/level", ApiSearch.as_view(), name="search/level"),
    path("search/type", ApiSearch.as_view(), name="search/type"),
    path("search/skill", ApiSearch.as_view(), name="search/skill"),
]
