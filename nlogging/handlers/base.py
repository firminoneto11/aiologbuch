from asyncio import Lock, to_thread
from functools import lru_cache
from logging import Handler
from threading import RLock
from typing import TYPE_CHECKING, Optional

from nlogging.filters import Filterer
from nlogging.formatters import BaseFormatter
from nlogging.levels import check_level
from nlogging.settings import RAISE_EXCEPTIONS
from nlogging.utils import is_direct_subclass

if TYPE_CHECKING:
    from logging import LogRecord


@lru_cache(maxsize=1)
def _handler_id_generator():
    i = 1
    while True:
        yield i
        i += 1


class BaseAsyncHandler(Filterer):
    _formatter: Optional[BaseFormatter]

    def __init__(self, level: int | str, formatter: BaseFormatter):
        super().__init__()
        self.level = level
        self.formatter = formatter
        self._lock = Lock()
        self._id = next(_handler_id_generator())

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int | str):
        self._level = check_level(value)

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, value: BaseFormatter):
        if not is_direct_subclass(value=value, base_cls=BaseFormatter):
            raise TypeError("'formatter' must be a subclass of BaseFormatter")
        self._formatter = value

    @property
    def lock(self):
        return self._lock

    @property
    def id(self):
        return self._id

    async def emit(self, record: "LogRecord") -> None:
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    # async def flush(self) -> None:
    #     raise NotImplementedError("flush must be implemented by Handler subclasses")

    async def close(self) -> None:
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


class BaseSyncHandler(Filterer):
    _formatter: Optional[BaseFormatter]

    def __init__(self, level: int | str, formatter: BaseFormatter):
        super().__init__()
        self.level = level
        self.formatter = formatter
        self._lock = RLock()
        self._id = next(_handler_id_generator())

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int | str):
        self._level = check_level(value)

    @property
    def formatter(self):
        return self._formatter

    @formatter.setter
    def formatter(self, value: BaseFormatter):
        if not is_direct_subclass(value=value, base_cls=BaseFormatter):
            raise TypeError("'formatter' must be a subclass of BaseFormatter")
        self._formatter = value

    @property
    def lock(self):
        return self._lock

    @property
    def id(self):
        return self._id

    def emit(self, record: "LogRecord") -> None:
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    def format(self, record: "LogRecord"):
        if not self.formatter:
            raise TypeError("No formatter found")
        return self.formatter.format(record)

    def handle(self, record: "LogRecord"):
        if rv := self.filter(record):
            self.emit(record)
        return rv

    def handle_error(self, record: "LogRecord"):
        if RAISE_EXCEPTIONS:
            Handler.handleError(None, record)

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()
