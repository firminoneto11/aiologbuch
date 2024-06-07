from logging import Handler
from typing import TYPE_CHECKING

from anyio.to_thread import run_sync

from aiologbuch.shared import RAISE_EXCEPTIONS, STDERR_LOCK
from aiologbuch.vendor.asyncer import syncify

if TYPE_CHECKING:
    from aiologbuch.types import FormatterProtocol, LogRecordProtocol


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
            async with STDERR_LOCK:
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
            syncify(STDERR_LOCK.acquire)()
            try:
                Handler.handleError(None, record)
            finally:
                syncify(STDERR_LOCK.release)()
