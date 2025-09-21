from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from c2s_challenge.common.setting import SettingProvider

from .abstract import DatabaseProvider
from .orm import BaseORM


class Database(DatabaseProvider):
    engine: Engine

    session_factory: sessionmaker[Session]

    def __init__(self, setting: SettingProvider) -> None:
        super().__init__(setting)

        self.engine = create_engine(self.db_url, echo=setting.is_dev())

        self.session_factory = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False
        )

        if setting.is_dev():
            BaseORM.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.session_factory()
