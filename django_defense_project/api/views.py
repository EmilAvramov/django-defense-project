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
    is_cached = ('digimon_list' in request.session)
    
    if not is_cached:
        response = requests.get(API_DIGIMON_LIST)
        request.session['digimon_list'] = response.json()

    digimon_list = request.session['digimon_list']

    return render(request, 'main/pages/home', {
        'digimon_data': digimon_list
    })