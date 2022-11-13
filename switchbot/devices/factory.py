from switchbot.devices.physical import (
    PlugMiniUS,
    PlugMiniJP,
    Meter,
    MeterPlus,
    Bot,
    Curtain,
)
from switchbot.enums import DeviceType


def device_factory(client, data):
    if data.get("device_type"):
        return physical_device_factory(client, data)

    return infra_device_factory(client, data)


def physical_device_factory(client, data):
    type_ = data["device_type"]

    if type_ == DeviceType.PLUG_MINI_US:
        return PlugMiniUS(client, data)

    if type_ == DeviceType.PLUG_MINI_JP:
        return PlugMiniJP(client, data)

    if type_ == DeviceType.METER:
        return Meter(client, data)

    if type_ == DeviceType.METER_PLUS:
        return MeterPlus(client, data)

    if type_ == DeviceType.CURTAIN:
        return Curtain(client, data)

    if type_ == DeviceType.BOT:
        return Bot(client, data)


def infra_device_factory(client, data):
    return
