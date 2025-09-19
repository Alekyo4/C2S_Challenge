from c2s_challenge.config import ConfigProvider

from .abstract import ServerProvider

class Server(ServerProvider):
  def __init__(self, config: ConfigProvider):
    pass

  def listen(self) -> None:
    print("Server started...") 