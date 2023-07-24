from django.shortcuts import render
from . import forms
from django.views.generic.base import TemplateView
from apps.api.decorators.attachFieldLinks import attachFieldLinks
from apps.api.util import api
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from apps.account.models import UserProfileModel
from .models import (
    DigimonImage,
    DigimonAtribute,
    DigimonDescription,
    DigimonEvolution,
    DigimonField,
    DigimonLevel,
    DigimonSkill,
    Digimon,
)
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.db.models import Prefetch


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
                request.session["digimon"] = data
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

    @method_decorator(login_required)
    def get(self, request, id=""):
        profile = UserProfileModel.objects.select_related("user").get(
            user=request.user
        )
        if id:
            try:
                digimon = profile.digimons.prefetch_related(
                    "images",
                    "levels",
                    "attributes",
                    "fields",
                    "descriptions",
                    "skills",
                    "prior_evos",
                    "next_evos",
                ).get(id=id)
            except Digimon.DoesNotExist:
                return render(
                    request,
                    "core/error.html",
                    {
                        "error_message": f"No digimon with ID {id} in your collection."
                    },
                )

            context = {
                "profile": profile,
                "digimon": digimon,
                "details_view": True,
            }
        else:
            digimons = profile.digimons.prefetch_related("images")
            context = {
                "profile": profile,
                "digimons": digimons,
                "details_view": False,
            }
        return render(request, "pages/library.html", context)

    @method_decorator(csrf_protect, login_required)
    def post(self, request, id=""):
        data = request.session["digimon"]
        if data["id"] == id and data["id"]:
            profile = UserProfileModel.objects.get(user=request.user.id)
            if self.add_to_DB(data, profile):
                return redirect("main_app:library")
        return render(request, "core/error.html")

    @transaction.atomic
    def add_to_DB(self, data, profile):
        digimon_data = {
            "name": data["name"],
            "antibody": data["xAntibody"],
            "release_date": data["releaseDate"],
            "comments": "",
        }
        images = [
            DigimonImage.objects.create(**value) for value in data["images"]
        ]
        fields = [
            DigimonField.objects.create(
                field_id=value["id"],
                field_name=value["field"],
                image=value["image"],
            )
            for value in data["fields"]
        ]
        attributes = [
            DigimonAtribute.objects.create(
                attr_id=value["id"], attr_name=value["attribute"]
            )
            for value in data["attributes"]
        ]
        descriptions = [
            DigimonDescription.objects.create(**value)
            for value in data["descriptions"]
            if value["language"] == "en_us"
        ]

        levels = [
            DigimonLevel.objects.create(
                level_id=value["id"], level_name=value["level"]
            )
            for value in data["levels"]
        ]

        skills = [
            DigimonSkill.objects.create(
                skill_id=value["id"],
                skill_name=value["skill"],
                translation=value["translation"],
                description=value["description"],
            )
            for value in data["skills"]
        ]

        prior_evos = [
            DigimonEvolution.objects.create(
                evo_id=value["id"],
                evo_name=value["digimon"],
                evo_condition=value["condition"],
                evo_image=value["image"],
                evo_link=value["url"],
            )
            for value in data["priorEvolutions"]
            if value["id"]
        ]

        next_evos = [
            DigimonEvolution.objects.create(
                evo_id=value["id"],
                evo_name=value["digimon"],
                evo_condition=value["condition"],
                evo_image=value["image"],
                evo_link=value["url"],
            )
            for value in data["nextEvolutions"]
            if value["id"]
        ]

        digimon = Digimon.objects.create(**digimon_data)
        digimon.images.add(*images)
        digimon.descriptions.add(*descriptions)
        digimon.skills.add(*skills)
        digimon.fields.add(*fields)
        digimon.attributes.add(*attributes)
        digimon.levels.add(*levels)
        digimon.prior_evos.add(*prior_evos)
        digimon.next_evos.add(*next_evos)
        digimon.save()
        profile.digimons.add(digimon)
        profile.save()
        return True

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    @method_decorator(csrf_protect, login_required)
    def delete(self, request, id=""):
        try:
            digimon = Digimon.objects.get(id=id)

            digimon.images.clear()
            digimon.levels.clear()
            digimon.attributes.clear()
            digimon.fields.clear()
            digimon.descriptions.clear()
            digimon.skills.clear()
            digimon.prior_evos.clear()
            digimon.next_evos.clear()

            digimon.delete()
        except Digimon.DoesNotExist:
            return JsonResponse({"error": "Digimon not found"}, status=404)

        return JsonResponse({"message": "Successfully deleted"}, status=204)
