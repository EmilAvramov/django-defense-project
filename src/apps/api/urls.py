from django.urls import path
from .views import ApiSearch

app_name = "api_app"

urlpatterns = [
    path("", ApiSearch.as_view(), name="search/digimon"),
    path("<int:id>", ApiSearch.as_view(), name="search/digimon_by_id"),
]
