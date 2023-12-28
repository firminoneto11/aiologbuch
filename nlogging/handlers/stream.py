from asyncio import StreamWriter, get_running_loop
from typing import TYPE_CHECKING, Optional, TextIO

from nlogging.protocols import AIOProtocol

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging.formatters import BaseFormatter

from .base import BaseAsyncHandler


class AsyncStreamHandler(BaseAsyncHandler):
    _writer: Optional[StreamWriter]

    terminator = "\n"

    def __init__(self, stream: TextIO, level: int | str, formatter: "BaseFormatter"):
        super().__init__(level=level, formatter=formatter)
        self._closed = True
        self._writer = None
        self._stream = stream

    @property
    def closed(self):
        return self._closed

    @property
    def writer(self):
        return self._writer

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value: TextIO):
        if not self.closed:
            raise ValueError("Cannot change stream on open handler")

        if value is self.stream:
            return

        self._stream = value

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: str):
        writer = await self._init_writer()
        writer.write(msg.encode())
        await writer.drain()

    async def close(self):
        if (self.writer) and (not self.closed):
            await self.acquire()
            try:
                await self.writer.drain()
                self.writer.close()
                await self.writer.wait_closed()
                self._closed = True
                self._writer = None
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
            self._writer = StreamWriter(
                transport=transport, protocol=protocol, reader=None, loop=loop
            )
            self._closed = False
            return self._writer
        finally:
            self.release()
