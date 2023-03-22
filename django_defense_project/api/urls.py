from django.urls import path
from . import views

urlpatterns = [
    path("digimon", views.get_digimon_list, name="digimon"),
]
