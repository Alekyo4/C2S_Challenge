class SettingNotFound(Exception):
    """Exception raised when a requested config key is not found."""

    def __init__(self, key: str) -> None:
        super().__init__(f"Config '{key}' not found")
