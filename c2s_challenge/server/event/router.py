from c2s_challenge.common.protocol import Request, Response

from c2s_challenge.common.protocol.model import RequestEvent

from .abstract import EventRouterProvider, EventHandler

class EventRouter(EventRouterProvider):
  __handlers: dict[RequestEvent, EventHandler]

  def __init__(self, handlers: dict[RequestEvent, EventHandler]):
    self.__handlers = handlers

  async def route(self, request: Request) -> Response:
    handler: EventHandler | None = self.__handlers.get(request.event)
    
    if not handler:
      return Response(status="error", data=f"no route found for received event '{request.event.evt_name}'")
    
    return await handler.handle(request.data)