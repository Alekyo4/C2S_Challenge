from c2s_challenge.common.setting import Setting, SettingProvider

from .abstract import AsyncClientProvider, SyncClientProvider


def make_client_sync(setting: SettingProvider | None = None) -> SyncClientProvider:
    """Factory function to create a SyncClient instance."""
    raise NotImplementedError()


def make_client_async(setting: SettingProvider | None = None) -> AsyncClientProvider:
    """Factory function to create a AsyncClient instance."""
    from .client import AsyncClient

    if setting is None:
        setting = Setting()

    return AsyncClient(setting=setting)
