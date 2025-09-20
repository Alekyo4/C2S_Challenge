from c2s_challenge.common.protocol import Response

from c2s_challenge.common.protocol.dto import VehicleSearchChatIDto, VehicleSearchChatODto

from c2s_challenge.server.agent import AgentAIProvider

from ..abstract import EventHandler

class VehicleSearchChatHandler(EventHandler):
  agent_ai: AgentAIProvider

  def __init__(self, agent_ai: AgentAIProvider):
    self.agent_ai = agent_ai

  async def handle(self, data: VehicleSearchChatIDto) -> Response:
    result: VehicleSearchChatODto = VehicleSearchChatODto(finished=True, content="Finished")

    return Response(status="success", data=result)