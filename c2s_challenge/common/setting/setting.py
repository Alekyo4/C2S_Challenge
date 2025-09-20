from dotenv import dotenv_values

from .abstract import SettingProvider

from .exception import SettingNotFound

class Setting(SettingProvider):
  envs: list[str] = ["development", "production"]

  __raw: dict[str, str] = {}

  def __init__(self, initial: dict[str, str] = {}) -> None:
    self.__raw = initial

    self.__load()

  def __load(self) -> None:
    for stage in self.envs:
      self.__raw.update(dotenv_values(f".env.{stage}"))

    self.__raw.update(dotenv_values())

  def get(self, key: str, default: str | None = None) -> str | None:
    return self.__raw.get(key, default)
  
  def get_required(self, key: str) -> str:
    value: str | None = self.get(key, None)

    if value is None:
      raise SettingNotFound(key)

    return value
  
  def is_dev(self) -> bool:
    return self.get("ENV", "development") == "development"