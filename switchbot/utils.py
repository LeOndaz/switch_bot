from collections.abc import Mapping
from humps import decamelize

_twelve_zeros = "".join([str(0) for i in range(12)])  # 12 zeros


def _decamelize_dict(obj: Mapping):
    new_obj = {}

    for key, val in obj.items():
        key = decamelize(key)

        if isinstance(val, Mapping):
            new_obj[key] = _decamelize_dict(val)
        else:
            new_obj[key] = val

    return new_obj


def is_hub(device):
    if isinstance(device, Mapping):
        value = device.get("hub_device_id")

        if value:
            return value == _twelve_zeros

    elif hasattr(device, "hub_device_id"):
        return getattr(device, "hub_device_id") == _twelve_zeros

    raise TypeError(f"{device} is not a valid device")
