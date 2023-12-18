import inspect
import sys
import typing

from nlogging.filters import Filterer
from nlogging.formatters import JsonFormatter
from nlogging.handlers import AsyncStreamHandler
from nlogging.levels import LogLevel, check_level, get_level_name
from nlogging.records import LogRecord

from .base import BaseLogger

if typing.TYPE_CHECKING:
    from nlogging.handlers import BaseAsyncHandler


class NLogger(Filterer, BaseLogger):
    if typing.TYPE_CHECKING:
        handlers: list["BaseAsyncHandler"]

    @classmethod
    def create_logger(cls, name: str, level: int):
        logger = cls(name, level)

        stream_handler = AsyncStreamHandler(stream=sys.stderr)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(JsonFormatter())

        logger.addHandler(stream_handler)
        return logger

    def __init__(self, name: str, level: int):
        Filterer.__init__(self)
        self.name = name
        self._level = check_level(level)
        self.handlers = []
        self.disabled = False

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: str | int):
        self._level = check_level(value)

    def setLevel(self, level: str | int):
        self.level = level

    async def debug(self, msg: dict | str):
        if self.isEnabledFor(LogLevel.DEBUG):
            await self._log(LogLevel.DEBUG, msg)

    async def info(self, msg: dict | str):
        if self.isEnabledFor(LogLevel.INFO):
            await self._log(LogLevel.INFO, msg)

    async def warning(self, msg: dict | str):
        if self.isEnabledFor(LogLevel.WARNING):
            await self._log(LogLevel.WARNING, msg)

    async def error(self, msg: dict | str):
        if self.isEnabledFor(LogLevel.ERROR):
            await self._log(LogLevel.ERROR, msg)

    async def exception(self, msg: dict | str):
        if self.isEnabledFor(LogLevel.ERROR):
            await self._log(LogLevel.ERROR, msg, exc_info=True)

    async def critical(self, msg: dict | str):
        if self.isEnabledFor(LogLevel.CRITICAL):
            await self._log(LogLevel.CRITICAL, msg)

    def findCaller(self, stack_info: bool = False, stacklevel: int = 1):
        ...

    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: str | dict,
        args: tuple,
        exc_info: bool,
        func=None,
        extra: dict | None = None,
        sinfo=None,
    ):
        ...

    async def _log(
        self,
        level,
        msg,
        args=None,
        exc_info=None,
        extra: typing.Optional[dict] = None,
    ):
        frame = inspect.stack()[2]
        fn, lno, func, sinfo = frame.filename, frame.lineno, frame.function, None

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        if args is None:
            args = ()

        record = LogRecord(
            self.name,
            level,
            fn,
            lno,
            msg,
            args,
            exc_info,
            func,
            sinfo,
            extra_data=extra,
        )

        await self.handle(record)

    async def handle(self, record: LogRecord):
        if (not self.disabled) and self.filter(record):
            await self.callHandlers(record)

    def addHandler(self, handler: "BaseAsyncHandler"):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def removeHandler(self, handler: "BaseAsyncHandler"):
        if handler in self.handlers:
            self.handlers.remove(handler)

    def hasHandlers(self):
        return len(self.handlers) > 0

    async def callHandlers(self, record: LogRecord):
        if not self.hasHandlers():
            raise ValueError("No handlers found for logger")

        for handler in self.handlers:
            if record.levelno >= handler.level:
                await handler.handle(record)

    def isEnabledFor(self, level: int):
        if self.disabled:
            return False
        return level >= self.level

    def __repr__(self):
        level = get_level_name(self.level)
        return f"<{self.__class__.__name__} {self.name} ({level})>"

    async def disable(self):
        if self.disabled:
            return
        [await handler.close() for handler in self.handlers]
        self.disabled = True
