from functools import lru_cache
from logging import Handler
from typing import TYPE_CHECKING

from anyio.to_thread import run_sync

from aiologbuch.shared import RAISE_EXCEPTIONS, STDERR_LOCK
from aiologbuch.vendor.asyncer import syncify

if TYPE_CHECKING:
    from aiologbuch.types import FilterProtocol, FormatterProtocol, LogRecordProtocol


@lru_cache(maxsize=1)
def _handler_id_generator():
    i = 1
    while True:
        yield i
        i += 1


class BaseHandler:
    terminator = b"\n"

    def __init__(self, filter: "FilterProtocol", formatter: "FormatterProtocol"):
        self._id = next(_handler_id_generator())
        self.formatter = formatter
        self.filter = filter

    @property
    def id(self):
        return self._id

    def format(self, record: "LogRecordProtocol"):
        return self.formatter.format(record)


class BaseAsyncHandler(BaseHandler):
    async def handle(self, record: "LogRecordProtocol"):
        if self.filter.filter(record):
            await self.emit(record)

    async def emit(self, record: "LogRecordProtocol"):
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
        if self.filter.filter(record):
            self.emit(record)

    def emit(self, record: "LogRecordProtocol"):
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
