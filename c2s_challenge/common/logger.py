from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger


def get_logger(name: str) -> Logger:
    if not name.isascii():
        raise TypeError(f"The name '{name}' is not accepted for logger prefix")

    logger: Logger = getLogger(name)

    logger.setLevel(DEBUG)

    if logger.hasHandlers():
        return logger

    handler: StreamHandler = StreamHandler()

    handler.setLevel(DEBUG)

    formatter: Formatter = Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
