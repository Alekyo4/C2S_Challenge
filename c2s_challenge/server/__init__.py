from c2s_challenge.common.config import Config, ConfigProvider

from .abstract import AsyncServerProvider, SyncServerProvider

def make_server(config: ConfigProvider | None = None) -> SyncServerProvider:
  """Factory function to create a Server instance."""
  raise NotImplementedError()

def make_server_async(config: ConfigProvider | None = None) -> AsyncServerProvider:
  """Factory function to create a AsyncServer instance."""
  from .server import AsyncServer

  if config is None:
    config = Config()

  return AsyncServer(config)