class ProtocolRequestInvalid(Exception):
    def __init__(self):
        super().__init__("The structure of the request sent to the server is invalid")


class ProtocolResponseInvalid(Exception):
    def __init__(self):
        super().__init__(
            "The structure of the response received from the server is invalid"
        )


class ProtocolNotFoundEvent(Exception):
    def __init__(self):
        super().__init__("The sent event is not mapped as valid on the server")
