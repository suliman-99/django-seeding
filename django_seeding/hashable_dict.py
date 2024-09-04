

def dict_to_tuple(d: dict):
    return tuple(sorted([(k, dict_to_tuple(v)) if isinstance(v, dict) else (k, v) for k, v in d.items()]))


class HashableDict(dict):
    def __init__(self, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = HashableDict(value)
        super().__init__(data)

    def __hash__(self):
        return hash(dict_to_tuple(self))
