import pytest

from c2s_challenge.common.setting import Setting, SettingProvider


@pytest.fixture(scope="session")
def mock_setting() -> SettingProvider:
    override: dict[str, str] = {
        "ENV": "development",
        "DATABASE_URL": "sqlite:///:memory:",
    }

    return Setting(override=override)
