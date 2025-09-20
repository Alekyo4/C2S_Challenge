class ServerWithoutContext(Exception):
  """Exception raised when the server run without context manager"""
  def __init__(self):
    super().__init__("Server not started. Use 'async with Server(...) as sv:'")