from inspect import stack
from sys import exc_info as get_exc_info
from sys import stderr
from typing import TYPE_CHECKING, Optional

from nlogging.filters import Filterer
from nlogging.formatters import JsonFormatter
from nlogging.handlers import AsyncStreamHandler
from nlogging.levels import LogLevel, check_level
from nlogging.records import LogRecord

from .base import BaseLogger

if TYPE_CHECKING:
    from nlogging.handlers import BaseAsyncHandler

    from .base import CallerInfo, MessageType


class NLogger(Filterer, BaseLogger):
    handlers: list["BaseAsyncHandler"]

    @classmethod
    def create_logger(cls, name: str, level: int | str):
        stream_handler = AsyncStreamHandler(stream=stderr)
        stream_handler.level = level
        stream_handler.formatter = JsonFormatter()

        logger = cls(name, level)
        logger.add_handler(stream_handler)

        return logger

    def __init__(self, name: str, level: int | str):
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

    async def debug(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.DEBUG):
            await self._log(LogLevel.DEBUG, msg)

    async def info(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.INFO):
            await self._log(LogLevel.INFO, msg)

    async def warning(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.WARNING):
            await self._log(LogLevel.WARNING, msg)

    async def error(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.ERROR):
            await self._log(LogLevel.ERROR, msg)

    async def exception(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.ERROR):
            await self._log(LogLevel.ERROR, msg, exc_info=True)

    async def critical(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.CRITICAL):
            await self._log(LogLevel.CRITICAL, msg)

    def find_caller(self) -> "CallerInfo":
        frame = stack()[3]  # Up 3 frames from this one is the original caller
        return {
            "caller_filename": frame.filename,
            "caller_function_name": frame.function,
            "caller_line_number": frame.lineno,
        }

    def make_record(
        self,
        name: str,
        msg: "MessageType",
        level: int,
        filename: str,
        function_name: str,
        line_number: int,
        exc_info,
        extra: Optional[dict] = None,
    ):
        return LogRecord(
            name=name,
            msg=msg,
            level=level,
            pathname=filename,
            func=function_name,
            lno=line_number,
            exc_info=exc_info,
            extra=extra,
            args=tuple(),
        )

    async def _log(
        self,
        level: int,
        msg: "MessageType",
        exc_info: bool = False,
        extra: Optional[dict] = None,
    ):
        caller = self.find_caller()

        record = self.make_record(
            name=self.name,
            msg=msg,
            level=level,
            filename=caller["caller_filename"],
            function_name=caller["caller_function_name"],
            line_number=caller["caller_line_number"],
            exc_info=get_exc_info() if exc_info else None,
            extra=extra,
        )

        await self.handle(record)

    async def handle(self, record: LogRecord):
        if (not self.disabled) and self.filter(record):
            await self.call_handlers(record)

    def add_handler(self, handler: "BaseAsyncHandler"):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def remove_handler(self, handler: "BaseAsyncHandler"):
        if handler in self.handlers:
            self.handlers.remove(handler)

    def has_handlers(self):
        return len(self.handlers) > 0

    async def call_handlers(self, record: LogRecord):
        if not self.has_handlers():
            raise ValueError("No handlers found for logger")

        for handler in self.handlers:
            if record.levelno >= handler.level:
                await handler.handle(record)

    def is_enabled_for(self, level: int):
        if self.disabled:
            return False
        return level >= self.level

    async def disable(self):
        if self.disabled:
            return
        [await handler.close() for handler in self.handlers]
        self.disabled = True
