from asyncio import StreamReader, StreamWriter, open_connection, to_thread
from functools import wraps
from types import TracebackType
from typing import Callable, Self

from c2s_challenge.common.logger import Logger, get_logger
from c2s_challenge.common.protocol import Protocol, Request, Response
from c2s_challenge.common.protocol.dto import (
    ChatMessageDto,
    VehicleChatIDto,
    VehicleChatODto,
)
from c2s_challenge.common.protocol.model import RequestEvent
from c2s_challenge.common.setting import SettingProvider

from .abstract import AsyncClientProvider
from .exception import ClientResponseError, ClientWithoutContext


class AsyncClient(AsyncClientProvider):
    __reader: StreamReader | None = None

    __writer: StreamWriter | None = None

    logger: Logger = get_logger("AsyncClient")

    def __init__(self, setting: SettingProvider):
        super().__init__(setting=setting)

    async def __aenter__(self) -> Self:
        self.__reader, self.__writer = await open_connection(self.host, self.port)

        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        if not self.__writer:
            return

        if self.__writer.can_write_eof():
            self.__writer.write_eof()

        self.__writer.close()

        await self.__writer.wait_closed()

        self.__writer = None
        self.__reader = None

    @staticmethod
    def __require_connection(func: Callable):
        @wraps(func)
        async def wrapper(self: Self, *args: tuple, **kwargs: dict[str, any]):
            if not self.__writer or not self.__reader:
                raise ClientWithoutContext()

            return await func(self, *args, **kwargs)

        return wrapper

    @__require_connection
    async def __send_request(self, request: Request) -> Response:
        request_raw: bytes = request.model_dump_json().encode("utf-8")

        self.__writer.write(request_raw + b"\n")

        await self.__writer.drain()

        response_raw: bytes = await self.__reader.readuntil()

        return Protocol.parse_response(response_raw)

    @__require_connection
    async def __ask_vehicle_chat(self, history: list[ChatMessageDto]) -> Response:
        dto: VehicleChatIDto = VehicleChatIDto(history=history)

        request: Request = Request(event=RequestEvent.VEHICLE_CHAT, data=dto)

        return await self.__send_request(request)

    @__require_connection
    async def vehicle_chat(self) -> VehicleChatODto:
        history: list[ChatMessageDto] = []

        # history.append(
        #     ChatMessageDto(
        #         role="user",
        #         content="Hello, I'm looking for the perfect car.",
        #     )
        # )

        # res_welcome: Response = await self.__ask_vehicle_chat(history)

        # print(f"🤖: {res_welcome.data.content}")

        while True:
            user_prompt: str = await to_thread(input, "📤: ")

            history.append(ChatMessageDto(role="user", content=user_prompt))

            response: Response = await self.__ask_vehicle_chat(history)

            if response.status != "success":
                raise ClientResponseError(response)

            result: VehicleChatODto = response.data

            if result.type == "filter":
                return result

            history.append(ChatMessageDto(role="assistant", content=result.content))

            print(f"🤖: {result.content}")

    async def start(self) -> None:
        vehicle_chat: VehicleChatODto = await self.vehicle_chat()

        print(vehicle_chat)
