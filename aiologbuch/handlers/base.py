from logging import Handler
from typing import TYPE_CHECKING

from anyio.to_thread import run_sync

from aiologbuch.shared.conf import RAISE_EXCEPTIONS

from .stderr.lock import async_stderr_lock, sync_stderr_lock

if TYPE_CHECKING:
    from aiologbuch.shared.types import FormatterProtocol, LogRecordProtocol


class BaseHandler:
    terminator = b"\n"

    def __init__(self, formatter: "FormatterProtocol"):
        self.formatter = formatter

    def format(self, record: "LogRecordProtocol"):
        return self.formatter.format(record)


class BaseAsyncHandler(BaseHandler):
    async def handle(self, record: "LogRecordProtocol"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def handle_error(self, record: "LogRecordProtocol"):
        if RAISE_EXCEPTIONS:
            async with async_stderr_lock():
                await run_sync(Handler.handleError, None, record)


class BaseSyncHandler(BaseHandler):
    def handle(self, record: "LogRecordProtocol"):
        try:
            msg = self.format(record) + self.terminator
            self.write_and_flush(msg)
        except:  # noqa
            self.handle_error(record)

    def handle_error(self, record: "LogRecordProtocol"):
        if RAISE_EXCEPTIONS:
            with sync_stderr_lock():
                Handler.handleError(None, record)
