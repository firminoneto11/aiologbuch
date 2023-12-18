import asyncio
from abc import abstractmethod
from logging import Handler
from typing import TYPE_CHECKING

from nlogging.filters import Filterer
from nlogging.formatters import Formatter
from nlogging.levels import LogLevel, check_level, get_level_name
from nlogging.settings import raise_exceptions

if TYPE_CHECKING:
    from nlogging.records import LogRecord


class BaseAsyncHandler(Filterer):
    def __init__(self):
        Filterer.__init__(self)
        self._level = LogLevel.NOTSET
        self._closed = False
        self.createLock()

    @property
    def level(self):
        return self._level

    def setLevel(self, level: str | int):
        self._level = check_level(level)

    @abstractmethod
    async def emit(self, record: "LogRecord"):
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    @abstractmethod
    async def flush(self):
        raise NotImplementedError("flush must be implemented by Handler subclasses")

    @abstractmethod
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

    async def handleError(self, record: "LogRecord"):
        if raise_exceptions:
            await asyncio.to_thread(Handler.handleError, None, record)

    def setFormatter(self, formatter: Formatter):
        if formatter.__class__ is Formatter:
            raise TypeError("formatter must be an instance of a Formatter subclass")
        self.formatter = formatter

    def createLock(self):
        self.lock = asyncio.Lock()

    async def acquire(self):
        if self.lock:
            await self.lock.acquire()

    def release(self):
        if self.lock:
            self.lock.release()

    def __repr__(self):
        return f"<{self.__class__.__name__} ({get_level_name(self.level)})>"

    def _at_fork_reinit(self):
        pass
