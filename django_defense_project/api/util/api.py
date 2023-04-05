from requests import get
from .config import endpoints, templates
from .attachFieldLinks import attachFieldLinks


def call(data_type, params={}, query="", id=""):
    error = False
    headers = {}
    single = ""

    if query:
        single = query
    if id:
        single = id

    try:
        if single:
            url = f"{endpoints[data_type]}/{single}"
        else:
            url = f"{endpoints[data_type]}"

        data = get(url, headers=headers, params=params)
        if data:
            data = attachFieldLinks(data)
            return {
                "data": data,
                "error": error,
                "template": templates[data_type],
            }
        else:
            raise Exception("No data found")
    except Exception:
        error = True
        return {"data": None, "error": error, "template": templates["error"]}
