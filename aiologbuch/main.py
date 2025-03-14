from inspect import currentframe, getmodule
from typing import TYPE_CHECKING, Literal, cast, overload

from .formatters import JsonFormatter, LineFormatter
from .handlers import (  # noqa
    AsyncFileHandler,
    AsyncStderrHandler,
    SyncFileHandler,
    SyncStderrHandler,
)
from .loggers import AsyncLogger, SyncLogger
from .managers import get_logger_manager
from .shared.conf import settings
from .shared.enums import IOModeEnum
from .shared.filters import Filter
from .shared.levels import check_level
from .shared.types import BaseLoggerProtocol

if TYPE_CHECKING:
    from .shared.types import LevelType


# TODO: Make sure that users can globally configure:
# - kind
# - formatter


async_manager = get_logger_manager(
    mode=IOModeEnum.ASYNC, logger_class=cast(BaseLoggerProtocol, AsyncLogger)
)
sync_manager = get_logger_manager(
    mode=IOModeEnum.SYNC, logger_class=cast(BaseLoggerProtocol, SyncLogger)
)


@overload
def get_logger(
    name: str = "",
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["async"] = "async",
) -> AsyncLogger: ...


@overload
def get_logger(
    name: str = "",
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["sync"] = "sync",
) -> SyncLogger: ...


def get_logger(
    name: str = "",
    level: "LevelType" = "INFO",
    filename: str = "",
    exclusive: bool = False,
    kind: Literal["async", "sync"] = "async",
):
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

    if created:
        if kind == "async":
            _setup_async_logger(logger=logger)
        else:
            _setup_sync_logger(logger=logger)

    if not settings.is_configured:
        settings.configure()

    return logger


def _setup_async_logger(logger: BaseLoggerProtocol):
    stderr_handler1 = AsyncStderrHandler(formatter=JsonFormatter())
    stderr_handler2 = AsyncStderrHandler(formatter=LineFormatter())
    logger._add_handler(stderr_handler1)
    logger._add_handler(stderr_handler2)


def _setup_sync_logger(logger: BaseLoggerProtocol):
    stderr_handler = SyncStderrHandler(formatter=JsonFormatter())
    # stderr_handler = SyncStderrHandler(formatter=LineFormatter())
    logger._add_handler(stderr_handler)
