from abc import ABC, abstractmethod

from pydantic import BaseModel

from c2s_challenge.common.protocol import Request, Response

from c2s_challenge.common.protocol.model import RequestEvent

class EventHandler(ABC):
  @abstractmethod
  async def handle(self, data: BaseModel) -> Response:
    raise NotImplementedError()

class EventRouterProvider(ABC):
  handlers: dict[RequestEvent, EventHandler]
  
  @abstractmethod
  async def route(self, request: Request) -> Response:
    raise NotImplementedError()