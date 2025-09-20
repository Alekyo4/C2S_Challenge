from abc import ABC, abstractmethod

from types import TracebackType

from typing import Self, Type

from c2s_challenge.common.setting import SettingProvider

class ServerProvider(ABC):
  @abstractmethod
  def __init__(self, setting: SettingProvider) -> None:
    raise NotImplementedError() 

class AsyncServerProvider(ServerProvider):
  @abstractmethod
  async def __aenter__(self) -> Self:
      raise NotImplementedError()

  @abstractmethod
  async def __aexit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
    raise NotImplementedError()
  
  @abstractmethod
  async def listen(self) -> None:
    raise NotImplementedError()

class SyncServerProvider(ServerProvider):
  @abstractmethod
  def __enter__(self) -> Self:
    raise NotImplementedError()
  
  @abstractmethod
  def __exit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
      raise NotImplementedError()
  
  @abstractmethod
  def listen(self) -> None:
    raise NotImplementedError()