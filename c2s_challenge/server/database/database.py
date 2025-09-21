from sqlalchemy import create_engine, Engine

from sqlalchemy.orm import Session, sessionmaker

from c2s_challenge.common.setting import SettingProvider

from .orm import BaseORM

from .abstract import DatabaseProvider


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
