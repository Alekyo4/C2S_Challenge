from abc import ABC, abstractmethod

from c2s_challenge.config import ConfigProvider

class ServerProvider(ABC):
  @abstractmethod
  def __init__(self, config: ConfigProvider) -> None:
    raise NotImplementedError()

  @abstractmethod
  def listen(self) -> None:
    raise NotImplementedError()