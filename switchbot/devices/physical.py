from switchbot.devices import SwitchBotDevice
from switchbot.api import SwitchBotAPIClient
from switchbot.devices.status import (
    PlugMiniUSStatus,
    PlugMiniJPStatus,
    MeterStatus,
    MeterPlusStatus,
    BotStatus,
    CurtainStatus,
)


class PhysicalDevice(SwitchBotDevice):
    def __init__(self, client: SwitchBotAPIClient, data):
        super().__init__(client, data)
        self.id = data["device_id"]
        self.name = data["device_name"]
        self.type = data["device_type"]
        self.hub_device_id = data["hub_device_id"]

    async def status(self):
        """
        Base implementation
        """
        status = await self.client.get_device_status(self.id)

        del status["device_id"]
        del status["device_type"]

        self.validate_status(status)
        return self.status_class(**status)


class PlugMiniUS(PhysicalDevice):
    status_class = PlugMiniUSStatus


class PlugMiniJP(PhysicalDevice):
    status_class = PlugMiniJPStatus


class Meter(PhysicalDevice):
    status_class = MeterStatus


class MeterPlus(PhysicalDevice):
    status_class = MeterPlusStatus


class Bot(PhysicalDevice):
    status_class = BotStatus


class Curtain(PhysicalDevice):
    status_class = CurtainStatus
