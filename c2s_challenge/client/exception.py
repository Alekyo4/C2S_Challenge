class ClientWithoutContext(Exception):
  """Exception raised when the client run without context manager"""
  def __init__(self):
    super().__init__("Client not started. Use 'async with Client(...) as cl:'")