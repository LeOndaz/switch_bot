import decimal
from dataclasses import dataclass


@dataclass
class BaseDeviceStatus:
    hub_device_id: str


@dataclass
class PlugMiniStatus(BaseDeviceStatus):
    power: bool
    voltage: decimal.Decimal
    weight: decimal.Decimal
    electricity_of_day: decimal.Decimal
    electric_current: decimal.Decimal


@dataclass
class PlugMiniUSStatus(PlugMiniStatus):
    pass


@dataclass
class PlugMiniJPStatus(PlugMiniStatus):
    pass


@dataclass
class MeterStatus(BaseDeviceStatus):
    temperature: decimal.Decimal
    humidity: decimal.Decimal


@dataclass
class MeterPlusStatus(MeterStatus):
    pass


@dataclass
class BotStatus(BaseDeviceStatus):
    power: bool


@dataclass
class CurtainStatus(BaseDeviceStatus):
    pass
