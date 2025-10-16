from c2s_challenge.client.agent import VehicleAgent
from c2s_challenge.common.setting import Setting, SettingProvider

from .provider import AsyncClientProvider, SyncClientProvider


def make_client_sync(setting: SettingProvider | None = None) -> SyncClientProvider:
    raise NotImplementedError()


def make_client_async(setting: SettingProvider | None = None) -> AsyncClientProvider:
    from .client import AsyncClient

    if setting is None:
        setting = Setting()

    return AsyncClient(setting=setting)


async def make_vehicle_agent(client: AsyncClientProvider) -> VehicleAgent:
    return VehicleAgent(client=client)
