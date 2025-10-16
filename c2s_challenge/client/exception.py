from c2s_challenge.common.protocol import Response


class ClientWithoutContext(Exception):
    def __init__(self) -> None:
        super().__init__("Client not started. Use 'async with Client(...) as cl:'")


class ClientResponseError(Exception):
    def __init__(self, response: Response) -> None:
        if response.status != "error":
            raise TypeError(
                "The response that was used for the exception is not marked as unresolved."
            )

        super().__init__(f"Error handling response: {str(response.data)}")
