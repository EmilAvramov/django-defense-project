ENDPOINT = "https://digimon-api.com/images/etc/fields"


def attachFieldLinks(data):
    data = data.json()
    array_data = data.get("content", False)
    if array_data:
        return data
    else:
        fields = data.get("fields", False)
        if fields:
            for item in data["fields"]:
                print(item)
                try:
                    item["href"] = f"{ENDPOINT}/{item['field']}.png"
                except Exception as e:
                    print(e)
                print(item)
            return data
        else:
            return data
