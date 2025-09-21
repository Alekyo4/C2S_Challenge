from asyncio import to_thread

from c2s_challenge.client.exception import ClientResponseError
from c2s_challenge.common.protocol.dto import (
    ChatMessageDto,
    VehicleChatIDto,
    VehicleChatODto,
    VehicleFilterDto,
    VehicleSearchIDto,
    VehicleSearchODto,
)
from c2s_challenge.common.protocol.model import Request, RequestEvent, Response

from .abstract import AsyncClientProvider


class VehicleAgent:
    client: AsyncClientProvider

    def __init__(self, client: AsyncClientProvider):
        self.client = client

    async def __send_vehicle_chat(self, history: list[ChatMessageDto]) -> Response:
        dto: VehicleChatIDto = VehicleChatIDto(history=history)

        request: Request = Request(event=RequestEvent.VEHICLE_CHAT, data=dto)

        return await self.client.send_request(request)

    async def _send_vehicle_search(self, filter: VehicleFilterDto) -> Response:
        dto: VehicleSearchIDto = VehicleSearchIDto(filter=filter)

        request: Request = Request(event=RequestEvent.VEHICLE_SEARCH, data=dto)

        return await self.client.send_request(request)

    async def filter_interactive(self) -> VehicleFilterDto:
        history: list[ChatMessageDto] = []

        history.append(
            ChatMessageDto(
                role="user",
                content="Hello, I'm looking for the perfect car.",
            )
        )

        res_welcome: Response = await self.__send_vehicle_chat(history)

        print(f"🤖: {res_welcome.data.content}")

        while True:
            user_prompt: str = await to_thread(input, "📤: ")

            history.append(ChatMessageDto(role="user", content=user_prompt))

            response: Response = await self.__send_vehicle_chat(history)

            if response.status != "success":
                raise ClientResponseError(response)

            result: VehicleChatODto = response.data

            if result.type == "filter":
                return result.content

            history.append(ChatMessageDto(role="assistant", content=result.content))

            print(f"🤖: {result.content}")

    async def search(self, filter: VehicleFilterDto) -> VehicleSearchODto:
        pass

    async def search_interactive(self) -> None:
        while True:
            vehicle_filter: VehicleFilterDto = await self.filter_interactive()

            vehicle_search: VehicleSearchODto = await self.search(vehicle_filter)

            print(vehicle_search)
