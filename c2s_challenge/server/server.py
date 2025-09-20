from asyncio import (
  Server as AsyncIoServer,
  StreamReader,
  StreamWriter,
  start_server as async_server)

from types import TracebackType

from typing import Self

from c2s_challenge.common.protocol import Protocol, Request, Response

from c2s_challenge.common.protocol.exception import ProtocolRequestInvalid, ProtocolNotFoundEvent

from c2s_challenge.common.setting import SettingProvider

from .event import EventRouterProvider

from .exception import ServerWithoutContext

from .abstract import AsyncServerProvider

class AsyncServer(AsyncServerProvider):
  io: AsyncIoServer
  
  def __init__(self, setting: SettingProvider, router: EventRouterProvider):
    super().__init__(setting=setting, router=router)
  
  async def __aenter__(self) -> Self:
    self.io = await async_server(
      self.__handle_request, self.host, self.port)

    return self
  
  async def __aexit__(
      self,
      _exc_type: type[BaseException] | None,
      _exc_val: BaseException | None,
      _exc_tb: TracebackType | None,
    ) -> None:
    if not self.io:
      return
    
    self.io.close()
    
    await self.io.wait_closed()
  
  async def __handle_request(self, reader: StreamReader, writer: StreamWriter):
    try:
      while True:
        try:
          raw: bytes = await reader.readline()

          if not raw:
            break

          request: Request = Protocol.parse_request(raw)

          response: Response = await self.router.route(request)
        except (ProtocolRequestInvalid, ProtocolNotFoundEvent) as e:
          response: Response = Response(status="error", data=str(e))
        except Exception:
          response: Response = Response(status="error", data="An internal server error occurred")

        writer.write(response.model_dump_json().encode("utf-8") + b"\n")

        await writer.drain()
    finally:
      writer.close()
      
      await writer.wait_closed()
  
  async def listen(self) -> None:
    if not self.io:
      raise ServerWithoutContext()
    
    async with self.io:
      await self.io.serve_forever()