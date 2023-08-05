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
from json import loads
from django.http import JsonResponse


messages = {
    "not_found": "Digimon not found in collection.",
    "not_added": "Was unable to add the digimon to your collection.",
    "updated": "Successfully updated digimon.",
    "deleted": "Successfully deleted.",
    "server_error": "An error occurred. Please try again.",
    "no_data": "Nothing found for your search query.",
}


def home(request):
    return render(request, "pages/home.html", {})


def about(request):
    return render(request, "pages/about.html", {})


def history(request):
    return render(request, "pages/history.html", {})


class Search(TemplateView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.form = forms.SearchForm()
        self.params = {"pageSize": 20}

    def get(self, request, id=""):
        data_type = "digimon"
        query = request.GET.get("query", None)
        nextPage = request.GET.get("nextPage", None)

        if id or query:
            response = api.call(data_type, self.params, query, id, None)
            data = response.get("data")
            error = response.get("error")
            template = response.get("template")

            if data and error is False:
                data = attachFieldLinks(data)
                request.session["digimon"] = data
                return render(
                    request, template, {"data": data, "form": self.form},
                )
            else:
                return render(
                    request, template, {"error_message": messages["no_data"]},
                )
        else:
            if nextPage:
                response = api.call(data_type, None, None, None, nextPage)
            else:
                response = api.call(data_type, self.params, None, None, None)
            data = response.get("data")
            error = response.get("error")
            template = response.get("template")
            print(data)
            if data and error is False:
                if nextPage:
                    request.session["digimons"] += data["content"]
                    data["content"] = request.session["digimons"]
                else:
                    request.session["digimons"] = data["content"]

                print(data["pageable"]["nextPage"])

                if nextPage:
                    return JsonResponse(data)

                return render(
                    request,
                    template,
                    {
                        "data": data,
                        "nextPage": data["pageable"]["nextPage"],
                        "form": self.form,
                    },
                )
            else:
                return render(
                    request, template, {"error_message": messages["no_data"]},
                )

    def post(self, request):
        return HttpResponseForbidden()

    def patch(self, request):
        return HttpResponseForbidden()

    def put(self, request):
        return HttpResponseForbidden()

    def delete(self, request):
        return HttpResponseForbidden()


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
                    {"error_message": messages["not_found"]},
                )

            context = {
                "profile": profile,
                "digimon": digimon,
                "details_view": True,
            }
        else:
            digimons = profile.digimons.prefetch_related("images").order_by(
                "name"
            )
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
        return render(
            request,
            "core/error.html",
            {"error_message": messages["not_added"]},
        )

    @method_decorator(csrf_protect, login_required)
    def patch(self, request, id=""):
        try:
            digimon = Digimon.objects.get(id=id)
        except Digimon.DoesNotExist:
            return render(
                request,
                "core/error.html",
                {"error_message": messages["not_found"]},
            )

        comments = loads(request.body).get("description", None)
        digimon.comments = comments
        digimon.save()
        return JsonResponse({"message": messages["updated"]}, status=200)

    def put(self, request):
        return HttpResponseForbidden()

    @method_decorator(csrf_protect, login_required)
    def delete(self, request, id=""):
        try:
            digimon = Digimon.objects.get(id=id)

            if self.delete_from_DB(digimon):
                return JsonResponse(
                    {"message": messages["deleted"]}, status=204
                )
            return JsonResponse(
                {"message": messages["server_error"]}, status=500
            )

        except Digimon.DoesNotExist:
            return render(
                request,
                "core/error.html",
                {"error_message": messages["not_found"]},
            )

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

    @transaction.atomic
    def delete_from_DB(self, digimon):
        try:
            digimon.images.clear()
            digimon.levels.clear()
            digimon.attributes.clear()
            digimon.fields.clear()
            digimon.descriptions.clear()
            digimon.skills.clear()
            digimon.prior_evos.clear()
            digimon.next_evos.clear()

            digimon.delete()
            return True
        except Exception:
            return False
