from abc import ABC, abstractmethod
from contextlib import contextmanager

from sqlalchemy.orm import Session

from c2s_challenge.common.setting import SettingProvider


class DatabaseProvider(ABC):
    db_url: str

    def __init__(self, setting: SettingProvider) -> None:
        self.db_url = setting.get_required("DATABASE_URL")

    @abstractmethod
    @contextmanager
    def get_session(self) -> Session:
        raise NotImplementedError()
