from typing import TYPE_CHECKING, Optional

from anyio import create_task_group

from aiologbuch.levels import LogLevel
from aiologbuch.types import AsyncHandlerProtocol

from .base import BaseLogger

if TYPE_CHECKING:
    from aiologbuch.types import LogRecordProtocol, MessageType


class AsyncLogger(BaseLogger[AsyncHandlerProtocol]):
    kind = "async"

    async def debug(self, msg: "MessageType"):
        if self._enabled:
            await self._log(LogLevel.DEBUG, msg)

    async def info(self, msg: "MessageType"):
        if self._enabled:
            await self._log(LogLevel.INFO, msg)

    async def warning(self, msg: "MessageType"):
        if self._enabled:
            await self._log(LogLevel.WARNING, msg)

    async def error(self, msg: "MessageType"):
        if self._enabled:
            await self._log(LogLevel.ERROR, msg)

    async def exception(self, exc: BaseException):
        if self._enabled:
            await self._log(LogLevel.ERROR, str(exc), exc_info=exc)

    async def critical(self, msg: "MessageType"):
        if self._enabled:
            await self._log(LogLevel.CRITICAL, msg)

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
            filename=caller["filename"],
            function_name=caller["function_name"],
            line_number=caller["line_number"],
            exc_info=exc_info,
        )

        await self._handle(record)

    async def _handle(self, record: "LogRecordProtocol"):
        if self._handlers:
            async with create_task_group() as tg:
                [tg.start_soon(handler.handle, record) for handler in self._handlers]
        else:
            raise ValueError("No handlers were set for the logger")

    async def _disable(self):
        if self._enabled:
            [await handler.close() for handler in self._handlers]
            self._handlers = set()
            self._enabled = False
