from asyncio import (
  Server as AsyncIoServer,
  StreamReader,
  StreamWriter,
  start_server as async_server)

from types import TracebackType

from typing import Self, Type

from c2s_challenge.common.protocol import Protocol, Request, Response

from c2s_challenge.common.protocol.exception import ProtocolRequestInvalid, ProtocolNotFoundEvent

from c2s_challenge.common.setting import SettingProvider

from .event import EventRouterProvider

from .exception import ServerWithoutContext

from .abstract import AsyncServerProvider

class AsyncServer(AsyncServerProvider):
  io: AsyncIoServer

  router: EventRouterProvider

  host: str
  port: int
  
  def __init__(self, setting: SettingProvider, router: EventRouterProvider):
    self.host = setting.get_required("SV_HOST")

    self.port = int(setting.get_required("SV_PORT"))

    self.router = router
  
  async def __aenter__(self) -> Self:
    self.io = await async_server(
      self.__handle_request, self.host, self.port)

    return self
  
  async def __aexit__(
      self,
      _exc_type: Type[BaseException] | None,
      _exc_val: BaseException | None,
      _exc_tb: TracebackType | None,
    ) -> None:
    if not hasattr(self, 'io') or not self.io:
      return
    
    self.io.close()
    
    await self.io.wait_closed()
  
  async def __handle_request(self, reader: StreamReader, writer: StreamWriter):
    response: Response | None = None

    try:
      raw: bytes = await reader.read(4096)

      if not raw:
        return
      
      request: Request = Protocol.parse_request(raw)

      response = await self.router.route(request)
    except (ProtocolRequestInvalid, ProtocolNotFoundEvent) as e:
      response = Response(status="error", data=str(e))
    except Exception:
      response = Response(status="error", data="An internal server error occurred")
    finally:
      if response:
        writer.write(response.model_dump_json().encode("utf-8"))

        await writer.drain()

      if writer.can_write_eof():
        writer.write_eof()

      writer.close()

      await writer.wait_closed()
  
  async def listen(self) -> None:
    if not hasattr(self, "io") or not self.io:
      raise ServerWithoutContext()
    
    async with self.io:
      await self.io.serve_forever()