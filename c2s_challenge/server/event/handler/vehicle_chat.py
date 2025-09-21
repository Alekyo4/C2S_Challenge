from c2s_challenge.common.protocol import Response

from c2s_challenge.common.protocol.dto import (
    VehicleFilterDto,
    VehicleChatIDto,
    VehicleChatODto,
)

from c2s_challenge.server.agent import AgentAIProvider

from c2s_challenge.server.agent.model import LLMResponse

from ..abstract import EventHandler


class VehicleChatHandler(EventHandler):
    agent_ai: AgentAIProvider

    def __init__(self, agent_ai: AgentAIProvider):
        self.agent_ai = agent_ai

    async def handle(self, data: VehicleChatIDto) -> Response:
        res_chat: LLMResponse = await self.agent_ai.get_chat_response(
            data.history,
            tools=[
                {
                    "name": "search_for_vehicles",
                    "description": "Search for vehicles in the database using filters extracted from the conversation with the user",
                }
            ],
        )

        if not res_chat.is_tool_call:
            result: VehicleChatODto = VehicleChatODto(
                finished=False, content=res_chat.text
            )

            return Response(status="success", data=result)

        res_extract: LLMResponse = await self.agent_ai.extract_structured(
            data.history, VehicleFilterDto
        )

        result: VehicleChatODto = VehicleChatODto(
            finished=True, content=res_extract.tool_arguments
        )

        return Response(status="success", data=result)
