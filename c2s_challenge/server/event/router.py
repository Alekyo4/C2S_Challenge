from c2s_challenge.common.protocol import Request, Response
from c2s_challenge.common.protocol.contracts import RequestEvent

from .provider import EventHandler, EventRouterProvider


class EventRouter(EventRouterProvider):
    def __init__(self, handlers: dict[RequestEvent, EventHandler]):
        self.handlers = handlers

    async def route(self, request: Request) -> Response:
        handler: EventHandler | None = self.handlers.get(request.event)

        if not handler:
            return Response(
                status="error",
                data=f"no route found for received event '{request.event.evt_name}'",
            )

        return await handler.handle(request.data)
