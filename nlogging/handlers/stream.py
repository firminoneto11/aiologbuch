import asyncio
from typing import TYPE_CHECKING, Optional, TextIO

from nlogging.levels import get_level_name
from nlogging.protocols import AIOProtocol

if TYPE_CHECKING:
    from nlogging.records import LogRecord

from .base import BaseNativeAsyncHandler


class NativeAsyncStreamHandler(BaseNativeAsyncHandler):
    if TYPE_CHECKING:
        writer: Optional[asyncio.StreamWriter]

    terminator = "\n"

    def __init__(self, stream: TextIO):
        BaseNativeAsyncHandler.__init__(self)
        self.stream = stream
        self.writer = None

    async def write(self, msg: str):
        if not self.writer:
            self.writer = await self._init_writer()
        self.writer.write(msg.encode())

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write(msg)
            await self.flush()
        except:  # noqa
            await self.handleError(record)

    async def flush(self):
        if self.writer:
            await self.writer.drain()

    async def close(self):
        if self.writer:
            await self.acquire()
            try:
                await self.flush()
                self.writer.close()
                self._closed = True
            finally:
                self.release()

    async def setStream(self, stream: TextIO):
        """
        Sets the StreamHandler's stream to the specified value,
        if it is different.

        Returns the old stream, if the stream was changed, or None
        if it wasn't.

        If the 'write' property is set, raises ValueError, because the
        handler would keep writing to the old stream, which is probably not
        what was intended.
        """
        if stream is self.stream:
            result = None
        else:
            if self.writer:
                raise ValueError("Cannot change stream on open handler")

            result = self.stream

            await self.acquire()
            try:
                await self.flush()
                self.stream = stream
            finally:
                self.release()

        return result

    async def _init_writer(self):
        if self.writer:
            return self.writer

        await self.acquire()
        try:
            loop = asyncio.get_running_loop()
            transport, protocol = await loop.connect_write_pipe(
                AIOProtocol, self.stream
            )
            return asyncio.StreamWriter(
                transport=transport, protocol=protocol, reader=None, loop=loop
            )
        finally:
            self.release()

    def __repr__(self):
        level = get_level_name(self.level)
        if name := str(getattr(self.stream, "name", "")):
            name += " "
        return f"<{self.__class__.__name__} {name}({level})>"
