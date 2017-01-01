import json


def read_dict(data):
    if not isinstance(data, str):
        return data

    try:
        data = open(data).read()
    except:
        pass
    return json.loads(data)
