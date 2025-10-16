class ServerWithoutContext(Exception):
    def __init__(self):
        super().__init__("Server not started. Use 'async with Server(...) as sv:'")
