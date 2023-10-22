def merge(*dicts):
    result = {}
    for dict_ in dicts:
        result = result | dict_

    return result
