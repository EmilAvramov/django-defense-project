from django.urls import path
from .views import DigimonSearch

app_name = "api_app"
urlpatterns = [
    path("search/digimon", DigimonSearch.as_view(), name="search/digimon"),
]
