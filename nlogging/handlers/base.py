from functools import lru_cache
from logging import Handler
from typing import TYPE_CHECKING, Optional

from anyio import Lock
from anyio.to_thread import run_sync

from nlogging.filters import Filterer
from nlogging.formatters import BaseFormatter
from nlogging.levels import check_level
from nlogging.settings import RAISE_EXCEPTIONS
from nlogging.utils import is_direct_subclass

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import LevelType


@lru_cache(maxsize=1)
def _handler_id_generator():
    i = 1
    while True:
        yield i
        i += 1


@lru_cache(maxsize=1)
def get_stderr_lock():
    return Lock()


class BaseAsyncHandler(Filterer):
    _formatter: Optional[BaseFormatter]
    terminator = b"\n"

    def __init__(self, level: "LevelType", formatter: BaseFormatter):
        super().__init__()
        self._id = next(_handler_id_generator())
        self.formatter = formatter
        self.level = level

    @property
    def id(self):
        return self._id

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, value: BaseFormatter):
        if not is_direct_subclass(value=value, base_cls=BaseFormatter):
            raise TypeError("'formatter' must be a subclass of BaseFormatter")
        self._formatter = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: "LevelType"):
        self._level = check_level(value)

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: bytes) -> None:
        raise NotImplementedError(
            "'write_and_flush' must be implemented by Handler subclasses"
        )

    async def close(self) -> None:
        raise NotImplementedError("'close' must be implemented by Handler subclasses")

    def format(self, record: "LogRecord"):
        if not self.formatter:
            raise TypeError("No formatter found")
        return self.formatter.format(record)

    async def handle(self, record: "LogRecord"):
        if rv := self.filter(record):
            await self.emit(record)
        return rv

    async def handle_error(self, record: "LogRecord"):
        if RAISE_EXCEPTIONS:
            async with get_stderr_lock():
                await run_sync(Handler.handleError, None, record)
