from django.shortcuts import render
from . import forms
from django.views.generic.base import TemplateView
from django.http import HttpResponseForbidden
from .util import api


class ApiSearch(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.SearchForm()
        self.params = {"pageSize": 10}

    def get(self, request):
        query = request.GET.get("query", None)
        data_type = request.path.split("/")[2]
        print(data_type)

        response = api.call(data_type, self.params, query)
        data = response.get("data")
        error = response.get("error")

        if data:
            return render(
                request,
                "main/pages/search.html",
                {"data": data.json(), "form": self.form},
            )
        else:
            return render(request, "main/core/error.html", {"error": error})

    def post(self, request):
        return HttpResponseForbidden()

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()
