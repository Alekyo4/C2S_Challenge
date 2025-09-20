from asyncio import (
  Server as AsyncIoServer,
  StreamReader,
  StreamWriter,
  start_server as async_server)

from types import TracebackType

from typing import Self, Type

from c2s_challenge.config import ConfigProvider

from .exception import ServerWithoutContext

from .abstract import AsyncServerProvider

class AsyncServer(AsyncServerProvider):
  io: AsyncIoServer

  host: str
  port: int

  def __init__(self, config: ConfigProvider):
    self.host = config.get_required("SV_HOST")

    self.port = int(config.get_required("SV_PORT"))
  
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
    addr: any = writer.get_extra_info("peername")

    print(addr)

    writer.close()

    await writer.wait_closed()
  
  async def listen(self) -> None:
    if not hasattr(self, "io") or not self.io:
      raise ServerWithoutContext()
    
    async with self.io:
      await self.io.serve_forever()