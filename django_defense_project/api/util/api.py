from requests import get


def call(data_type, params, query):
    headers = {}
    if params is not None:
        params = {}
    endpoints = {
        "digimon": "https://digi-api.com/api/v1/digimon",
        "attribute": "https://digi-api.com/api/v1/attribute",
        "field": "https://digi-api.com/api/v1/field",
        "level": "https://digi-api.com/api/v1/level",
        "type": "https://digi-api.com/api/v1/type",
        "skill": "https://digi-api.com/api/v1/skill",
    }
    if query:
        url = f"{endpoints[data_type]}/{query}"
    else:
        url = f"{endpoints[data_type]}"
    return get(url, headers=headers, params=params)
