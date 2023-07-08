ENDPOINT = "https://digimon-api.com/images/etc/fields"


def attachFieldLinks(data):
    array_data = data.get("content", False)
    if array_data:
        return data
    else:
        fields = data.get("fields", False)
        if fields:
            for item in data["fields"]:
                try:
                    item["href"] = f"{ENDPOINT}/{item['field']}.png"
                except Exception as e:
                    print(e)
            return data
        else:
            return data
