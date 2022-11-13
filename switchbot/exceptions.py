class SwitchBotException(Exception):
    """
    An exception for SwitchBot
    """


class InvalidStatusException(SwitchBotException):
    """
    Raise if SwitchBot API returns empty status for a device
    """

    def __init__(self, *args):
        super().__init__("Invalid status received from SwitchBot API", *args)
