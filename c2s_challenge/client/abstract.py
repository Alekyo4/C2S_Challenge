from abc import ABC, abstractmethod

from types import TracebackType

from typing import Self

from c2s_challenge.common.setting import SettingProvider

class ClientProvider(ABC):
  host: str
  port: int
  
  def __init__(self, setting: SettingProvider):
    self.port = int(setting.get_required("SV_PORT"))
    
    self.host = setting.get_required("SV_HOST")

class AsyncClientProvider(ClientProvider):
  @abstractmethod
  async def __aenter__(self) -> Self:
      raise NotImplementedError()

  @abstractmethod
  async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
    raise NotImplementedError()
  
  @abstractmethod
  async def start(self) -> None:
    raise NotImplementedError()

class SyncClientProvider(ClientProvider):
  @abstractmethod
  def __enter__(self) -> Self:
    raise NotImplementedError()

  @abstractmethod
  def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
    raise NotImplementedError()
  
  @abstractmethod
  def start(self) -> None:
    raise NotImplementedError()