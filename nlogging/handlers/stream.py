from asyncio import StreamWriter, get_running_loop
from sys import stderr
from typing import TYPE_CHECKING, Optional

from nlogging.protocols import AIOProtocol

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging._types import LevelType
    from nlogging.formatters import BaseFormatter

from .base import BaseAsyncHandler, BaseSyncHandler


class AsyncStreamHandler(BaseAsyncHandler):
    _writer: Optional[StreamWriter]

    terminator = b"\n"

    def __init__(self, level: "LevelType", formatter: "BaseFormatter"):
        super().__init__(level=level, formatter=formatter)
        self.closed = True
        self._writer = None

    @property
    def writer(self):
        return self._writer

    @writer.setter
    def writer(self, value: Optional[StreamWriter]):
        if self.is_open:
            raise RuntimeError("Cannot change writer on open handler")

        if self.writer is value:
            return

        self._writer = value

    @property
    def is_open(self):
        return bool(self.writer) and (not self.closed)

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: bytes):
        if not self.is_open:
            await self._init_writer()

        if not self.writer:
            # NOTE: This is not likely to happen, but you never know...
            raise RuntimeError("Writer was not initialized")

        async with self.lock:
            self.writer.write(msg)
            await self.writer.drain()

    async def close(self):
        if self.is_open:
            async with self.lock:
                await self.writer.drain()
                self.writer.close()
                self.writer = None
                self.closed = True

    async def _init_writer(self):
        loop = get_running_loop()
        async with self.lock:
            transport, protocol = await loop.connect_write_pipe(AIOProtocol, stderr)
            self.writer = StreamWriter(
                transport=transport, protocol=protocol, reader=None, loop=loop
            )
            self.closed = False


class SyncStreamHandler(BaseSyncHandler):
    terminator = b"\n"

    def __init__(self, level: "LevelType", formatter: "BaseFormatter"):
        super().__init__(level=level, formatter=formatter)

    def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            self.write_and_flush(msg)
        except:  # noqa
            self.handle_error(record)

    def write_and_flush(self, msg: bytes):
        with self.lock:
            stderr.write(msg.decode())
            stderr.flush()
