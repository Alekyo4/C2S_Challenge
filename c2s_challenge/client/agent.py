from asyncio import to_thread

from tabulate import tabulate

from c2s_challenge.common.protocol.contracts import Request, RequestEvent, Response
from c2s_challenge.common.protocol.dto import (
    ChatMessageDto,
    VehicleChatIDto,
    VehicleChatODto,
    VehicleDto,
    VehicleFilterDto,
    VehicleSearchIDto,
    VehicleSearchODto,
)

from .provider import AsyncClientProvider


class VehicleAgent:
    client: AsyncClientProvider

    def __init__(self, client: AsyncClientProvider):
        self.client = client

    async def chat(self, history: list[ChatMessageDto]) -> VehicleChatODto:
        dto: VehicleChatIDto = VehicleChatIDto(history=history)

        request: Request = Request(event=RequestEvent.VEHICLE_CHAT, data=dto)

        response: Response = await self.client.send_request(request)

        return VehicleChatODto.model_validate(response.data)

    async def search(self, filter: VehicleFilterDto) -> VehicleSearchODto:
        dto: VehicleSearchIDto = VehicleSearchIDto(filter=filter)

        request: Request = Request(event=RequestEvent.VEHICLE_SEARCH, data=dto)

        response: Response = await self.client.send_request(request)

        return VehicleSearchODto.model_validate(response.data)

    async def run_interactive(self) -> None:
        while True:
            vehicle_filter: VehicleFilterDto = await self.__filter_interactive()

            vehicle_search: VehicleSearchODto = await self.search(vehicle_filter)

            await self.__display_vehicles(vehicle_search.result)

    async def __filter_interactive(self) -> VehicleFilterDto:
        history: list[ChatMessageDto] = [
            ChatMessageDto(
                role="user",
                content="Hello, I'm looking for the perfect car.",
            )
        ]

        chat_welcome: VehicleChatODto = await self.chat(history)

        print(f"\033[92m🤖: {chat_welcome.content}")

        history.append(ChatMessageDto(role="assistant", content=chat_welcome.content))

        while True:
            user_prompt: str = await to_thread(input, "\033[92m📤: ")

            history.append(ChatMessageDto(role="user", content=user_prompt))

            chat_response: VehicleChatODto = await self.chat(history)

            if chat_response.type == "filter":
                return chat_response.content

            history.append(
                ChatMessageDto(role="assistant", content=chat_response.content)
            )

            print(f"\033[92m🤖: {chat_response.content}")

    async def __display_vehicles(self, vehicles: list[VehicleDto]) -> None:
        headers: list[str] = [
            "Vin",
            "Make",
            "Model",
            "Fuel Type",
            "Color",
            "Year",
            "Price",
        ]

        table_data: list[list[str]] = []

        for vehicle in vehicles:
            table_data.append(
                [
                    vehicle.vin,
                    vehicle.make.capitalize(),
                    vehicle.model.capitalize(),
                    vehicle.fuel_type,
                    vehicle.color,
                    vehicle.year,
                    vehicle.price,
                ]
            )

        table: str = tabulate(table_data, headers=headers, tablefmt="outline")

        print(f"\033[92m{table}\n")
