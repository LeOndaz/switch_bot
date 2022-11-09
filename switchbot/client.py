import base64
import hashlib
import hmac
import uuid
from collections.abc import Mapping
from functools import cached_property
from typing import List, Tuple
import httpx
from switchbot.utils import _decamelize_dict
from switchbot.exceptions import SwitchBotException


class SwitchBot(httpx.AsyncClient):
    MAX_HITS_PER_DAY = 10000  # TODO: implement throttling

    ROOT_URL = "https://api.switch-bot.com/v1.1"
    DEVICES_LIST_URL = "/devices"
    DEVICE_STATUS_URL = "/devices/{id}/status"
    SETUP_WEBHOOK_URL = "/webhook/setupWebhook"
    QUERY_WEBHOOK_URL = "/webhook/queryWebhook"
    DELETE_WEBHOOK_URL = "/webhook/deleteWebhook"

    def __init__(self, token, secret):
        self.token = token
        self.secret = bytes(secret, "utf8")

        self._t = str(uuid.uuid4())
        self._nonce = str(uuid.uuid4())

        super().__init__(headers=self._get_headers(), base_url=self.ROOT_URL)

    @cached_property
    def signature(self):
        to_sign = bytes(f"{self.token}{self._t}{self._nonce}", "utf8")
        return base64.b64encode(
            hmac.new(self.secret, msg=to_sign, digestmod=hashlib.sha256).digest()
        )

    def _get_headers(self):
        return {
            "authorization": self.token,
            "nonce": self._nonce,
            "t": self._t,
            "sign": self.signature,
            "content-type": "application/json",
        }

    def _object_hook(self, obj: Mapping):
        """
        A hook for jsonlib to decamelize all response data to be able to use snake_case
        """
        return _decamelize_dict(obj)

    def _parse_response(self, r):
        data = r.json(object_hook=self._object_hook)

        if data["status_code"] != httpx.codes.CONTINUE:
            raise SwitchBotException(data)

        return data["body"]

    async def request(self, *args, **kwargs):
        response = await super().request(*args, **kwargs)

        if response.status_code != httpx.codes.OK:
            raise SwitchBotException(response.text)

        return response

    async def get_device_status(self, id) -> Mapping:
        assert isinstance(id, str), "id must be a string"

        response = await self.get(self.DEVICE_STATUS_URL.format(id=id))
        return self._parse_response(response)

    async def devices(self) -> Tuple[List[Mapping], List[Mapping]]:
        response = await self.get(self.DEVICES_LIST_URL)
        data = self._parse_response(response)
        return data["device_list"], data["infrared_remote_list"]

    async def setup_webhook(self, url, device_list="ALL"):
        assert (
                device_list == "ALL"
        ), "The only allowed deviceList value currently is ALL"

        response = await self.post(
            self.SETUP_WEBHOOK_URL,
            json={"url": url, "deviceList": device_list, "action": "setupWebhook"},
        )

        return self._parse_response(response)

    async def query_webhook(self):
        response = await self.post(self.QUERY_WEBHOOK_URL, json={"action": "queryUrl"})

        return self._parse_response(response)

    async def delete_webhook(self, url):
        response = await self.post(
            self.DELETE_WEBHOOK_URL, json={"action": "deleteWebhook", "url": url}
        )

        return self._parse_response(response)
