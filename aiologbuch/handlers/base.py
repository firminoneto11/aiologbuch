from logging import Handler
from typing import TYPE_CHECKING

from anyio.to_thread import run_sync

from aiologbuch.shared.conf import GLOBAL_STDERR_LOCK, RAISE_EXCEPTIONS
from aiologbuch.shared.utils import sync_lock_context

if TYPE_CHECKING:
    from aiologbuch.shared.types import FormatterProtocol, LogRecordProtocol


class BaseHandler:
    def __init__(self, formatter: "FormatterProtocol"):
        self.formatter = formatter

    def format(self, record: "LogRecordProtocol"):
        return self.formatter.format(record)


class BaseAsyncHandler(BaseHandler):
    async def handle(self, record: "LogRecordProtocol"):
        try:
            msg = self.format(record)
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def handle_error(self, record: "LogRecordProtocol"):
        if RAISE_EXCEPTIONS:
            async with GLOBAL_STDERR_LOCK:
                await run_sync(Handler.handleError, None, record)


class BaseSyncHandler(BaseHandler):
    def handle(self, record: "LogRecordProtocol"):
        try:
            msg = self.format(record)
            self.write_and_flush(msg)
        except:  # noqa
            self.handle_error(record)

    def handle_error(self, record: "LogRecordProtocol"):
        if RAISE_EXCEPTIONS:
            with sync_lock_context(lock=GLOBAL_STDERR_LOCK):
                Handler.handleError(None, record)
