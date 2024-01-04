from ._types import LevelType
from .formatters import JsonFormatter
from .handlers import AsyncFileHandler, AsyncStreamHandler
from .loggers import AsyncLoggerManagerSingleton, NLogger
from .shared import ROOT_LOGGER_NAME


def get_logger(
    name: str = ROOT_LOGGER_NAME,
    level: LevelType = "INFO",
    filename: str = "",
):
    """
    This function is used to get a logger instance. If you inform the same name, it
    will always return the same logger.

    :param name: The name of the logger. Default is nlogger, which is the root logger.
    :param level: The level of the logger. Default is INFO.
    :param filename: The filename to write the logs.

    :return: A NLogger instance.
    """
    manager = AsyncLoggerManagerSingleton[NLogger](logger_class=NLogger)
    logger, created = manager.get_logger(name=name, level=level)

    if created:
        formatter = JsonFormatter()
        logger._add_handler(AsyncStreamHandler(level=level, formatter=formatter))

        if filename:
            logger._add_handler(
                AsyncFileHandler(filename=filename, level=level, formatter=formatter)
            )

    return logger
