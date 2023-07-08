from django.shortcuts import render
from . import forms
from django.views.generic.base import TemplateView
from apps.api.decorators.attachFieldLinks import attachFieldLinks
from apps.api.util import api


def home(request):
    return render(request, "pages/home.html", {})


class Search(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.SearchForm()
        self.params = {"pageSize": 10}

    def get(self, request, id=""):
        data_type = "digimon"
        if id:
            response = api.call(data_type, self.params, None, id)
            data = response.get("data")
            error = response.get("error")
            template = response.get("template")

            if data:
                data = attachFieldLinks(data)
                return render(
                    request, template, {"data": data, "form": self.form},
                )
            else:
                return render(
                    request, template, {"form": self.form, "error": error}
                )
        else:
            response = api.call(data_type, self.params, None, None)
            data = response.get("data")
            error = response.get("error")
            template = response.get("template")
            if data:
                return render(
                    request, template, {"data": data, "form": self.form},
                )
            else:
                return render(
                    request, template, {"form": self.form, "error": error}
                )


def about(request):
    return render(request, "pages/about.html", {})
