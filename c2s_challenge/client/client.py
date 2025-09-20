from asyncio import StreamReader, StreamWriter, open_connection, to_thread

from types import TracebackType

from typing import Callable, Self

from functools import wraps

from c2s_challenge.common.setting import SettingProvider

from c2s_challenge.common.protocol import Protocol, Request, Response

from c2s_challenge.common.protocol.model import RequestEvent

from c2s_challenge.common.protocol.dto import VehicleSearchIDto, VehicleSearchODto

from c2s_challenge.common.logger import Logger, get_logger

from .exception import ClientWithoutContext

from .abstract import AsyncClientProvider

class AsyncClient(AsyncClientProvider):
  __reader: StreamReader | None = None

  __writer: StreamWriter | None = None

  logger: Logger = get_logger("AsyncClient")
  
  def __init__(self, setting: SettingProvider):
    super().__init__(setting=setting)

  async def __aenter__(self) -> Self:
    self.__reader, self.__writer = await open_connection(self.host, self.port)

    return self
  
  async def __aexit__(
    self,
    _exc_type: type[BaseException] | None,
    _exc_val: BaseException | None,
    _exc_tb: TracebackType | None,
  ) -> None:
    if not self.__writer:
      return
    
    if self.__writer.can_write_eof():
      self.__writer.write_eof()

    self.__writer.close()
    
    await self.__writer.wait_closed()

    self.__writer = None
    self.__reader = None
  
  @staticmethod
  def __require_connection(func: Callable):
    @wraps(func)
    async def wrapper(self: Self, *args: tuple, **kwargs: dict[str, any]):
      if not self.__writer or not self.__reader:
        raise ClientWithoutContext()
      
      return await func(self, *args, **kwargs)

    return wrapper
  
  @__require_connection
  async def __send_request(self, request: Request) -> Response:
    request_raw: bytes = request.model_dump_json().encode("utf-8")
    
    self.__writer.write(request_raw)

    await self.__writer.drain()
    
    response_raw: bytes = await self.__reader.read(4096)

    return Protocol.parse_response(response_raw)
  
  async def start(self) -> None:
    print("🤖 Olá! Sou seu assistente automotivo. Como posso ajudar a encontrar seu próximo carro?")

    dto: VehicleSearchIDto = VehicleSearchIDto(make="123", model="testando")

    request: Request = Request(event=RequestEvent.VEHICLE_SEARCH, data=dto)

    vehicle_search: VehicleSearchODto = await self.__send_request(request)

    print(vehicle_search)