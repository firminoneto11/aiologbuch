from asyncio import StreamWriter, get_running_loop
from typing import TYPE_CHECKING, Optional, TextIO

from nlogging.protocols import AIOProtocol

if TYPE_CHECKING:
    from nlogging.records import LogRecord

from .base import BaseAsyncHandler


class AsyncStreamHandler(BaseAsyncHandler):
    _writer: Optional[StreamWriter]

    terminator = "\n"

    def __init__(self, stream: TextIO):
        BaseAsyncHandler.__init__(self)
        self._writer = None
        self._closed = False
        self._stream = stream

    @property
    def writer(self):
        return self._writer

    @property
    def closed(self):
        return self._closed

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value: TextIO):
        if value is self.stream:
            return

        if (self.writer) and (not self.closed):
            raise ValueError("Cannot change stream on open handler")

        self._writer = None
        self._stream = value

    async def flush(self):
        if self.writer:
            await self.writer.drain()

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: str):
        if (not self.writer) or (self.closed):
            self.writer = await self._init_writer()
        self.writer.write(msg.encode())
        await self.flush()

    async def close(self):
        if (self.writer) and (not self.closed):
            await self.acquire()
            try:
                await self.flush()
                self.writer.close()
                await self.writer.wait_closed()
                self._closed = True
            finally:
                self.release()

    async def _init_writer(self):
        if (self.writer) and (not self.closed):
            return self.writer

        loop = get_running_loop()

        await self.acquire()
        try:
            transport, protocol = await loop.connect_write_pipe(
                AIOProtocol, self.stream
            )
            return StreamWriter(
                transport=transport, protocol=protocol, reader=None, loop=loop
            )
        finally:
            self.release()
