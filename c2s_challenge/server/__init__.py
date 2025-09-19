from c2s_challenge.config import Config, ConfigProvider

from .abstract import ServerProvider

def make_server(config: ConfigProvider | None = None) -> ServerProvider:
  """Factory function to create a Server instance."""
  from .server import Server

  if config is None:
    config = Config()

  return Server(config)