from requests import get
from .config import endpoints, templates


def compileQuery(data_type, query="", id=""):
    target = ""

    if query:
        target = query
    if id:
        target = id

    if target:
        url = f"{endpoints[data_type]}/{target}"
    else:
        url = f"{endpoints[data_type]}"

    return url


def call(data_type, params={}, query="", id=""):
    error = False
    headers = {}

    try:
        url = compileQuery(data_type, query, id)

        data = get(url, headers=headers, params=params)
        if data:
            data = data.json()
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
