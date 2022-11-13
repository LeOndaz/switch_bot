from switchbot.exceptions import SwitchBotException, InvalidStatusException
from switchbot.api import SwitchBotAPIClient


class SwitchBotDevice:
    status_class = None

    def __init__(self, client: SwitchBotAPIClient, data):
        self.client = client
        self.data = data

    async def status(self):
        raise NotImplementedError

    def validate_status(self, status):
        # BUG in SwitchBot API
        if not status:
            raise InvalidStatusException()

        for field_name in self.status_class.__dataclass_fields__.keys():
            cls_name = self.__class__.__name__

            if status.get(field_name) is None:
                raise SwitchBotException(f"Missing required field {field_name}")

            if status.get(field_name) is None:
                raise SwitchBotException(
                    f"Missing field: {field_name} for device {cls_name}"
                )

    def __repr__(self):
        return self.__class__.__qualname__ + f"(client={self.client}, data={repr(self.data)})"
