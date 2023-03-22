from django.shortcuts import render
import requests

# API endpoints
API_DIGIMON_LIST = "https://digi-api.com/api/v1/digimon"
API_ATTRIBUTE_LIST = "https://digi-api.com/api/v1/attribute"
API_FIELD_LIST = "https://digi-api.com/api/v1/field"
API_LEVEL_LIST = "https://digi-api.com/api/v1/level"
API_TYPE_LIST = "https://digi-api.com/api/v1/type"
API_SKILL_LIST = "https://digi-api.com/api/v1/skill"


def get_digimon_list(request):
    is_cached = "data" in request.session
    params = {"pageSize": 30}

    if not is_cached:
        response = requests.get(API_DIGIMON_LIST, params=params)
        request.session["data"] = response.json()

    digimon_list = request.session["data"]

    # print(request.session["digimon_list"])

    # if not digimon_list:
    #     digimon_list = requests.get(API_DIGIMON_LIST, params=params).json()

    return render(
        request,
        "main/pages/home.html",
        {"data": digimon_list["content"], "is_cached": is_cached},
    )
