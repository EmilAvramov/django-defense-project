from django.shortcuts import render
from . import forms
from django.views.generic.base import TemplateView
from apps.api.decorators.attachFieldLinks import attachFieldLinks
from apps.api.util import api
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def home(request):
    return render(request, "pages/home.html", {})


class Search(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.SearchForm()
        self.params = {"pageSize": 20}

    def get(self, request, id=""):
        data_type = "digimon"
        query = request.GET.get("query", None)
        if id or query:
            response = api.call(data_type, self.params, query, id)
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

    def post(self, request):
        return HttpResponseForbidden()

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()


def about(request):
    return render(request, "pages/about.html", {})



class Library(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @login_required
    def get(self, request):
        return render(request, "pages/library.html", {})

    @login_required
    def post(self, request):
        return HttpResponseForbidden()

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()





@login_required()
def library(request):
    if request.user:
        return render(request, "pages/library.html", {})
    else:
        return redirect("account:login")
