from inspect import stack
from logging import LogRecord
from sys import exc_info as get_exc_info
from typing import TYPE_CHECKING, Optional

from nlogging.filters import Filterer
from nlogging.formatters import JsonFormatter
from nlogging.handlers import SyncStreamHandler
from nlogging.levels import LogLevel, check_level

from .base import BaseSyncLogger

if TYPE_CHECKING:
    from _typeshed import OptExcInfo

    from nlogging.handlers import BaseSyncHandler

    from .base import CallerInfo, LevelType, MessageType


class SyncNLogger(Filterer, BaseSyncLogger):
    @classmethod
    def create_logger(cls, name: str, level: "LevelType"):
        logger = cls(name, level)
        logger.add_handler(SyncStreamHandler(level=level, formatter=JsonFormatter()))
        return logger

    def __init__(self, name: str, level: "LevelType"):
        super().__init__()
        self.name = name
        self._level = check_level(level)
        self._handlers = {}
        self.disabled = False

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

    def debug(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.DEBUG):
            self._log(LogLevel.DEBUG, msg)

    def info(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.INFO):
            self._log(LogLevel.INFO, msg)

    def warning(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.WARNING):
            self._log(LogLevel.WARNING, msg)

    def error(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.ERROR):
            self._log(LogLevel.ERROR, msg)

    def exception(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.ERROR):
            self._log(LogLevel.ERROR, msg, exc_info=True)

    def critical(self, msg: "MessageType"):
        if self.is_enabled_for(LogLevel.CRITICAL):
            self._log(LogLevel.CRITICAL, msg)

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
        exc_info: Optional["OptExcInfo"],
    ):
        return LogRecord(
            name, level, filename, line_number, msg, None, exc_info, function_name
        )

    def _log(
        self,
        level: int,
        msg: "MessageType",
        exc_info: bool = False,
    ):
        caller = self.find_caller()

        record = self.make_record(
            name=self.name,
            level=level,
            msg=msg,
            filename=caller["caller_filename"],
            function_name=caller["caller_function_name"],
            line_number=caller["caller_line_number"],
            exc_info=get_exc_info() if exc_info else None,
        )

        self.handle(record)

    def handle(self, record: LogRecord):
        if (not self.disabled) and self.filter(record):
            self.call_handlers(record)

    def add_handler(self, handler: "BaseSyncHandler"):
        if handler.id not in self.handlers:
            self.handlers[handler.id] = handler

    def remove_handler(self, handler: "BaseSyncHandler"):
        self.handlers.pop(handler.id, None)

    def has_handlers(self):
        return len(self.handlers.keys()) > 0

    def call_handlers(self, record: LogRecord):
        if not self.has_handlers():
            raise ValueError("No handlers found for the logger")

        for handler in self.handlers.values():
            if record.levelno >= handler.level:
                handler.handle(record)

    def is_enabled_for(self, level: int):
        if self.disabled:
            return False
        return level >= self.level

    def update_handlers_level(self):
        for handler in self.handlers.values():
            handler.level = self.level

    def disable(self):
        if self.disabled:
            return
        [handler.close() for handler in self.handlers.values()]
        self.disabled = True
