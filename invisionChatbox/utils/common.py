
def replace_many(items: list, text: str, replace_with=''):
    for i in items:
        text.replace(i, replace_with)
    return text


def safe_get(data: dict, key: str, data_type, default):
    return resp if (resp := data.get(key)) and isinstance(resp, data_type) else default
