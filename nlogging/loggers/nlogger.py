from inspect import stack
from logging import LogRecord
from traceback import format_exception
from typing import TYPE_CHECKING, Optional

from anyio import create_task_group

from nlogging.filters import Filter
from nlogging.levels import LogLevel, check_level
from nlogging.loggers.base import BaseAsyncLogger

if TYPE_CHECKING:
    from nlogging._types import AsyncHandlerProtocol, CallerInfo, LevelType, MessageType


class NLogger(BaseAsyncLogger):
    _handlers: dict[int, "AsyncHandlerProtocol"]

    def __init__(self, name: str, level: "LevelType"):
        self.name = name
        self.level = level
        self._handlers = {}
        self._disabled = False

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value: "LevelType"):
        should_update_handlers = False
        if getattr(self, "_level", None) is not None:
            should_update_handlers = value != self._level

        self._level = check_level(value)

        if should_update_handlers:
            for handler in self._handlers.values():
                handler.filter = Filter(level=self.level)

    @property
    def _mem_addr(self):
        return hex(id(self))

    async def debug(self, msg: "MessageType"):
        if self._is_enabled_for(LogLevel.DEBUG):
            await self._log(LogLevel.DEBUG, msg)

    async def info(self, msg: "MessageType"):
        if self._is_enabled_for(LogLevel.INFO):
            await self._log(LogLevel.INFO, msg)

    async def warning(self, msg: "MessageType"):
        if self._is_enabled_for(LogLevel.WARNING):
            await self._log(LogLevel.WARNING, msg)

    async def error(self, msg: "MessageType", exc: Optional[BaseException] = None):
        if self._is_enabled_for(LogLevel.ERROR):
            await self._log(LogLevel.ERROR, msg, exc_info=exc)

    async def critical(self, msg: "MessageType"):
        if self._is_enabled_for(LogLevel.CRITICAL):
            await self._log(LogLevel.CRITICAL, msg)

    def _find_caller(self) -> "CallerInfo":
        frame = stack()[3]  # 3 frames up from this one is the original caller
        return {
            "caller_filename": frame.filename,
            "caller_function_name": frame.function,
            "caller_line_number": frame.lineno,
        }

    def _make_record(
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
        caller = self._find_caller()

        record = self._make_record(
            name=self.name,
            level=level,
            msg=msg,
            filename=caller["caller_filename"],
            function_name=caller["caller_function_name"],
            line_number=caller["caller_line_number"],
            exc_info=exc_info,
        )

        await self._handle(record)

    async def _handle(self, record: LogRecord):
        await self._call_handlers(record)

    def _add_handler(self, handler: "AsyncHandlerProtocol"):
        if handler.id not in self._handlers:
            self._handlers[handler.id] = handler

    def _remove_handler(self, handler: "AsyncHandlerProtocol"):
        self._handlers.pop(handler.id, None)

    def _has_handlers(self):
        return len(self._handlers.keys()) > 0

    async def _call_handlers(self, record: LogRecord):
        if not self._has_handlers():
            raise ValueError("No handlers found for the logger")

        async with create_task_group() as tg:
            for handler in self._handlers.values():
                tg.start_soon(handler.handle, record)

    def _is_enabled_for(self, level: int):
        if self._disabled:
            return False
        return level >= self.level

    async def _disable(self):
        if self._disabled:
            return
        [await handler.close() for handler in self._handlers.values()]
        self._handlers = {}
        self._disabled = True
