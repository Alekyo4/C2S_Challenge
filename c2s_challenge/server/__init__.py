from c2s_challenge.common.setting import Setting, SettingProvider

from .abstract import AsyncServerProvider, SyncServerProvider

def make_server(setting: SettingProvider | None = None) -> SyncServerProvider:
  """Factory function to create a Server instance."""
  raise NotImplementedError()

def make_server_async(setting: SettingProvider | None = None) -> AsyncServerProvider:
  """Factory function to create a AsyncServer instance."""
  from .server import AsyncServer

  if setting is None:
    setting = Setting()

  return AsyncServer(setting)