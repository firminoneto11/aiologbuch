from typing import TYPE_CHECKING

from .filters import ExclusiveFilter, Filter
from .formatters import JsonFormatter, LineFormatter
from .handlers import AsyncFileHandler, AsyncStreamHandler
from .levels import check_level
from .loggers import AsyncLoggerManagerSingleton, NLogger

if TYPE_CHECKING:
    from ._types import LevelType


def get_logger(
    name: str, level: "LevelType" = "INFO", filename: str = "", exclusive: bool = False
):
    """
    This function is used to get a logger instance. If you inform the same name, it
    will always return the same logger.

    The only required field is 'name', which is used to identify the logger. If you
    don't inform a 'filename', the logger will only log to 'sys.stderr'.

    :param name: The name of the logger.
    :param level: The level of the logger. Default is INFO.
    :param filename: The filename to write the logs.
    :param exclusive: If True, the logger will only log the messages that are \
        exclusively for the level chosen. Only works with a 'filename' specified.\
        Default is False.

    :return: A NLogger instance.
    """
    logger, created = _get_logger(name=name, level=level)

    if created:
        _setup_logger(logger=logger, filename=filename, exclusive=exclusive)

    return logger


def _get_logger(name: str, level: "LevelType"):
    level_ = check_level(level)
    manager = AsyncLoggerManagerSingleton[NLogger](logger_class=NLogger)
    return manager.get_logger(name=name, filter=Filter(level_))


def _setup_logger(logger: NLogger, filename: str, exclusive: bool):
    formatter = JsonFormatter()
    line_formatter = LineFormatter()  # noqa

    logger._add_handler(
        AsyncStreamHandler(filter=Filter(logger.level), formatter=formatter)
    )

    if filename:
        logger._add_handler(
            AsyncFileHandler(
                filename=filename,
                filter=(
                    ExclusiveFilter(level=logger.level)
                    if exclusive
                    else Filter(logger.level)
                ),
                formatter=formatter,
            )
        )
