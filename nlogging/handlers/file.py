from typing import TYPE_CHECKING, Optional

from anyio.streams.file import FileWriteStream

from .base import BaseAsyncHandler

if TYPE_CHECKING:
    from logging import LogRecord
    from os import PathLike

    from nlogging._types import LevelType
    from nlogging.formatters import BaseFormatter


class AsyncFileHandler(BaseAsyncHandler):
    _stream: Optional[FileWriteStream]

    terminator = b"\n"

    def __init__(
        self,
        filename: "str | PathLike[str]",
        level: "LevelType",
        formatter: "BaseFormatter",
    ):
        super().__init__(level=level, formatter=formatter)
        self.closed = True
        self._filename = filename
        self._stream = None

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value: Optional[FileWriteStream]):
        if self.is_open:
            raise RuntimeError("Cannot change stream on open handler")

        if self.stream is value:
            return

        self._stream = value

    @property
    def is_open(self):
        return bool(self.stream) and (not self.closed)

    async def emit(self, record: "LogRecord"):
        try:
            msg = self.format(record) + self.terminator
            await self.write_and_flush(msg)
        except:  # noqa
            await self.handle_error(record)

    async def write_and_flush(self, msg: bytes):
        if not self.stream:
            async with self.lock:
                self.stream = await FileWriteStream.from_path(
                    path=self._filename, append=True
                )
                self.closed = False

        if not self.is_open:
            raise RuntimeError("I/O operation on closed file")

        async with self.lock:
            await self.stream.send(msg)

    async def close(self):
        if self.is_open:
            async with self.lock:
                await self.stream.aclose()
                self.stream = None
                self.closed = True
