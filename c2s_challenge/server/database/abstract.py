from abc import ABC, abstractmethod

from contextlib import contextmanager

from sqlalchemy.orm import Session

from pydantic import BaseModel

from urllib.parse import urlparse

from c2s_challenge.common.setting import SettingProvider


class DatabaseProvider(ABC):
    db_url: str

    def __init__(self, setting: SettingProvider) -> None:
        connc: str = setting.get_required("DB_URL")

        self.db_url = urlparse(connc).geturl()

    @abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError()


class DatabaseRepository(ABC):
    @abstractmethod
    def __init__(self, database: DatabaseProvider):
        raise NotImplementedError()

    @abstractmethod
    @contextmanager
    def add(self, vehicle: BaseModel) -> BaseModel:
        raise NotImplementedError()
