from c2s_challenge.common.protocol import Response
from c2s_challenge.common.protocol.dto import (
    VehicleChatIDto,
    VehicleChatODto,
    VehicleFilterDto,
)
from c2s_challenge.server.aicore import LLMProvider
from c2s_challenge.server.aicore.contracts import LLMResponse

from ..provider import EventHandler


class VehicleChatHandler(EventHandler):
    llm: LLMProvider

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def handle(self, data: VehicleChatIDto) -> Response:
        chat_tool: dict[str, any] = {
            "name": "search_for_vehicles",
            "description": "Search for vehicles in the database using filters extracted from the conversation with the user",
        }

        res_chat: LLMResponse = await self.llm.get_chat_response(
            history=data.history,
            tools=[chat_tool],
        )

        if not res_chat.is_tool_call:
            result: VehicleChatODto = VehicleChatODto(
                type="text", content=res_chat.text
            )

            return Response(data=result)

        res_extract: LLMResponse = await self.llm.extract_structured(
            history=data.history, schema=VehicleFilterDto
        )

        result: VehicleChatODto = VehicleChatODto(
            type="filter", content=res_extract.tool_arguments
        )

        return Response(data=result)
