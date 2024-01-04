from typing import TYPE_CHECKING

from .filters import Filter
from .formatters import JsonFormatter
from .handlers import AsyncFileHandler, AsyncStreamHandler
from .loggers import AsyncLoggerManagerSingleton, NLogger

if TYPE_CHECKING:
    from ._types import LevelType


def get_logger(name: str, level: "LevelType" = "INFO", filename: str = ""):
    """
    This function is used to get a logger instance. If you inform the same name, it
    will always return the same logger.

    :param name: The name of the logger.
    :param level: The level of the logger. Default is INFO.
    :param filename: The filename to write the logs.

    :return: A NLogger instance.
    """
    manager = AsyncLoggerManagerSingleton[NLogger](logger_class=NLogger)
    logger, created = manager.get_logger(name=name, level=level, filter_class=Filter)

    if created:
        logger._add_handler(handler_class=AsyncStreamHandler, formatter=JsonFormatter())

        if filename:
            logger._add_handler(
                handler_class=AsyncFileHandler,
                formatter=JsonFormatter(),
                filename=filename,
            )

    return logger
