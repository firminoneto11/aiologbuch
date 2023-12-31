from typing import TYPE_CHECKING

from anyio.streams.file import FileWriteStream

from .base import BaseAsyncHandler

if TYPE_CHECKING:
    from logging import LogRecord

    from nlogging.formatters import BaseFormatter


class AsyncFileHandler(BaseAsyncHandler):
    terminator = "\n"

    def __init__(self, filename: str, level: int | str, formatter: "BaseFormatter"):
        super().__init__(level=level, formatter=formatter)
        self._closed = True
        self._filename = filename
        self._stream = None

    @property
    def closed(self):
        return self._closed

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value: FileWriteStream):
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
        if not self.stream:
            self.stream = await FileWriteStream.from_path(
                path=self._filename, append=True
            )
            self._closed = False

        if self.closed:
            raise ValueError("I/O operation on closed file")

        await self.acquire()
        try:
            await self.stream.send(msg.encode())
        finally:  # noqa
            self.release()

    async def close(self):
        if not self.closed:
            await self.stream.aclose()
            self._closed = True
