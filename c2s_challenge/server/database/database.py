from sqlalchemy import create_engine, Engine

from sqlalchemy.orm import Session, sessionmaker

from c2s_challenge.config import ConfigProvider

from .models import ORM

from .database import DatabaseProvider

class Database(DatabaseProvider):
  engine: Engine
  
  session_factory: sessionmaker[Session]
  
  def __init__(self, config: ConfigProvider) -> None:
    super().__init__(config)

    self.engine = create_engine(self.db_url, echo=config.is_dev())

    self.session_factory = sessionmaker(
      bind=self.engine,
      autoflush=False,
      autocommit=False)
    
    if config.is_dev():
      ORM.metadata.create_all(self.engine)

  def get_session(self) -> Session:
    return self.session_factory()