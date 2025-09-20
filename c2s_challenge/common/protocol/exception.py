class ProtocolRequestInvalid(Exception):
  """Exception raised when the request sent for protocol is invalid"""
  def __init__(self):
    super().__init__("The structure of the request sent to the server is invalid")

class ProtocolNotFoundEvent(Exception):
  """Exception raised when the event not found"""
  def __init__(self):
    super().__init__("The sent event is not mapped as valid on the server")