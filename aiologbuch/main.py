from inspect import currentframe, getmodule
from typing import TYPE_CHECKING, Literal, overload

from .filters import Filter
from .formatters import JsonFormatter
from .handlers import AsyncStderrHandler
from .loggers import AsyncLogger, SyncLogger
from .managers import get_logger_manager
from .shared.levels import check_level

if TYPE_CHECKING:
    from .shared.types import LevelType


# TODO: Make sure that users can globally configure:
# - kind
# - formatter


async_manager = get_logger_manager(AsyncLogger)
sync_manager = get_logger_manager(SyncLogger)


@overload
def get_logger(
    name: str = "",
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["async"] = "async",
) -> AsyncLogger:
    ...


@overload
def get_logger(
    name: str = "",
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["sync"] = "sync",
) -> SyncLogger:
    ...


def get_logger(
    name: str = "",
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["async", "sync"] = "async",
):
    """
    This function is used to get a logger instance. If you inform the same name, it
    will always return the same logger.

    If you don't inform a 'filename', the logger will only log to 'sys.stderr'.

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
    if not name:
        try:
            if (frame := currentframe().f_back) is None:
                raise ValueError()
        except (AttributeError, ValueError) as exc:
            raise RuntimeError("Could not find the caller's frame") from exc

        if (module := getmodule(frame)) is None:
            raise RuntimeError("Could not find the caller's module")

        name = module.__name__

    filter_ = Filter(level=check_level(level=level))
    manager = async_manager if kind == "async" else sync_manager
    logger, created = manager.get_logger(name=name, filter_=filter_)

    if created and kind == "async":
        _setup_async_logger(logger=logger)

    return logger


def _setup_async_logger(logger: AsyncLogger):
    stderr_handler = AsyncStderrHandler(formatter=JsonFormatter())
    logger._add_handler(stderr_handler)
