from requests import get
from .config import endpoints, templates


def call(data_type, params={}, query=""):
    error = False
    headers = {}

    try:
        if query:
            url = f"{endpoints[data_type]}/{query}"
        else:
            url = f"{endpoints[data_type]}"

        data = get(url, headers=headers, params=params)
    except Exception:
        error = True
        return {"data": None, "error": error, "template": templates["error"]}

    return {"data": data, "error": error, "template": templates[data_type]}
