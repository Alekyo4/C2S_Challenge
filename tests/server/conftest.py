import pytest

from c2s_challenge.common.setting import SettingProvider
from c2s_challenge.server.database import Database, DatabaseProvider


@pytest.fixture(scope="function")
def mock_database(mock_setting: SettingProvider) -> DatabaseProvider:
    return Database(setting=mock_setting)
