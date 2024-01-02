from inspect import stack
from logging import LogRecord
from traceback import format_exception
from typing import TYPE_CHECKING, Optional

from anyio import create_task_group

from nlogging.filters import Filterer
from nlogging.formatters import JsonFormatter
from nlogging.handlers import AsyncStreamHandler
from nlogging.levels import LogLevel, check_level

from .base import BaseAsyncLogger

if TYPE_CHECKING:
    from nlogging.handlers import BaseAsyncHandler

    from .base import CallerInfo, LevelType, MessageType


class NLogger(Filterer, BaseAsyncLogger):
    def __init__(self, name: str, level: "LevelType"):
        super().__init__()
        self.name = name
        self._level = check_level(level)
        self._handlers = {}
        self.disabled = False

        self.add_handler(
            AsyncStreamHandler(level=self.level, formatter=JsonFormatter())
        )

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: "LevelType"):
        should_update_handlers = self.level != value
        self._level = check_level(value)

        if should_update_handlers:
            self.update_handlers_level()

    @property
    def handlers(self):
        return self._handlers

    @property
    def mem_addr(self):
        return hex(id(self))

    async def debug(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.DEBUG):
            await self._log(LogLevel.DEBUG, msg)

    async def info(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.INFO):
            await self._log(LogLevel.INFO, msg)

    async def warning(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.WARNING):
            await self._log(LogLevel.WARNING, msg)

    async def error(self, msg: "MessageType", exc: Optional[BaseException] = None):
        if self.is_enabled_for(LogLevel.ERROR):
            await self._log(LogLevel.ERROR, msg, exc_info=exc)

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
        level: int,
        msg: "MessageType",
        filename: str,
        function_name: str,
        line_number: int,
        exc_info: Optional[BaseException] = None,
    ):
        if exc_info:
            info = (type(exc_info), exc_info, exc_info.__traceback__)
            text = "".join(format_exception(exc_info, limit=None, chain=True))
        else:
            info, text = None, None

        record = LogRecord(
            name, level, filename, line_number, msg, None, info, function_name
        )

        if text:
            record.exc_text = text

        return record

    async def _log(
        self,
        level: int,
        msg: "MessageType",
        exc_info: Optional[BaseException] = None,
    ):
        caller = self.find_caller()

        record = self.make_record(
            name=self.name,
            level=level,
            msg=msg,
            filename=caller["caller_filename"],
            function_name=caller["caller_function_name"],
            line_number=caller["caller_line_number"],
            exc_info=exc_info,
        )

        await self.handle(record)

    async def handle(self, record: LogRecord):
        if (not self.disabled) and self.filter(record):
            await self.call_handlers(record)

    def add_handler(self, handler: "BaseAsyncHandler"):
        if handler.id not in self.handlers:
            self.handlers[handler.id] = handler

    def remove_handler(self, handler: "BaseAsyncHandler"):
        self.handlers.pop(handler.id, None)

    def has_handlers(self):
        return len(self.handlers.keys()) > 0

    async def call_handlers(self, record: LogRecord):
        if not self.has_handlers():
            raise ValueError("No handlers found for the logger")

        async with create_task_group() as tg:
            for handler in self.handlers.values():
                if record.levelno >= handler.level:
                    tg.start_soon(handler.handle, record)

    def is_enabled_for(self, level: int):
        if self.disabled:
            return False
        return level >= self.level

    def update_handlers_level(self):
        for handler in self.handlers.values():
            handler.level = self.level

    async def disable(self):
        if self.disabled:
            return
        [await handler.close() for handler in self.handlers.values()]
        self._handlers = {}
        self.disabled = True
