from functools import lru_cache
from logging import Handler
from typing import TYPE_CHECKING

from anyio import Lock
from anyio.to_thread import run_sync

from nlogging.filters import Filter
from nlogging.levels import check_level
from nlogging.settings import RAISE_EXCEPTIONS

if TYPE_CHECKING:
    from logging import LogRecord
    from typing import Protocol

    from nlogging._types import LevelType

    class FormatterProtocol(Protocol):
        def format(self, record: "LogRecord") -> bytes:
            ...


@lru_cache(maxsize=1)
def _handler_id_generator():
    i = 1
    while True:
        yield i
        i += 1


@lru_cache(maxsize=1)
def get_stderr_lock():
    return Lock()


class BaseAsyncHandler:
    terminator = b"\n"

    def __init__(self, level: "LevelType", formatter: "FormatterProtocol"):
        self._id = next(_handler_id_generator())
        self.formatter = formatter
        self.level = level

    @property
    def id(self):
        return self._id

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: "LevelType"):
        self._level = check_level(value)
        self.filter = Filter(level=self.level)

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
        return self.formatter.format(record)

    async def handle(self, record: "LogRecord"):
        if self.filter.filter(record):
            await self.emit(record)

    async def handle_error(self, record: "LogRecord"):
        if RAISE_EXCEPTIONS:
            async with get_stderr_lock():
                await run_sync(Handler.handleError, None, record)
