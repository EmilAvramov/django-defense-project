from django.shortcuts import render
from . import forms
from django.views.generic.base import TemplateView
from .util import api


class DigimonSearch(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template_name = "main/pages/home.html"
        self.form = forms.SearchForm()
        self.data = []
        self.params = {"pageSize": 10}

    def get(self, request):
        query = request.GET.get("query", None)
        self.data = api.call("digimon", self.params, query).json()
        print(self.data)

        return render(
            request, self.template_name, {"data": self.data, "form": self.form}
        )
