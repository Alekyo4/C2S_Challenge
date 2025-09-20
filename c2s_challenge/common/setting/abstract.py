from abc import ABC, abstractmethod

class SettingProvider(ABC):
  @abstractmethod
  def __init__(self, initial: dict[str, str] = {}) -> None:
    raise NotImplementedError()
  
  @abstractmethod
  def get(self, key: str, default: str | None = None) -> str | None:
    raise NotImplementedError()

  @abstractmethod
  def get_required(self, key: str) -> str:
    raise NotImplementedError()
  
  @abstractmethod
  def is_dev(self) -> bool:
    raise NotImplementedError()