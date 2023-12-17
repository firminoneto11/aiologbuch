import asyncio
from abc import abstractmethod
from logging import Handler
from typing import TYPE_CHECKING, Optional

from nlogging.filters import Filterer
from nlogging.formatters import Formatter
from nlogging.levels import LogLevel, check_level, get_level_name
from nlogging.settings import raise_exceptions

if TYPE_CHECKING:
    from nlogging.records import LogRecord

# _lock = asyncio.Lock()
# _handlers = weakref.WeakValueDictionary()
# _handlerList = []


# async def _acquireLock():
#     if _lock:
#         await _lock.acquire()


# def _releaseLock():
#     if _lock:
#         _lock.release()


# def _addHandlerRef(handler: "BaseNativeAsyncHandler"):
#     _acquireLock()
#     try:
#         _handlerList.append(weakref.ref(handler, _removeHandlerRef))
#     finally:
#         _releaseLock()


# def _removeHandlerRef(wr: weakref.ReferenceType):
#     acquire, release, handlers = _acquireLock, _releaseLock, _handlerList
#     if acquire and release and handlers:
#         acquire()
#         try:
#             handlers.remove(wr)
#         except ValueError:
#             pass
#         finally:
#             release()


class BaseNativeAsyncHandler(Filterer):
    def __init__(
        self, level: int = LogLevel.NOTSET, formatter: Optional[type[Formatter]] = None
    ):
        Filterer.__init__(self)
        # self._name = None
        self._level = check_level(level)
        self._closed = False

        if isinstance(formatter, Formatter):
            raise TypeError("formatter must be an instance of Formatter subclass")

        self.formatter = formatter

        # _addHandlerRef(self)

        self.createLock()

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: int | str):
        self._level = check_level(value)

    # @property
    # def name(self):
    #     return self._name

    # @name.setter
    # def name(self, value: str):
    #     _acquireLock()
    #     try:
    #         if self._name in _handlers:
    #             del _handlers[self._name]
    #         self._name = value
    #         if value:
    #             _handlers[value] = self
    #     finally:
    #         _releaseLock()

    # async def close(self):
    #     await _acquireLock()
    #     try:
    #         self._closed = True
    #         if self._name and self._name in _handlers:
    #             del _handlers[self._name]
    #     finally:
    #         _releaseLock()

    @abstractmethod
    async def emit(self, record: LogRecord):
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    @abstractmethod
    async def flush(self):
        raise NotImplementedError("flush must be implemented by Handler subclasses")

    @abstractmethod
    async def close(self):
        raise NotImplementedError("close must be implemented by Handler subclasses")

    def format(self, record: LogRecord):
        if not self.formatter:
            raise TypeError("No formatter found")
        return self.formatter.format(record)

    async def handle(self, record: LogRecord):
        if rv := self.filter(record):
            await self.emit(record)
        return rv

    async def handleError(self, record: LogRecord):
        if raise_exceptions:
            await asyncio.to_thread(Handler.handleError, None, record)

    def setFormatter(self, formatter: Formatter):
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
