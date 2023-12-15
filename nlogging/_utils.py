"""
def _get_logger(name: str) -> Logger:
    if not exists(settings.LOGS_DIR):
        makedirs(settings.LOGS_DIR)

    # Creating the file handlers for the logger
    handlers = [
        Handler(
            file_handler=python_logging.FileHandler(
                filename=settings.LOGS_DIR / f"{name}.log"
            ),
            level=python_logging.DEBUG,
        ),
    ]

    # Creating a logger with a custom name and the file handler and returning it
    return Logger(name=name, handlers=handlers)


@lru_cache(maxsize=50)
def get_logger(name: str) -> Logger:
    return _get_logger(name=name)
"""
