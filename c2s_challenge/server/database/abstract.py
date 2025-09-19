from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from urllib.parse import urlparse

from c2s_challenge.config import ConfigProvider

class DatabaseProvider(ABC):
  def __init__(self, config: ConfigProvider) -> None:
    connc: str = config.get_required("DB_URL")

    self.db_url = urlparse(connc).geturl()

  @abstractmethod
  def get_session(self) -> Session:
    raise NotImplementedError()