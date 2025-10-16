class SettingNotFound(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Config '{key}' not found")
