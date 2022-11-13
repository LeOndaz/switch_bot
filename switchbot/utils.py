import re
from collections.abc import Mapping

from humps import decamelize

titled_words = re.compile("[A-Z][a-z0-9]*")


def _decamelize_dict(obj: Mapping):
    new_obj = {}

    for key, val in obj.items():
        key = decamelize(key)

        if isinstance(val, Mapping):
            new_obj[key] = _decamelize_dict(val)
        else:
            new_obj[key] = val

    return new_obj


def pascalise_name(name):
    matches = titled_words.findall(name)
    return " ".join(matches)
