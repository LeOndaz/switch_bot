from switchbot.api import SwitchBotAPIClient
from switchbot.devices import factory


class SwitchBot:
    def __init__(self, token, secret):
        self.api_client = SwitchBotAPIClient(token, secret)

    async def devices(self):
        data = await self.api_client.devices()  # IR: TODO
        devices = []

        for item in data:
            device = factory.device_factory(self.api_client, item)
            devices.append(device)

        return devices

