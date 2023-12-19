from asyncio import Lock, to_thread
from logging import Handler
from typing import TYPE_CHECKING, Optional

from nlogging.filters import Filterer
from nlogging.formatters import BaseFormatter
from nlogging.levels import LogLevel, check_level
from nlogging.settings import RAISE_EXCEPTIONS
from nlogging.utils import is_direct_subclass

if TYPE_CHECKING:
    from nlogging.records import LogRecord


class BaseAsyncHandler(Filterer):
    _formatter: Optional[BaseFormatter]

    def __init__(self):
        Filterer.__init__(self)
        self._level = LogLevel.NOTSET
        self._formatter = None
        self._lock = Lock()

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: str | int):
        self._level = check_level(value)

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, value: BaseFormatter):
        if not is_direct_subclass(cls_or_instance=value, base_cls=BaseFormatter):
            raise TypeError("'formatter' must be a subclass of BaseFormatter")
        self._formatter = value

    @property
    def lock(self):
        return self._lock

    async def emit(self, record: "LogRecord"):
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    async def flush(self):
        raise NotImplementedError("flush must be implemented by Handler subclasses")

    async def close(self):
        raise NotImplementedError("close must be implemented by Handler subclasses")

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
            await to_thread(Handler.handleError, None, record)

    async def acquire(self):
        await self.lock.acquire()

    def release(self):
        self.lock.release()
