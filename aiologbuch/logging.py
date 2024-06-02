from typing import TYPE_CHECKING, Literal, overload

# from .filters import ExclusiveFilter
from .filters import Filter

# from .formatters import JsonFormatter, LineFormatter
# from .handlers import AsyncFileHandler, AsyncStreamHandler
from .levels import check_level
from .loggers import AsyncLogger, SyncLogger
from .managers import get_logger_manager

if TYPE_CHECKING:
    from .types import LevelType


async_manager = get_logger_manager(AsyncLogger)
sync_manager = get_logger_manager(SyncLogger)


@overload
def get_logger(
    name: str,
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["async"] = "async",
) -> AsyncLogger:
    ...


@overload
def get_logger(
    name: str,
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["sync"] = "sync",
) -> SyncLogger:
    ...


def get_logger(
    name: str,
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["async", "sync"] = "async",
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
    :param kind: Determines the kind of the logger that will be returned, either a \
        sync or an async logger. The possible values are 'async' and 'sync'. The \
        default value is 'async'.

    :returns: A logger instance.
    """
    level = check_level(level=level)
    manager = async_manager if kind == "async" else sync_manager
    logger, created = manager.get_logger(name=name, filter=Filter(level))

    if created:
        # _setup_logger(logger=logger, filename=filename, exclusive=exclusive)
        ...

    return logger


# def _setup_logger(logger: NLogger, filename: str, exclusive: bool):
#     formatter = JsonFormatter()
#     line_formatter = LineFormatter()  # noqa

#     logger._add_handler(
#         stream_handler := AsyncStreamHandler(
#             filter=Filter(logger.level), formatter=formatter
#         )
#     )

#     if filename:
#         filter_ = (
#             ExclusiveFilter(level=logger.level) if exclusive else Filter(logger.level)
#         )
#         logger._add_handler(
#             AsyncFileHandler(filename=filename, filter=filter_, formatter=formatter)
#         )
#         if exclusive:
#             logger._remove_handler(stream_handler)
