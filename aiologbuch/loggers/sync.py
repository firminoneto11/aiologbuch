from typing import TYPE_CHECKING, Optional

from aiologbuch.shared.enums import IOModeEnum
from aiologbuch.shared.levels import LogLevel
from aiologbuch.shared.types import SyncHandlerProtocol

from .base import BaseLogger

if TYPE_CHECKING:
    from aiologbuch.shared.types import LogRecordProtocol, MessageType


class SyncLogger(BaseLogger[SyncHandlerProtocol]):
    mode = IOModeEnum.SYNC

    def debug(self, msg: "MessageType"):
        if self._filter(level=LogLevel.DEBUG) and self._enabled:
            self._log(LogLevel.DEBUG, msg)

    def info(self, msg: "MessageType"):
        if self._filter(level=LogLevel.INFO) and self._enabled:
            self._log(LogLevel.INFO, msg)

    def warning(self, msg: "MessageType"):
        if self._filter(level=LogLevel.WARNING) and self._enabled:
            self._log(LogLevel.WARNING, msg)

    def error(self, msg: "MessageType"):
        if self._filter(level=LogLevel.ERROR) and self._enabled:
            self._log(LogLevel.ERROR, msg)

    def exception(self, exc: BaseException, msg: Optional["MessageType"] = None):
        if self._filter(level=LogLevel.ERROR) and self._enabled:
            message = msg if msg else str(exc)
            self._log(LogLevel.ERROR, message, exc_info=exc)

    def critical(self, msg: "MessageType"):
        if self._filter(level=LogLevel.CRITICAL) and self._enabled:
            self._log(LogLevel.CRITICAL, msg)

    def _log(
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
            filename=caller.filename,
            function_name=caller.function_name,
            line_number=caller.line_number,
            exc_info=exc_info,
        )

        self._handle(record)

    def _handle(self, record: "LogRecordProtocol"):
        [handler.handle(record) for handler in self._handlers]

    def _disable(self):
        if self._enabled:
            [handler.close() for handler in self._handlers]
            self._handlers = set()
            self._enabled = False
